from flask import Flask
from flask_assistant import Assistant, ask, tell
import logging
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

app = Flask(__name__)
assist = Assistant(app, route='/')


@assist.action('Default Fallback Intent')
def greet_and_start():
    speech = "Hello World from DJS woz app!"
    return ask(speech)

if __name__ == '__main__':
    app.run(debug=True)