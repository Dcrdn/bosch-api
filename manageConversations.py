from information import getModels

marcas=["BMW", "Hyundai", "Honda"]
years=["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]

def saludoInicial():
    return "Hi, I can help you to buy automobile pars. Would you like to work with our providers or with our partner PartsTech?"

def decitionPT():
    phrase1="Excelent. I'm going to ask you some questions about what you are looking for."
    phrase2="What is the branch of the car?"
    return phrase1,phrase2


def marca(oracion):
    oracion=oracion.split()
    for word in oracion:
        if word in marcas:
            return word
    return None

def getYear(oracion):
    oracion=oracion.split()
    for word in oracion:
        if word in years:
            return word
    return None

def getModelo(oracion, marcaId, year):
    results=getModels(year, marcaId):

def getModelo(oracion, year, marcaId):
    oracion=oracion.split()
    for pos in range(0,len(oracion)):
        oracion[pos]=oracion[pos].lower()
    result=getModels(year, marcaId)
    for modelo in result:
        if(modelo["modelName"].lower() in oracion):
            return [modelo["modelName"], modelo["modelId"]]
    return [None, None]