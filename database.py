from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

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
        return ('<Req %r Res %r>' % self.request, self.response)


if __name__ == "__main__":
    app.run()