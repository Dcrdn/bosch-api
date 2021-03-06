# coding: utf8
import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from information import existeMarca, getEngines, existeModelo, existeSubmodelo, existeMotor, getPrice, js_read,js_read2, js_save,js_save2, existeParte, getCart, submitCart, getSubModels
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

@app.route("/palomino", methods=['POST','GET'])
def palomitas():
    valor=request.args
    print("sirvee")
    print(valor)
    return "jeje"


@app.route("/sms", methods=['POST'])
def wazza():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    dic=js_read2()
    if("siguiente" not in dic):
        dic["siguiente"]="saludo"
    siguiente=dic["siguiente"]
    print("dicc")
    print(dic)
    print("---")

    if(siguiente=="saludo"):
        toSend="Hola! ¿En que te puedo ayudar?"
        dic["siguiente"]="conseguir_datos"
    elif(siguiente=="conseguir_datos"):
        toSend="¿Cual es el nombre de tu empresa?"
        resp.message("{}".format(toSend))
        toSend="Claro, solo tienes que contestar unas preguntas"
        dic["siguiente"]="nombreEmpresa"
    elif(siguiente=="nombreEmpresa"):
        dic["empresa"]=msg
        toSend="Okay. ¿Cuantos puntos de buro tiene?"
        dic["siguiente"]="puntosBuro"
    elif(siguiente=="puntosBuro"):
        dic["puntosBuro"]=msg
        toSend="Bien. ¿Cuanto spuntos del SAT tiene?"
        dic["siguiente"]="puntosSat"
    elif(siguiente=="puntosSat"):
        dic["puntosSat"]=msg
        toSend="Excelete. ¿Cual es tu ingreso mensual?"
        dic["siguiente"]="ingresoMensual"
    elif(siguiente=="ingresoMensual"):
        dic["ingresoMensual"]=msg
        toSend="¿Cual es el monto deseado?"
        dic["siguiente"]="montoDeseado"
    elif(siguiente=="montoDeseado"):
        dic["montoDeseado"]=msg
        toSend="Y finalmente, ¿A que plazo te gustaria tu credito?"
        dic["siguiente"]="plazoDeseado"
    elif(siguiente=="plazoDeseado"):
        dic["plazoDeseado"]=msg
        toSend="Analizando datos..."
        resp.message("{}".format(toSend))
        toSend="ANALIZADO wii..."
        resp.message("{}".format(toSend))
        toSend=json.dumps(dic)
    js_save2(dic)
    print("saved")
    print(dic)
    print("--")
    resp.message("{}".format(toSend))
    return str(resp)

@app.route("/messenger", methods=['POST'])
def wazza2():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    dic=js_read2()
    if("siguiente" not in dic):
        dic["siguiente"]="saludo"
    siguiente=dic["siguiente"]
    print("dicc")
    print(dic)
    print("---")

    if(siguiente=="saludo"):
        toSend="Hola! ¿En que te puedo ayudar?"
        dic["siguiente"]="conseguir_datos"
    elif(siguiente=="conseguir_datos"):
        toSend="¿Cual es el nombre de tu empresa?"
        resp.message("{}".format(toSend))
        toSend="Claro, solo tienes que contestar unas preguntas"
        dic["siguiente"]="nombreEmpresa"
    elif(siguiente=="nombreEmpresa"):
        dic["empresa"]=msg
        toSend="Okay. ¿Cuantos puntos de buro tiene?"
        dic["siguiente"]="puntosBuro"
    elif(siguiente=="puntosBuro"):
        dic["puntosBuro"]=msg
        toSend="Bien. ¿Cuanto spuntos del SAT tiene?"
        dic["siguiente"]="puntosSat"
    elif(siguiente=="puntosSat"):
        dic["puntosSat"]=msg
        toSend="Excelete. ¿Cual es tu ingreso mensual?"
        dic["siguiente"]="ingresoMensual"
    elif(siguiente=="ingresoMensual"):
        dic["ingresoMensual"]=msg
        toSend="¿Cual es el monto deseado?"
        dic["siguiente"]="montoDeseado"
    elif(siguiente=="montoDeseado"):
        dic["montoDeseado"]=msg
        toSend="Y finalmente, ¿A que plazo te gustaria tu credito?"
        dic["siguiente"]="plazoDeseado"
    elif(siguiente=="plazoDeseado"):
        dic["plazoDeseado"]=msg
        toSend="Analizando datos..."
        resp.message("{}".format(toSend))
        toSend="ANALIZADO wii..."
        resp.message("{}".format(toSend))
        toSend=json.dumps(dic)
    js_save2(dic)
    print("saved")
    print(dic)
    print("--")
    resp.message("{}".format(toSend))
    return str(resp)

