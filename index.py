from flask import Flask, request, jsonify, render_template, redirect, url_for, current_app, g

from flask_cors import CORS
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
db = SessionLocal() 
models.Base.metadata.create_all(bind=engine)
print(models.UserQuery.__table__)

#CORS(app)
#app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap(app)

user_utter="Listening..."
wizard_utter="No response"

class NameForm(Form):
    name = StringField('Enter Response...', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    #return render_template('first.html', query=cache.get("user_utterance"))
    return render_template('first.html', query=user_utter)
    

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    query = data['queryResult']['queryText']
    global user_utter


    if "djs wizard says" in query:
        temp_query = query
        reply{
            "fulfillmentText": temp_query.split("djs wizard says",1)[1],
        }

    else:
        #db_resp = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).limit(1)
        user_utterance = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().user_request
        wizard_utterance = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response

        if (user_utterance != "Listening..." and wizard_utterance != "No Response"):
            #[[[new record]]] (1,1)
            user_utter = query
            new_user_utr = models.UserQuery(user_request=query)
            db.add(new_user_utr)
            db.commit()
            # Add new record above this
            reply = {
                #"fulfillmentText": db_resp,
                "fulfillmentText": "Preparing response. Please hold.",
            }
        elif (user_utterance == "Listening..." and wizard_utterance != "No Response"):
            #[[[Update last record]]] (0,1)
            user_utter = query
            db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().user_request = query
            db.commit()
            reply = {
                #"fulfillmentText": db_resp,
                "fulfillmentText": "Preparing response. Please hold.",
            }
        else:
            #[[[Nothing happens]]] (1,0) 
            reply = {
                "fulfillmentText": "Please hold for previous response.",
            }   

    return jsonify(reply)


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
    message = request.form['message']
    global user_utter
    global wizard_utter
    
    user_utterance = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().user_request
    wizard_utterance = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response

    if (user_utterance != "Listening..." and wizard_utterance != "No Response"):
        #[[[new record]]] (1,1)
        wizard_utter = message
        new_wiz_utr = models.UserQuery(wizard_response=message)
        db.add(new_wiz_utr)
        db.commit()
    elif (user_utterance != "Listening..." and wizard_utterance == "No Response"):
        wizard_utter = request.form['response']
        db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first().wizard_response = message
        db.commit()
    else:
        user_utter = "Can't send response. Waiting for user."
        time.sleep(30)
        user_utter="Listening..."
    
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", "djs wizard says"+message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)
    #return wizard_utter

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
    #serve(app, host='0.0.0.0', port=80)
    socketio.run(app)