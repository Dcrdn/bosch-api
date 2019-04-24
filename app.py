import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
account_sid = 'ACa9513b791536c7a97c306e8f9b6c9a79'
auth_token = '07c24096e11336cd33017101119f72e0'
account_sid2 = 'AC01310a6100555a897c5e4cf36f4bc601'
auth_token2 = '5be98f5de25583f76a5e1354f6bd442d'
client = Client(account_sid, auth_token)
client2 = Client(account_sid2, auth_token2)
from models import Usuarios

@app.route("/")
def hello():
    return "puto el que lo lea exepto Dafne, hi"

@app.route("/sms", methods=['POST'])
def sms_reply():
    fromMessage = request.form.get('From')
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    r=requests.post("https://bosch-nlp.herokuapp.com/intent", json=parametros)
    toSend=r.json()["response"]["name"]
    if(toSend=="saludos"):
        mensaje="Hola! Te puedo ayudar a comprar/cotizar autopartes con proveedores externos o con nuestro aliado PartsTech. ¿Con quien te gustaria?"
    else:
        mensaje="no jala"
    toSend=mensaje
    resp.message("*HERE IS YOUR MESSAGE jeje*: {}".format(toSend))
    if fromMessage == 'whatsapp:+5213332005486':
        message = client2.messages.create(
                              body='{}'.format(toSend),
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+5213314585897'
                          )
    else: 
        message = client.messages.create(
                              body='{}'.format(msg),
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+5213332005486',
                              media_url='https://frasesparami.com/wp-content/uploads/2017/06/IMAGENES-DE-RISA-CON-FRASES.jpg'
                          )
    print(message)
    return str(resp)

@app.route("/messenger", methods=['POST'])
def messenger_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    r=requests.post("https://bosch-nlp.herokuapp.com/intent", json=parametros)
    toSend=r.json()["response"]["name"]
    toSend=getInfo(toSend)
    resp.message("HERE IS YOUR MESSAGE jeje: {}".format(toSend))
    return str(resp)




# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure




if __name__ == '__main__':
    app.run()