from flask import Flask, request, jsonify, render_template, redirect, url_for, current_app, g
from flask_assistant import Assistant, ask, tell, event
#from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from sqlalchemy import Table
import models
from database import SessionLocal, engine
from waitress import serve

import dialogflow
import requests
import json
import pusher
import time
import pickle
import os

# wtf-form load
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap

# Initial Flask App config and Flask-session
app = Flask(__name__)
assist = Assistant(app, route='/')

models.Base.metadata.create_all(bind=engine)
print(models.UserQuery.__table__)

#CORS(app)
#app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap(app)


user_utter="Listening..."
wizard_utter="No Response"

class NameForm(Form):
    name = StringField('Enter Response...', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    #return render_template('first.html', query=cache.get("user_utterance"))
    
    # if (db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().user_request == "No Response"):
    #     db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().user_request = "Conversation End"
    #     db.commit()
    # if (db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response == "No Response"):
    #     db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response =  "Conversation End"
    #     db.commit()
    
    return render_template('index.jsx', query=user_utter)
    

#@app.route('/webhook', methods=['POST'])
@assist.action('Default Fallback Intent')
def webhook():

    db_user = SessionLocal()

    data = request.get_json(silent=True)
    query = data['queryResult']['queryText']
    global user_utter

    # Set global variable that wizard listens to for query
    user_utter = query

    # Add new query to db
    new_user_utr = models.UserQuery(user_request=query)
    db_user.add(new_user_utr)
    db_user.commit()

    time.sleep(3.4)

    wiz_db_resp = db_user.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response
    db_user.close()
    if(wiz_db_resp== "No Response"):
        return event('attempt-1')
    else:
        return ask(str(wiz_db_resp))

@assist.action('Default Fallback Intent - Attempt1')
def attempt1():
    db_user = SessionLocal()
    time.sleep(3.4)
    wiz_db_resp = db_user.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response
    db_user.close()
    if(wiz_db_resp== "No Response"):
        return event('attempt-2')
    else:
        return ask(str(wiz_db_resp))

@assist.action('Default Fallback Intent - Attempt2')
def attempt2():
    db_user = SessionLocal()
    time.sleep(3.4)
    wiz_db_resp = db_user.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response
    db_user.close()
    if(wiz_db_resp== "No Response"):
        return ask("Sorry, I couldn't find any response to that. Could you please repeat?")
    else:
        return ask(str(wiz_db_resp))

@assist.action('Default Fallback Intent - Attempt3')
def attempt3():
    db_user = SessionLocal()
    time.sleep(3.4)
    wiz_db_resp = db_user.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response
    db_user.close()
    if(wiz_db_resp== "No Response"):
        return ask("Sorry, I couldn't find any response to that.")
    else:
        return ask(str('attempt3'+wiz_db_resp))

@app.route('/webhook', methods=['GET'])
def renderUserQuery():
    if(user_utter == "Listening..."):
        return render_template('UserQuery.html', query = "")
    else:
        return render_template('UserQuery.html', query = user_utter)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", "djs wizard says"+message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


@app.route('/send_response', methods=['POST'])
def send_response():
    message = request.form['response']
    db_wiz = SessionLocal()
    global user_utter
    global wizard_utter
    
    # User and Wizard utterance from last record
    user_utterance = db_wiz.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().user_request
    wizard_utterance = db_wiz.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response

    if (user_utterance == user_utter and user_utterance != "Listening..." and wizard_utterance == "No Response"):

        # Setting global variable
        wizard_utter = message

        # Updating last query wizard response
        db_wiz.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response = message
        db_wiz.commit()
        db_wiz.close()
    user_utter="Listening..."
    
    # project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    # fulfillment_text = detect_intent_texts(project_id, "unique", "wizard says "+message, 'en')
    # response_text = { "message":  fulfillment_text }
    # return jsonify(response_text)
    return message

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    #main()
    #app.run()
    # server = Server(app.wsgi_app)
    # server.serve()
    
    #app.secret_key=os.urandom(32)
    serve(app, host='0.0.0.0', port=80)
    #socketio.run(app)