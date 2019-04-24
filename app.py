import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from information import existeMarca, existeModelo, existeSubmodelo
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
#from models import Usuarios

dicInfo={}

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
    user=request.form.get('From')
    print(user)
    print(type(user))
    print(user["messenger"])
    global dicInfo

    r=requests.post("https://bosch-nlp.herokuapp.com/intent", json=parametros)
    toSend=r.json()["response"]["name"]
    if(str(toSend)=="saludos"):
        toSend="Hi, I can help you to buy automobile pars. Would you like to work with our providers or with our partner PartsTech?"
        print("-----------------hey")
    elif(str(toSend)=="decision.pt"):
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
        resp.message("{}".format(toSend))
        toSend="What is the branch of the car?"
    elif(str(toSend)=="marca"):
        marca=msg.split()
        marca=marca[-1]
        res=existeMarca(marca.lower())
        dicInfo[user]={"marca":marca, "marcaId":res[1]}
        toSend="Great. What is the year of the car? marca: "+ marca +", id: "+ str(res[1])
        print(dicInfo)
    elif(str(toSend)=="year"):
        year=msg.split()
        year=year[-1]
        res=dicInfo[user]
        res["year"]=year
        dicInfo[user]=res
        toSend="Okay. What is the model of the car? year: "+ year
        print(dicInfo)        
    elif(str(toSend)=="modelo"):
        modelo=msg.split()
        modelo=modelo[-1]
        print("---------------")
        print(dicInfo)
        info=existeModelo(modelo.lower(), dicInfo["user"]["year"], dicInfo["user"]["marcaId"]) #elantra

        res=dicInfo[user]
        res["modelo"]=modelo
        res["modeloId"]=info[1]

        dicInfo[user]=res
        toSend="Yikes. What is the submodel of the car? modelo: "+ modelo + " id: " + str(info[1])
        print(dicInfo)
    elif(str(toSend)=="modelo.sub"):
        submodelo=msg.split()
        submodelo=submodelo[-1]
        info=existeSubmodelo(submodelo.lower(), dicInfo["user"]["year"], dicInfo["user"]["marcaId"], dicInfo["user"]["modeloId"])
        res=dicInfo[user]
        res["submodelo"]=submodelo
        res["submodeloId"]=info[1]
        dicInfo[user]=res

        toSend="Almost done. What is the name of the engine? sub: "+ submodelo + " id: "+ str(info[1])
        print(dicInfo)
    elif(str(toSend)=="motor"):
        engine=msg.split()
        engine=subenginemodelo[-1]
        info=existeMotor("1.8L L4 vin E DOHC  ULEV".lower(), dicInfo["user"]["year"], dicInfo["user"]["marcaId"], dicInfo["user"]["modeloId"], dicInfo["user"]["submodeloId"])

        res=dicInfo[user]
        toSend="Great! Now tell me the auto part you want to buy"
        res["engineName"]=engine
        res["engineId"]=info[1]
        res["engine"]=info[2]
        dicInfo[user]=res
        print(dicInfo)
    elif(str(toSend)=="part"): #the part i want is the -..-.-.
        oracion=msg.split()
        index=oracion.index("is")
        message=oracion[index+2:]
        part=' '.join(message)

        toSend="The part you want to buy costs: X. part is: "+ part
        resp.message("{}".format(toSend))
        toSend="Do you want to add it to your cart?"
    elif(str(toSend)=="cart"):
        #aqui la agrego al carrito
        toSend="Do you want to buy something else or you want to do the checkout?"
    elif(str(toSend)=="buyelse"):
        toSend="Is it for the same car?"
    elif(str(toSend)=="samecar"):
        toSend="Great! Now tell me the auto part you want to buy"
    elif(str(toSend)=="checkout"):
        toSend="your total would be Y ammount"
        resp.message("{}".format(toSend))
        toSend="Do you want to pay with whatsapp payments or via bank deposit?"
    elif(str(toSend)=="bankdeposit"):
        toSend="Great. Here you have the bank details"
        resp.message("{}".format(toSend))
        toSend="Please provide us an address to send the product when your payment is accepted"
    elif(str(toSend)=="address"):
        toSend="Perfect. We will let you know when your package it's on it's way"
    elif(str(toSend)=="despedidas"):
        dicInfo={}
        toSend="I'll be here if you need something else."
    else:
        print("no se pudo")
    resp.message("{}".format(toSend))
    return str(resp)

if __name__ == '__main__':
    app.run()