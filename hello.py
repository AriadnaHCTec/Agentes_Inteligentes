from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
#MESA
from TraficModel_v2 import *

model = TraficModel(1, 32, 32)

def updateTraffic(): 
    states = []
    for agent in model.schedule.agents:
        if isinstance(agent,CarAgent):
            states.append(agent.pos)
    model.step()
    return positions

def trafficToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "state" : p
        }
    posDICT.append(pos)    
    return json.dumps(posDICT)

anterior = (0,0)
def updatePositions(): 
    global anterior
    positions = []
    positions.append(anterior)
    for agent in model.schedule.agents:
        print(agent)
        if isinstance(agent,CarAgent):
            positions.append(agent.pos)    
            anterior = agent.pos
    model.step()
    return positions

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : float(p[0]),
            "z" : float(p[1]),
            "y" : float(0.0)
        }
    posDICT.append(pos)
    return json.dumps(posDICT)

app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


@app.route('/')
def root():
	global model
	model = TraficModel(1, 32, 32)
	return jsonify([{"message":"Hello World from IBM Cloud!"}])

@app.route('/updatePositions')
def upPositions():	
    return positionsToJSON(updatePositions())

@app.route('/trafficLight')
def upTraffic():  
    return positionsToJSON(updatePositions())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)