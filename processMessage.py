"""
saludos
despedidas
cotizar
infoB
decision.prove
decision.pt
marca
year
modelo
modelo.sub
motor
    if(toSend=="saludos"):
        toSend="Hola! Te puedo ayudar a comprar/cotizar autopartes con proveedores externos o con nuestro aliado PartsTech. ¿Con quien te gustaria?"
    else:
        toSend= "not possible"
    resp.message("HERE IS YOUR MESSAGE jeje: {}".format(toSend))
"""

def getInfo(intentName):
    if(intentName=="saludos"):
        mensaje="Hola! Te puedo ayudar a comprar/cotizar autopartes con proveedores externos o con nuestro aliado PartsTech. ¿Con quien te gustaria?"
        return mensaje
    return "no llego a nada"