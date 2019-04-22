import os
import json
import datetime
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

from models import Usuarios

@app.route("/")
def hello():
    return "puto el que lo lea exepto Dafne"

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    resp.message("HERE IS YOUR MESSAGE: {}".format(msg))
    return str(resp)


if __name__ == '__main__':
    app.run()