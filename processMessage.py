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
"""

def getInfo(intentName):
    if(intentName=="saludos"):
        mensaje="Hola! Te puedo ayudar a comprar/cotizar autopartes con proveedores externos o con nuestro aliado PartsTech. ¿Con quien te gustaria?"
        return mensaje