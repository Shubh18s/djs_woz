from flask_bootstrap import Bootstrap

from flask import Flask, render_template
from flask_assistant import Assistant, ask, tell, event
from flask_assistant import request
import logging
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

app = Flask(__name__)

bootstrap = Bootstrap(app)
assist = Assistant(app, route='/')
query = ""

@assist.action('Default Fallback Intent')
def greet_and_start():
    user_query = request['queryResult']['queryText']
    speech = "You said " + user_query
    query = user_query
    return ask(speech)


    #return render_template("WoZ_Speech_Check.html", query=user_query)
    #return event(index, query=user_query)
    #speech = "Hello from DJS WOZ app!"
    #speech = "Your favorite color is {}".format(user_says)
    #return ask(speech)
    #return render_template("WoZ_Speech_Check.html")

@app.route('/')
def index(query=query):
    return render_template("WoZ_Speech_Check.html", query=query)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)