from rasa_nlu.model import Interpreter
import json

interpreter = Interpreter.load("./models/current/nlu")

def getIntent(message):
    #message = "quiero saber de PartsTech"
    result = interpreter.parse(message)
    print(json.dumps(result, indent=2))


getIntent("quiero saber de PartsTech")