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
account_sid = 'ACa9513b791536c7a97c306e8f9b6c9a79'
auth_token = '07c24096e11336cd33017101119f72e0'
client = Client(account_sid, auth_token)

from models import Usuarios

@app.route("/")
def hello():
    return "puto el que lo lea exepto Dafne, hi"

@app.route("/sms", methods=['POST'])
def sms_reply():
    print(request.form)
    msg = request.form.get('Body')
    resp = MessagingResponse()
    resp.message("*HERE IS YOUR MESSAGE*: {}".format(msg))
    message = client.messages.create(
                              body='{}'.format(msg),
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+5213332005486'
                          )
    print(message.body)
    return str(resp)



# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure




if __name__ == '__main__':
    app.run()