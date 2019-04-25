import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from information import existeMarca, existeModelo, existeSubmodelo, existeMotor, getPrice, js_read, js_save, existeParte
import requests
import sys
import time
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

@app.route("/")
def hello():
    return "API of the team BeMyGuide at Bosch Hackathon TalentLand 2019"

@app.route("/sms", methods=['POST'])
def messenger_reply2():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    user=request.form.get('From')
    other = request.form.get('To')
    other = str(other)

    r=requests.post("https://bosch-nlp.herokuapp.com/intent", json=parametros)
    
    toSend=r.json()["response"]["name"]
    user=str(user)
    dicInfo=js_read()

    if(toSend==None):
        a=1
    elif(msg.lower()=="no" or msg=="bye"):
        toSend="Okay"
        dicInfo[user]["next"]=None
        js_save(dicInfo)
        resp.message("{}".format(toSend))
        time.sleep(2)
        return str(resp)   
    if(user in dicInfo):
        if(dicInfo[user]["next"]!=None):
            toSend=dicInfo[user]["next"]

    if(str(toSend)=="saludos"):
        toSend="Hi, I can assist you to buy automobile parts. Would you like to work with our suppliers or with our partner PartsTech?"
    elif(str(toSend)=="decision.pt"):
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
        dicInfo[user]={"prove":False, "next":"marca"}
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend="What is the branch of the car?"
    elif(str(toSend)=="decision.prove"):
        dicInfo[user]={"prove":True, "next":"marca"}

        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
        resp.message("{}".format(toSend))
        time.sleep(2)

        toSend="What is the branch of the car?"
    elif(str(toSend)=="marca"):
        res=existeMarca(msg.lower())
        if(res==None):
            toSend="We didn't find that branch in our database. Try with another one"            
        else:            
            info=dicInfo[user]
            info["marca"]=res[0]
            info["marcaId"]=res[1]
            info["next"]="year"
            dicInfo[user]=info
            toSend="Great. What is the year of the car?"
    elif(str(toSend)=="year"):
        year=msg.split()
        year=year[-1]
        res=dicInfo[user]
        res["year"]=year
        res["next"]="modelo"
        dicInfo[user]=res
        toSend="Okay. What is the model of the car?"
    elif(str(toSend)=="modelo"):
        info=existeModelo(msg.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"]) #elantra
        if(info==None):
            toSend="We didn't find that model in our database. Try with another one"            
        else: 
            res=dicInfo[user]
            res["modelo"]=info[0]
            res["modeloId"]=info[1]
            res["next"]="modelo.sub"
            dicInfo[user]=res
            toSend="Cool. What is the submodel of the car?"
    elif(str(toSend)=="modelo.sub"):
        info=existeSubmodelo(msg.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"])
        if(info==None):
            toSend="We didn't find that submodel in our database. Try with another one"            
        else: 
            res=dicInfo[user]
            res["submodelo"]=info[0]
            res["submodeloId"]=info[1]
            res["next"]="motor"
            dicInfo[user]=res
            toSend="Almost done. What is the name of the engine? "
    elif(str(toSend)=="motor"):
        info=existeMotor("the motor is 1.8L L4 vin E DOHC  ULEV".lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"])
        if(info==None):
            toSend="We didn't find that model in our database. Try with another one"            
        else: 
            res=dicInfo[user]
            toSend="Great! Now tell me the auto part you want to buy"
            res["engineName"]=info[0]
            res["engineId"]=info[1]
            res["engine"]=info[2]
            res["next"]="part"
            dicInfo[user]=res
    elif(str(toSend)=="part"): #the part i want is the -..-.-.
        part=existeParte(msg.lower())
        if(part==None):
            toSend="We didn't find that part in our database. Try with another one"            
        else: 
            price= getPrice(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"], dicInfo[user]["engineId"], dicInfo[user]["engine"]["engineParams"], part)
            idPart=price[0]
            price=price[3]
            res=dicInfo[user]
            res["partId"]=idPart
            res["partPrice"]=price
            res["partName"]=part
            prove=dicInfo[user]["prove"]
            if(prove):
                toSend="Tell me how many pieces do you want"
                res["next"]="pieces"
            else:    
                toSend="The "+ part +" costs: "+ str(price) 
                resp.message("{}".format(toSend))
                time.sleep(2)
                toSend="Do you want to add it to your cart?"
                res["next"]="cart"
            dicInfo[user]=res
    elif(str(toSend)=="pieces"): #diego --> pieces
        piezas=msg.split()
        piezas=piezas[-1]
        res=dicInfo[user]
        res["totalPieces"]=piezas
        res["next"]=None

        dicInfo[user]=res
        toSend="Do you want to buy something else or do you want send the request to our providers?"
    elif(str(toSend)=="providers"): #diego --> pieces
        #envio a provedores, hacer algo aqui en whats
        toSend="aqui se hace algo pero pa wats juejue"
    elif(str(toSend)=="cart"):
        #aqui la agrego al carrito
        info=dicInfo[user]
        if("cart" in info):
            data=info["cart"]
            data.append([dicInfo[user]["partId"],dicInfo[user]["partName"], dicInfo[user]["partPrice"]])
            info["cart"]=data
        else:
            info["cart"]=[[dicInfo[user]["partId"],dicInfo[user]["partName"], dicInfo[user]["partPrice"]]]
        info["next"]=None
        dicInfo[user]=info
        toSend="Do you want to buy something else or you want to do the checkout?"
    elif(str(toSend)=="buyelse"):
        toSend="Is it for the same car?"
    elif(str(toSend)=="samecar"):
        res=dicInfo[user]
        res["next"]="part"
        dicInfo[user]=res
        toSend="Great!  Now tell me the auto part you want to buy"
    elif(str(toSend)=="checkout"):
        comprar=dicInfo[user]["cart"]
        total=0
        for element in comprar:
            total+=int(element[2])
            toSend="Product: " + element[1] +"   Price: " + str(element[2])
            resp.message("{}".format(toSend))   
            time.sleep(2)         
        toSend="Your total is: " + str(total)
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend="Do you want to pay with whatsapp payments or via bank deposit?"
    elif(str(toSend)=="bankdeposit"):
        toSend = "Great. Here you have the bank details"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend = "Bank Account: XXXXXXXXXXXXXXXXXXXXXXX"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend = "Reference: XXXX"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend="Please provide us an address and name to send the product when your payment is accepted"
    elif(str(toSend)=="address"):
        toSend="Perfect. We will let you know when your package it's on it's way"
    elif(str(toSend)=="despedidas"):
        dicInfo={}
        toSend="I'll be here if you need something else."
    js_save(dicInfo)
    resp.message("{}".format(toSend))
    time.sleep(2)
    return str(resp)

@app.route("/messenger", methods=['POST'])
def messenger_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    user=request.form.get('From')

    r=requests.post("https://bosch-nlp.herokuapp.com/intent", json=parametros)

    toSend=r.json()["response"]["name"]
    user=str(user)
    dicInfo=js_read()

    if(toSend==None):
        a=1
    elif(msg.lower()=="no" or msg=="bye"):
        toSend="Okay"
        dicInfo[user]["next"]=None
        js_save(dicInfo)
        resp.message("{}".format(toSend))
        return str(resp)   
    if(user in dicInfo):
        if(dicInfo[user]["next"]!=None):
            toSend=dicInfo[user]["next"]

    if(str(toSend)=="saludos"):
        toSend="Hi, I can assist you to buy automobile parts. Would you like to work with our suppliers or with our partner PartsTech?"
    elif(str(toSend)=="decision.pt"):
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
        dicInfo[user]={"prove":False, "next":"marca"}
        resp.message("{}".format(toSend))
        toSend="What is the branch of the car?"
    elif(str(toSend)=="decision.prove"):
        dicInfo[user]={"prove":True, "next":"marca"}

        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
        resp.message("{}".format(toSend))
        toSend="What is the branch of the car?"
    elif(str(toSend)=="marca"):
        res=existeMarca(msg.lower())
        if(res==None):
            toSend="We didn't find that branch in our database. Try with another one"            
        else:            
            info=dicInfo[user]
            info["marca"]=res[0]
            info["marcaId"]=res[1]
            info["next"]="year"
            dicInfo[user]=info
            toSend="Great. What is the year of the car?"
    elif(str(toSend)=="year"):
        year=msg.split()
        year=year[-1]
        res=dicInfo[user]
        res["year"]=year
        res["next"]="modelo"
        dicInfo[user]=res
        toSend="Okay. What is the model of the car?"
    elif(str(toSend)=="modelo"):
        info=existeModelo(msg.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"]) #elantra
        if(info==None):
            toSend="We didn't find that model in our database. Try with another one"            
        else: 
            res=dicInfo[user]
            res["modelo"]=info[0]
            res["modeloId"]=info[1]
            res["next"]="modelo.sub"
            dicInfo[user]=res
            toSend="Cool. What is the submodel of the car?"
    elif(str(toSend)=="modelo.sub"):
        info=existeSubmodelo(msg.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"])
        if(info==None):
            toSend="We didn't find that submodel in our database. Try with another one"            
        else: 
            res=dicInfo[user]
            res["submodelo"]=info[0]
            res["submodeloId"]=info[1]
            res["next"]="motor"
            dicInfo[user]=res
            toSend="Almost done. What is the name of the engine? "
    elif(str(toSend)=="motor"):
        info=existeMotor("the motor is 1.8L L4 vin E DOHC  ULEV".lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"])
        if(info==None):
            toSend="We didn't find that model in our database. Try with another one"            
        else: 
            res=dicInfo[user]
            toSend="Great! Now tell me the auto part you want to buy"
            res["engineName"]=info[0]
            res["engineId"]=info[1]
            res["engine"]=info[2]
            res["next"]="part"
            dicInfo[user]=res
    elif(str(toSend)=="part"): #the part i want is the -..-.-.
        part=existeParte(msg.lower())
        if(part==None):
            toSend="We didn't find that part in our database. Try with another one"            
        else: 
            price= getPrice(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"], dicInfo[user]["engineId"], dicInfo[user]["engine"]["engineParams"], part)
            idPart=price[0]
            price=price[3]
            res=dicInfo[user]
            res["partId"]=idPart
            res["partPrice"]=price
            res["partName"]=part
            prove=dicInfo[user]["prove"]
            if(prove):
                toSend="Tell me how many pieces do you want"
                res["next"]="pieces"
            else:    
                toSend="The "+ part +" costs: "+ str(price) 
                resp.message("{}".format(toSend))
                toSend="Do you want to add it to your cart?"
                res["next"]="cart"
            dicInfo[user]=res
    elif(str(toSend)=="pieces"): #diego --> pieces
        piezas=msg.split()
        piezas=piezas[-1]
        res=dicInfo[user]
        res["totalPieces"]=piezas
        res["next"]=None

        dicInfo[user]=res
        toSend="Do you want to buy something else or do you want send the request to our Jobbers?"
    elif(str(toSend)=="jobbers"): #diego --> pieces
        #envio a provedores, hacer algo aqui en whats
        toSend="aqui se hace algo pero pa wats juejue"
    elif(str(toSend)=="cart"):
        #aqui la agrego al carrito
        info=dicInfo[user]
        if("cart" in info):
            data=info["cart"]
            data.append([dicInfo[user]["partId"],dicInfo[user]["partName"], dicInfo[user]["partPrice"]])
            info["cart"]=data
        else:
            info["cart"]=[[dicInfo[user]["partId"],dicInfo[user]["partName"], dicInfo[user]["partPrice"]]]
        info["next"]=None
        dicInfo[user]=info
        toSend="Do you want to buy something else or you want to do the checkout?"
    elif(str(toSend)=="buyelse"):
        toSend="Is it for the same car?"
    elif(str(toSend)=="samecar"):
        res=dicInfo[user]
        res["next"]="part"
        dicInfo[user]=res
        toSend="Great!  Now tell me the auto part you want to buy"
    elif(str(toSend)=="checkout"):
        comprar=dicInfo[user]["cart"]
        total=0
        for element in comprar:
            total+=int(element[2])
            toSend="Product: " + element[1] +"   Price: " + str(element[2])
            resp.message("{}".format(toSend))            
        toSend="Your total is: " + str(total)
        resp.message("{}".format(toSend))
        toSend="Do you want to pay with whatsapp payments or via bank deposit?"
    elif(str(toSend)=="bankdeposit"):
        toSend = "Great. Here you have the bank details"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend = "Bank Account: XXXXXXXXXXXXXXXXXXXXXXX"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend = "Reference: XXXX"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend="Please provide us an address and name to send the product when your payment is accepted"
    elif(str(toSend)=="address"):
        toSend="Perfect. We will let you know when your package it's on it's way"
    elif(str(toSend)=="despedidas"):
        dicInfo={}
        toSend="I'll be here if you need something else."
    js_save(dicInfo)
    resp.message("{}".format(toSend))
    return str(resp)

if __name__ == '__main__':
    app.run()