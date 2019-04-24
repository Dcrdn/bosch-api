#requests
import requests
import json
#make es mi linea de carro

auth={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiZXRhLnBhcnRzdGVjaC5jb20iLCJleHAiOjE1NTYzMTkxMzUsInBhcnRuZXIiOiJiZXRhX2Jvc2NoIiwidXNlciI6ImhhY2t0ZWFtXzYifQ.oWfmoSuKvmlVH_MwchNEo-qRRc3Hb9zxsPDG2_D3YS8"}
"""
mi archivo base tiene:
makeName	
makeId
"""


#requiere year & make
urlModel ="https://api.beta.partstech.com/taxonomy/vehicles/models" #estos son los modelos cada linea de carros
#regresa: modelName, modelId

#make & model 
urlYear = "https://api.beta.partstech.com/taxonomy/vehicles/years" #los years de los modelos de cada carro
#regresa: submodelName,submodelId

#requiere year & make & model
urlSubmodel="https://api.beta.partstech.com/taxonomy/vehicles/submodels"  #estos son los submodels de un modelo
#regresa: submodelName,submodelId

#year, make, model and submodel are required.
urlEngine="https://api.beta.partstech.com/taxonomy/vehicles/engines" #estos son los engines
#regresa: engineId, engineName, engineParams (objeto)

"""
"searchParams": {
"vehicleParams": {
"yearId": 2015,
"makeId": 65,
"modelId": 123,
"subModelId": 234,
"engineId": 12344,
"engineParams": {
"engineVinId": 134,
"engineDesignationId": 344,
"engineVersionId": 342,
"fuelTypeId": 54,
"cylinderHeadTypeId": 25243
}
},
"keyword": "Air Filter"
}

yearId, makeId, modelId, subModelId, engineParams: engineVinId,
"""
urlGetPrice="https://api.beta.partstech.com/catalog/search" 
# devuelve parts, filets

def getModels(year, marcaId):
    parametros={"year":year,"make":marcaId}
    r=requests.get(urlModel, headers=auth, params=parametros)
    return r.json() #devuelve una lista de los modelos de la linea de carros
    #if len()!=0 si tengo algo chido

def getSubModels(year, marcaId, modelId):
    parametros={"year":year,"make":marcaId, "model":modelId}
    r=requests.get(urlSubmodel, headers=auth, params=parametros)
    return r.json() #devuelve una lista de los submodelos de un modelo de carros

def getEngines(year, marcaId, modelId, submodelId):
    parametros={"year":year,"make":marcaId, "model":modelId, "submodel":submodelId}
    r=requests.get(urlEngine, headers=auth, params=parametros)
    return r.json() #devuelve una lista de los submodelos de un modelo de carros

def js_r():
   with open("data/response.json") as f_in:
       return(json.load(f_in))

def existeMarca(name):
    file=js_r()
    for marca in file:
        if(marca["makeName"].lower()==name):
            print("found")
            print(marca["makeName"])
            return [marca["makeName"], marca["makeId"]]
    return [None, None]

def existeModelo(modeloName, year, marcaId): #make id que recibi de marca
    result=getModels(year, marcaId)
    for modelo in result:
        if(modelo["modelName"].lower()==modeloName):
            print("found")
            print(modelo["modelName"])
            return [modelo["modelName"], modelo["modelId"]]
    return [None, None]

def existeSubmodelo(subModeloName, year, marcaId, modelId):
    result=getSubModels(year, marcaId, modelId)
    for submodelo in result:
        if(submodelo["submodelName"].lower()==subModeloName):
            print("found")
            print(submodelo["submodelName"])
            return [submodelo["submodelName"], submodelo["submodelId"]]
    return [None, None]

def existeMotor(motorName, year, marcaId, modelId, submodelId):
    result=getEngines(year, marcaId, modelId, submodelId)
    print(result)
    for engine in result:
        if(engine["engineName"].lower()==motorName):
            print("found")
            print(engine["engineName"])
            return [engine["engineName"], engine["engineId"], engine]
    return [None, None]

#yearId, makeId, modelId, subModelId, engineId, engineParams: engineVinId,

def getPrice(yearId, makeId, modelId, subModelId, engineId, engineParams, keyword):
    vehicle={"yearId":yearId, "makeId":makeId, "modelId":modelId, "subModelId":subModelId, "engineId":engineId, "engineParams":engineParams}
    parametros={"vehicleParams":vehicle,"keyword":keyword}
    parametros={"searchParams":parametros}
    print(parametros)
    r=requests.post(urlGetPrice, headers=auth, json=parametros)
    idPart=r.json()["parts"][0]["partId"]
    brand=r.json()["parts"][0]["brand"]["brandID"]
    url=r.json()["parts"][0]["images"][0]["preview"]
    precio=r.json()["parts"][0]["attributes"][0]["value"]
    print(keyword)
    print(idPart)
    print(brand)
    print(url)
    print(precio)
    return [idPart, brand, url, precio] #devuelve una lista de los modelos de la linea de carros

#sonata
data=existeMarca("Hyundai".lower())
data2=existeModelo("Elantra".lower(), 2016, data[1])
data3=existeSubmodelo("GL".lower(), 2016, data[1], data2[1])
data4=existeMotor("1.8L L4 vin E DOHC  ULEV".lower(), 2016, data[1], data2[1], data3[1])
print("----")
year=2016
idMarca=data[1]
idModelo=data2[1]
idSubmodelo=data3[1]
idEngine=data4[1]
engineParams=data4[2]["engineParams"]
result= getPrice(year, idMarca, idModelo, idSubmodelo, idEngine, engineParams, "Air Filter")