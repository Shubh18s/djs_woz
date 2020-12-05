# Spoken Dialog WOZ (djs_woz): A tool to perform Wizard of Oz experiments in speech-only Question Answering scenarios

Spoken Dialog WOZ is a web app that can be integrated with a smart speaker such as Google Nest Mini to conduct Wizard of Oz experiments in a speech-only scenarios. The user (participant) interacts with the system using the smart speaker unaware about the existence of a human(wizard) controlling the system either partially or completely to respond to user's queries. The experimenter provides the strategies/scripts for a successful dialogue between the user and the system. The wizard follows these scripts to answer user's queries effectively with minimal congnitive load.

# Instructions to Run:
Running Spoken Dialog WOZ in a development environment requires installing NodeJS and Python preferably 3.x or higher. You will also need to install ngrok. Once installed, In order to Run Spoken Dialog WOZ follow the below steps - 
1. Open the terminal and create a new environment using the command - <i>python -m venv PATH_TO_DJS_ENV</i>
2. Activate the djs-env by running - <i>PATH_TO_DJS_ENV/Scripts\activate</i>
3. Clone the djs_woz repository - <i>git clone https://github.com/Shubh18s/djs_woz.git</i>
4. Install all the required python packages by running - (i) <i>cd PATH_TO_DJS_WOZ</i> and (ii) <i>pip install -r requirements.txt</i>
5. To start the webhook, run - (i) <i>set FLASK_APP=index.py</i> and (ii) <i>flask run</i>
6. Open a second terminal and install all the required node modules by running - (i) <i>cd PATH_TO_DJS_WOZ/static</i> and (ii) <i>npm install</i>
7. While in the static directory, build the webpack and generate bundle.js by running - <i>npm run watch</i>
8. Open a third terminal and run - (i) <i>cd PATH_TO_NGROK_FOLDER</i> and (ii) <i>ngrok http 5000</i>
9. In Dialogflow, within the agent created, update the webhook service URL for fulfillment using the public URL created by ngrok and save.
10. Open the Web browser and visit http://localhost:5000/. A user interface should present.
