# /index.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, current_app
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
import dialogflow
import requests
import json
import pusher
import time
import pickle
import os

#from app import app
from livereload import Server

# wtf-form load
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_bootstrap import Bootstrap

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'djs_woz.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class UserQuery(db.Model):
    __tablename__ = 'userquery'
    id = db.Column(db.Integer, primary_key=True)
    user_request = db.Column(db.Text, default="Listening...")
    wizard_response = db.Column(db.Text, default="No Response")
    def __repr__(self):
       return("'{0}', '{1}'".format(self.user_request, self.wizard_response))




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
    #cache['user_query']="Listening..."
    #cache['wizard_response']="No response"

    global user_query
    global wizard_response
    user_query="Listening..."
    wizard_response="No response"

    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''


        #request.wizard_response=form.name.data
    #return render_template('index.html')
    # if g.query:
    #     return render_template('first.html', form=form, name=name, query=g.query)
    # else:
    return render_template('first.html', form=form, name=name, query=user_query)
    #return render_template('first.html', query=cache['user_query'])

# def getResponseFromWizard(user_query=""):
#     return redirect(url_for('/', query=cache['user_query']))

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    query = data['queryResult']['queryText']
    
    #return redirect(url_for('index'), query=query)
    global user_query
    global wizard_response
    #user_query=query
    time.sleep(2)
    if(user_query=="Listening..."):
        user_query=query
        tempResp = "Did you say, "+query+"?"

        reply = {
            "fulfillmentText": tempResp,
        }
        return jsonify(reply)
    else:
        time.sleep(2)
        #user_query="Listening..."
        
        reply = {
            "fulfillmentText": wizard_response,
        }
        # global wizard_response
        user_query="Listening..."
        
        wizard_response="No response"
        return jsonify(reply)
        
    #wizard_response=""
    #return jsonify(reply)
    


    #return getResponse()
    
    # if(wizard_response!=""):
    #     reply = {
    #         "fulfillmentText": wizard_response,
    #     }
    #     return jsonify(reply)
    # else:
    #     time.sleep(2)
    #     reply = {
    #         "fulfillmentText": "Sorry!",
    #         }
    #     return jsonify(reply)

    
    
    #getResponseFromWizard(query)

def getResponse():
    count=0
    if(wizard_response!=""):
        reply = {
            "fulfillmentText": wizard_response,
        }
        wizard_response=""
        return jsonify(reply)
    else:
        if(count==0):
            time.sleep(2)
            count=1
            getResponse()
        else:
            reply = {
            "fulfillmentText": "Sorry!",
            }
            return jsonify(reply)


@app.route('/webhook', methods=['GET'])
def renderUserQuery():
    if user_query:
        current_exchange = UserQuery.query.order_by(UserQuery.id.desc()).first().user_request
        if current_exchange is None:
            return render_template('UserQuery.html', query = "Listening...")
        else:
            return render_template('UserQuery.html', query = current_exchange)
        
        #return render_template('UserQuery.html', query=user_query)


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