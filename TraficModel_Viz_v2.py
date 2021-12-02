"""
Visualización del Modelo de Trafico
Version 2 - Movimiento aleatorio del auto en el grid

Solución al reto de TC2008B semestre AgostoDiciembre 2021
Autor: Jorge Ramírez Uresti
"""

from TraficModel_v2 import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


# # Representación visual

# In[8]:


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}  

    if (isinstance(agent,ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    elif (isinstance(agent, CarAgent)):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.4
        portrayal["h"] = 0.4
    elif (isinstance(agent,TrafficLightAgent)):
        if agent.fase == 0: #Rojo
            portrayal["Color"] = "red"
        elif agent.fase == 1:
            portrayal["Color"] = "yellow"
        elif agent.fase == 2:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "black"
            print("Fased semáforo inválida.")
    return portrayal

grid = CanvasGrid(agent_portrayal, 32, 32, 500, 500)
server = ModularServer(TraficModel,
                       [grid],
                       "Trafic Model",
                       {"N":5, "ancho":32, "alto":32})
server.port = 8521 # The default
server.launch()