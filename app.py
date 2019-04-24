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

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    resp.message("*HERE IS YOUR MESSAGE*: {}".format(msg))
    message = client.messages.create(
                              body='Hello there!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+5213332005486'
                          )
    return str(message.sid.body)



# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure




if __name__ == '__main__':
    app.run()