# /index.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, current_app, g

from flask_session import Session
from flask_socketio import SocketIO, emit


from flask import _app_ctx_stack
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from sqlalchemy import Table

import models
from database import SessionLocal, engine

from waitress import serve
#from flask_sqlalchemy import SQLAlchemy
import dialogflow
import requests
import json
import pusher
import time
import pickle
import os

#from app import app
#from livereload import Server

# wtf-form load
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap

# Initial Flask App config and Flask-session
app = Flask(__name__)
app.config['SESSION_TYPE']='redis'
sess=Session(app)
# socketio = SocketIO(app, manage_session=False)

# Creating database metadata and session
db = SessionLocal() 
models.Base.metadata.create_all(bind=engine)
print(models.UserQuery.__table__)

# @app.route('/set/')
# def set():
#     session['key'] = 'value'
#     return 'ok'

# @app.route('/get/')
# def get():
#     return session.get('key', 'not set')


## Flask_sql_alchemy config
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'djs_woz.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# db = SQLAlchemy(app)


CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap(app)

user_query="Listening..."
wizard_response="No response"

cache = {}

class NameForm(Form):
    name = StringField('Enter Response...', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    sess['user_utterance'] = ""
    sess['wizard_utterance'] = ""
    return render_template('first.html', query=user_query)
    

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    query = data['queryResult']['queryText']
    
    #reply_diag=""
    #diag_prev_req = db.query(models.UserQuery).order_by(models.UserQuery.id.desc()).first() 
    # if diag_prev_req:
    #     if(diag_prev_req.wizard_response=="No Response"):
    #         reply_diag = "Please hold!! We're still getting the response"
    #     else:
    #         diag_new_req = models.UserQuery(user_request=query)
    #         db.add(diag_new_req)
    #         reply_diag = "Preparing response..."
        
    if(sess.get('user_utterance')==""):
        sess['user_utterance']=query
        reply = {
            "fulfillmentText": "Preparing response. Please hold.",
        }
    else:
        reply = {
            "fulfillmentText": "Please hold for previous response.",
        }

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

    if(sess.get('user_utterance')==""):
        return render_template('UserQuery.html', query = "Listening...")
    else:
        return render_template('UserQuery.html', query = sess.get["user_utterance"])


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
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
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


#def main():
 #   print(dialogflow.SessionsClient())
  #  print(os.getenv('DIALOGFLOW_PROJECT_ID'))

# run Flask app
if __name__ == "__main__":
    #main()
    #app.run()
    # server = Server(app.wsgi_app)
    # server.serve()
    
    
    serve(app, host='0.0.0.0', port=80)
    #socketio.run(app)