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

def js_r(filename):
   with open(filename) as f_in:
       return(json.load(f_in))

def js_save(dictionary):
    with open('data/data.json', 'w') as fp:
        json.dump(dictionary, fp)

def crear():
    data = js_r("data/response.json")
    dic={}
    for marca in data:
        validYears=[]
        yearDic={}
        for year in range(2010,2019):
            modelos=getModels(year, marca["makeId"])
            if len(modelos)==0:
                continue

            dic[marca["makeName"]]={"years": [], "modelos":{}}
            validYears.append(year)
            modelosDic={}
            
            for modelo in modelos:
                modeloDic={}

                submodelos=getSubModels(year, marca["makeId"], modelo["modelId"])
                if len(submodelos)==0:
                    continue
                subModelosDic={}
                for submodelo in submodelos:                    
                    engines=getEngines(year, marca["makeId"], modelo["modelId"], submodelo["submodelId"])
                    if(len(engines)==0):
                        continue
                    enginesDic={}
                    for engine in engines:
                        enginesDic[engine["engineName"]]={"info":engine}
                    subModelosDic[submodelo["submodelName"]]={"info": submodelo, "engines":enginesDic}
                modeloDic={"info": modelo, "submodelos": subModelosDic}
                modelosDic[modelo["modelName"]]=modeloDic           
                print("sub modelo terminado "+ str(modelo["modelName"]))
            yearDic[str(year)]=modelosDic
        print("Done marca: " + str(marca["makeName"]) + "  & year: " +str(yearDic))
        dic[marca["makeName"]]=yearDic
    js_save(dic)
    return True


"""
dic={
    marca:{
        year{
            modelos:{
                modeloName:{  modelosDic
                    info:{
                        info del modelo
                    },
                    subModelos:{ subModelosDic ya sta
                        A21:{
                            info:{
                                info del modelo
                            },
                            engines:{
                                AA1:{
                                    info:{
                                        info del engine
                                    }
                                },
                            }
                        },
                    }
                },
            }
        }
    }
}
"""
res=crear()
print(res)

#print(getModels(1990,21)) #una lista de los modelos de cada linea de carros
