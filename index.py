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
    

# Correct syntax  - db.query(models.UserQuery).all()
# query=db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).limit(1) 


    #conn = engine.connect()
    #reply_diag=""
    # diag_prev_req = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first()
    # reply = {
    #     "fulfillmentText": diag_prev_req,
    # }
    # if diag_prev_req:
    #     if(diag_prev_req.wizard_response=="No Response"):
    #         reply_diag = "Please hold!! We're still getting the response"
    #     else:
    #         diag_new_req = models.UserQuery(user_request=query)
    #         db.add(diag_new_req)
    #         reply_diag = "Preparing response..."
    
    # if cache.get("user_utterance"):
    #     reply = {
    #         "fulfillmentText": "Please hold for previous response.",
    #     }
    # else:
    #     cache.set("user_utterance", query)
    #     reply = {
    #         "fulfillmentText": "Preparing response. Please hold.",
    #     }    

    global user_utter
    
    #db_resp = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).limit(1)
    try:
        user_utterance = db.query(models.UserQuery.user_request).order_by(models.UserQuery.id.desc()).first().user_request
        try:
            wizard_utterance = db.query(models.UserQuery.user_request).order_by(models.UserQuery.id.desc()).first().wizard_response
            


            #[[[new record]]] (1,1)
            user_utter = query
            new_user_utr = models.UserQuery(user_request=query)
            db.add(new_user_utr)
            db.commit()

            # Update last record query here above this
            reply = {
                #"fulfillmentText": db_resp,
                "fulfillmentText": "Preparing response. Please hold.",
            }
        except:

            #[[[Nothing happens]]] (1,0)

            reply = {
                "fulfillmentText": "Please hold for previous response.",
            }
    except:
        try:
            wizard_utterance = db.query(models.UserQuery.user_request).order_by(models.UserQuery.id.desc()).first().wizard_response
            
            #[[[Update last record]]] (0,1)
            user_utter = query


            reply = {
                #"fulfillmentText": db_resp,
                "fulfillmentText": "Preparing response. Please hold.",
            }
        except:

            #[[[This will never be true, something will always be in last record]]]

            reply = {
                "fulfillmentText": "Preparing response. Please hold.",
            }





        user_utter = query
        new_user_utr = models.UserQuery(user_request=query)
        db.add(new_user_utr)
        db.commit()
        reply = {
                #"fulfillmentText": db_resp,
                "fulfillmentText": "Preparing response. Please hold.",
            }
    # if(db )#(user_utter == "Listening..."):
    #     if db_resp.:#(wizard_utter == "No response"):
    #         user_utter = query
    #         # ins = models.UserQuery.insert()
    #         # conn.execute(ins, user_request=query, user_sent=1)
    #         models.UserQuery.insert(user_request=query, user_sent=1)
    #         reply = {
    #             #"fulfillmentText": db_resp,
    #             "fulfillmentText": "Preparing response. Please hold.",
    #         }
    #     else:
    #         reply = {
    #             "fulfillmentText": "Please hold for previous response.",
    #         }
    # else:
    #     reply = {
    #             "fulfillmentText": "Preparing previous response. Please hold.",
    #         }
            
    return jsonify(reply)


# @socketio.on('connect', namespace='/wizard_integration')
# def wizard_connect():
#     print('Wizard connected')

# @socketio.on('disconnect', namespace='/wizard_integration')
# def wizard_disconnect():
#     print('Wizard disconnected')

# @socketio.on('get user query', namespace='/test')
# def get_user_query(message):
#     emit('user query', {'data': message['data']})

@app.route('/webhook', methods=['GET'])
def renderUserQuery():
    #diag_prev_req = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first() 
    
    # if diag_prev_req:
    #     if(diag_prev_req.wizard_response=="No Response"):
    #         return render_template('UserQuery.html', query = diag_prev_req.user_request)
    # else:
    #     return render_template('UserQuery.html', query = "Listening...")

    if(user_utter == "Listening..."):
        return render_template('UserQuery.html', query = "")
    else:
        return render_template('UserQuery.html', query = user_utter)
    

    # if cache.get("user_utterance"):
    #     return render_template('UserQuery.html', query = cache.get("user_utterance"))
    # else:
    #     return render_template('UserQuery.html', query = "Listening")


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
    fulfillment_text = detect_intent_texts(project_id, "unique", "query_response:"+message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


@app.route('/send_response', methods=['POST'])
def send_response():
    global wizard_response
    wizard_response=request.form['response']
    return wizard_response
    #wizard_response=request.form['response']
    #return cache['wizard_response']

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# @socketio.on('render query', namespace='/queryRenderSocket')
# def render_user_utterance():
#     emit('user utterance', {'data': 'This is user utterance'})


#def main():
 #   print(dialogflow.SessionsClient())
  #  print(os.getenv('DIALOGFLOW_PROJECT_ID'))

# run Flask app
if __name__ == "__main__":
    #main()
    #app.run()
    # server = Server(app.wsgi_app)
    # server.serve()
    
    #app.secret_key=os.urandom(32)
    #serve(app, host='0.0.0.0', port=80)
    socketio.run(app)