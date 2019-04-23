import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

account_sid = 'AC01310a6100555a897c5e4cf36f4bc601'
auth_token = '5be98f5de25583f76a5e1354f6bd442d'
client = Client(account_sid, auth_token)

from models import Usuarios

@app.route("/")
def hello():
    return "puto el que lo lea exepto Dafne, hi"

def send_message(to, body):
   # Initialize client
   client = Client(account_sid, auth_token)
   client.messages.create(
       body=body,
       from_=os.getenv('+1 415 523 8886'),
       to=to
   )
@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.values.get('Body')
    send_message(to=request.values.get('From'), body="You sent {}".format(msg))
    return ('', 204)


if __name__ == '__main__':
    app.run()