@app.route("/sms2", methods=['POST'])
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
        #with resp.message() as message:
        #        message.media('https://demo.twilio.com/owl.png')
    elif(str(toSend)=="decision.pt"):
        toSend="What is the branch of the car?"
        dicInfo[user]={"prove":False, "next":"marca"}
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
    elif(str(toSend)=="decision.prove"):
        dicInfo[user]={"prove":True, "next":"marca"}
        toSend="What is the branch of the car?"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
    elif(str(toSend)=="marca"):
        res=existeMarca(msg.lower())
        if(res[1]==None):
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
        else:  #modified this
            res=dicInfo[user]
            res["modelo"]=info[0]
            res["modeloId"]=info[1]
            res["next"]="modelo.sub"
            toSend="Cool. What is the submodel of the car?\n"
            submodelos=getSubModels(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"])
            opciones=[]
            counter=1
            string="Options \n"
            for submodelo in submodelos:
                string+=str(counter)+ "-  "+submodelo["submodelName"] +" \n"
                temp={"number":counter, "name":submodelo["submodelName"]}
                opciones.append(temp)
                counter+=1
            toSend+=string
            res["submodelos"]=opciones
            dicInfo[user]=res
    elif(str(toSend)=="modelo.sub"):
        modelossub=dicInfo[user]["submodelos"]
        modelo=""
        for element in modelossub:
            if(str(element["number"])==str(msg)):
                modelo=element["name"]
                break
        print("modelo")
        print(modelo)

        info=existeSubmodelo(modelo.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"])
        print(info)
        #if(info==None):
        #    toSend="We didn't find that submodel in our database. Try with another one"            
        #else: 
        res=dicInfo[user]
        res["submodelo"]=info[0]
        res["submodeloId"]=info[1]
        res["next"]="motor"
        toSend="Almost done. What is the name of the engine? \n"
        #jejediego
        opciones=[]
        counter=1
        string="Options \n"
        
        result=getEngines(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], info[1])
        print("result")
        print(result)
        print("res")
        print(res)
        for engine in result:
            string+=str(counter)+ "-  "+engine["engineName"] +" \n"
            temp={"number":counter, "name":engine["engineName"]}
            opciones.append(temp)
            counter+=1
        toSend+=string
        res["engines"]=opciones
        dicInfo[user]=res
    elif(str(toSend)=="motor"):
        modelossub=dicInfo[user]["engines"]
        modelo=""
        for element in modelossub:
            if(str(element["number"])==str(msg)):
                modelo=element["name"]
                break
        info=existeMotor(modelo.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"])
        
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
        print("------")
        print(dicInfo)
    elif(str(toSend)=="part"): #the part i want is the -..-.-.
        part=existeParte(msg.lower())
        if(part==None):
            toSend="We didn't find that part in our database. Try with another one"            
        else: 
            price= getPrice(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"], dicInfo[user]["engineId"], dicInfo[user]["engine"]["engineParams"], part)
            idPart=price[0]
            urlImage=price[2]
            price=price[3]

            toSend="Your product "+ part + ":" 
            resp.message("{}".format(toSend))

            with resp.message() as message:
                message.media(urlImage)
                    
            res=dicInfo[user]
            res["partId"]=idPart
            res["partPrice"]=price
            res["partName"]=part
            prove=dicInfo[user]["prove"]
            if(prove):
                toSend="Tell me how many pieces do you want"
                res["next"]="pieces"
            else:    
                #toSend="The "+ part +" costs: "+ str(price) 
                #resp.message("{}".format(toSend))
                #time.sleep(2)
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
        toSend="Contacting..."
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
        #subir todo a carrito
        #{partId, quantity}
        lista=[]
        for element in comprar:
            total+=int(element[2])
            toSend="Product: " + element[1] +"   Price: $"
            resp.message("{}".format(toSend))
            temp={"partId":dicInfo[user]["partId"], "quantity":1}
            lista.append(temp)
        sessionId=submitCart("beta_bosch", lista)
        print("wuu tengo el session id "+ str(sessionId))
        price=getCart(sessionId)
        print("wuu tengo el price")
        toSend="Your total is: " + str("$")
        resp.message("{}".format(toSend))
        toSend="Do you want to pay with whatsapp payments or via bank deposit?"
    elif(str(toSend)=="bankdeposit"):
        toSend = "Great. Here you have the bank details"
        resp.message("{}".format(toSend))
        """
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend = "Bank Account: XXXXXXXXXXXXXXXXXXXXXXX"
        resp.message("{}".format(toSend))
        time.sleep(2)
        toSend = "Reference: XXXX"
        resp.message("{}".format(toSend))
        """
        with resp.message() as message:
            message.media('https://www.usunlocked.com/wp-content/uploads/2016/07/Bank_Transfer_Step4-750x349.png')
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

@app.route("/messenger2", methods=['POST'])
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
        toSend="What is the branch of the car?"
        dicInfo[user]={"prove":False, "next":"marca"}
        resp.message("{}".format(toSend))
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
    elif(str(toSend)=="decision.prove"):
        dicInfo[user]={"prove":True, "next":"marca"}
        toSend="What is the branch of the car?"
        resp.message("{}".format(toSend))
        toSend="Excelent. I'm going to ask you some questions about what you are looking for."
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
        else:  #modified this
            res=dicInfo[user]
            res["modelo"]=info[0]
            res["modeloId"]=info[1]
            res["next"]="modelo.sub"
            toSend="Cool. What is the submodel of the car?\n"
            submodelos=getSubModels(dicInfo[user]["year"], dicInfo[user]["marcaId"], info[1])
            opciones=[]
            counter=1
            string="Options \n"
            print("submodelos")
            print(submodelos)
            print("-----------------")

            for submodelo in submodelos:
                string+=str(counter)+ "-  "+submodelo["submodelName"] +" \n"
                temp={"number":counter, "name":submodelo["submodelName"]}
                opciones.append(temp)
                counter+=1
            toSend+=string
            res["submodelos"]=opciones
            dicInfo[user]=res
    elif(str(toSend)=="modelo.sub"):
        modelossub=dicInfo[user]["submodelos"]
        modelo=""
        for element in modelossub:
            if(str(element["number"])==str(msg)):
                modelo=element["name"]
                break
        print("modelo")
        print(modelo)

        info=existeSubmodelo(modelo.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"])
        print(info)
        #if(info==None):
        #    toSend="We didn't find that submodel in our database. Try with another one"            
        #else: 
        res=dicInfo[user]
        res["submodelo"]=info[0]
        res["submodeloId"]=info[1]
        res["next"]="motor"
        toSend="Almost done. What is the name of the engine? \n"
        #jejediego
        opciones=[]
        counter=1
        string="Options \n"
        
        result=getEngines(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], info[1])
        print("result")
        print(result)
        print("res")
        print(res)
        for engine in result:
            string+=str(counter)+ "-  "+engine["engineName"] +" \n"
            temp={"number":counter, "name":engine["engineName"]}
            opciones.append(temp)
            counter+=1
        toSend+=string
        res["engines"]=opciones
        dicInfo[user]=res
    elif(str(toSend)=="motor"):
        modelossub=dicInfo[user]["engines"]
        modelo=""
        for element in modelossub:
            if(str(element["number"])==str(msg)):
                modelo=element["name"]
                break
        info=existeMotor(modelo.lower(), dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"])
        
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
        print("------")
        print(dicInfo)
    elif(str(toSend)=="part"): #the part i want is the -..-.-.
        part=existeParte(msg.lower())
        if(part==None):
            toSend="We didn't find that part in our database. Try with another one"            
        else: 
            price= getPrice(dicInfo[user]["year"], dicInfo[user]["marcaId"], dicInfo[user]["modeloId"], dicInfo[user]["submodeloId"], dicInfo[user]["engineId"], dicInfo[user]["engine"]["engineParams"], part)
            print("priceeee")
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
            print("--------aaaaaa")
            print(dicInfo)

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
        toSend="Contacting..."
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
        print("before checkout")
        print(dicInfo)

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
        #subir todo a carrito
        #{partId, quantity}
        lista=[]
        for element in comprar:
            total+=int(element[2])
            toSend="Product: " + element[1] +"   Price: " + str("$")
            resp.message("{}".format(toSend))
            temp={"partId":dicInfo[user]["partId"], "quantity":1}
            lista.append(temp)
        sessionId=submitCart("beta_bosch", lista)
        print("wuu tengo el session id "+ str(sessionId))
        price=getCart(sessionId)
        print("wuu tengo el price")
        toSend="Your total is: " + str("$")
        resp.message("{}".format(toSend))
        toSend="Do you want to pay with messenger payments or via bank deposit?"
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