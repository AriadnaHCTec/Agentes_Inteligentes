#!/usr/bin/env python
# coding: utf-8

# In[1]:


from mesa import Agent, Model, model
from mesa.time import RandomActivation
from mesa.space import Grid, SingleGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random


# In[2]:


# "Constantes"
N = 32                               #Dimensión de la cuadrícula
LARGO_CALLE = 12                     #en casillas
ANCHO_CALLE = 2                      #en casillas
L_INTER = 8                          #dimensión de la intersección en casillas
POS_INTER = (12,12)                  #esquina inferior izquirda de la intersección (x,y)
POS_CALLES = [(0, 13), (31, 18), (18, 0), (13,31)]  #Posición (x,y) del inicio del primer carril, por sentido
POS_VUELTA = {"0-D": (13, 13), "0-I": (17,14), "1-D": (18,18), "1-I": (14,17),
             "2-D": (18, 13), "2-I": (17,17), "3-D": (13,18), "3-I": (14,14)}
POS_SF = {"S0": (20, 12), "S1": (11,19), "S2": (19,20), "S3": (12,11)}
TIEMPO_MAXIMO = 60                   #en steps


# In[3]:


class CarAgent(Agent):
    """ Modelo para un auto """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        random.seed()
        self.direccion = 0 #Frente 0, Derecha 1, Izquierda 2, Atras 3
        self.sentido = 0 #Derecha 0, Izquierda 1, Arriba 2, Abajo 3
        self.futuro_sentido = 0 #La acción que tomará al cruzar la primera línea del cruce
        #El sentido toma en consideracion que las columnas crecen a la derecha y los renglones
        # crecen hacia arriba

    def isFreeMyDirection(self,listFreeSpaces,list_possible_steps):
        if (self.sentido == 0): #Derecha
            if(self.direccion == 0): #Frente
                return listFreeSpaces[7],list_possible_steps[7]
            elif (self.direccion == 1): #Derecha
                return listFreeSpaces[6],list_possible_steps[6]
            elif(self.direccion == 2): #Izquierda
                return listFreeSpaces[8],list_possible_steps[8]
            elif(self.direccion == 3): #Atras
                return listFreeSpaces[1],list_possible_steps[1]
            else:
                print("Error en self.direccion")
                return False,(-1,-1)
        elif (self.sentido == 1): #Izquierda
            if(self.direccion == 0): #Frente
                return listFreeSpaces[1],list_possible_steps[1]
            elif (self.direccion == 1): #Derecha
                return listFreeSpaces[2],list_possible_steps[2]
            elif(self.direccion == 2): #Izquierda
                return listFreeSpaces[0],list_possible_steps[0]
            elif(self.direccion == 3): #Atras
                return listFreeSpaces[7],list_possible_steps[7]
            else:
                print("Error en self.direccion")
                return False,(-1,-1)
        elif (self.sentido == 2): #Arriba
            if(self.direccion == 0): #Frente
                return listFreeSpaces[5],list_possible_steps[5]
            elif (self.direccion == 1): #Derecha
                return listFreeSpaces[8],list_possible_steps[8]
            elif(self.direccion == 2): #Izquierda
                return listFreeSpaces[2],list_possible_steps[2]
            elif(self.direccion == 3): #Atras
                return listFreeSpaces[3],list_possible_steps[3]
            else:
                print("Error en self.direccion")
                return False,(-1,-1)
        elif (self.sentido == 3): #Abajo
            if(self.direccion == 0): #Frente
                return listFreeSpaces[3],list_possible_steps[3]
            elif (self.direccion == 1): #Derecha
                return listFreeSpaces[0],list_possible_steps[0]
            elif(self.direccion == 2): #Izquierda
                return listFreeSpaces[6],list_possible_steps[6]
            elif(self.direccion == 3): #Atras
                return listFreeSpaces[5],list_possible_steps[5]
            else:
                print("Error en self.direccion")
                return False,(-1,-1)
        else:
            print("Error en self.sentido")
            return False,(-1,-1)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, #8 conectado. Orden: arriba izquierda, centro, derecha; enmedio izquierda y derecha; abajo izquierda, centro, derecha
            include_center=True) #incluye su posición
        print(possible_steps)
        myPosition = possible_steps[4]

        #Verificar cuales espacios a mi alrededor están ocupados
        freeSpaces = []
        for pos in possible_steps:
            freeSpaces.append(self.model.grid.is_cell_empty(pos))
        print(freeSpaces)
        
        #Cambiar de sentido si está en la casilla indicada
        if self.sentido != self.futuro_sentido:
            if self.sentido == 0:    #Derecha                             
                if (self.futuro_sentido == 3 and self.pos == POS_VUELTA["0-D"]) or self.pos == POS_VUELTA["0-I"]:
                    self.sentido = self.futuro_sentido
            elif self.sentido == 1:  #Izquierda
                if (self.futuro_sentido == 2 and self.pos == POS_VUELTA["1-D"]) or self.pos == POS_VUELTA["1-I"]:
                    self.sentido = self.futuro_sentido
            elif self.sentido == 2:  #Arriba
                if (self.futuro_sentido == 0 and self.pos == POS_VUELTA["2-D"]) or self.pos == POS_VUELTA["2-I"]:
                    self.sentido = self.futuro_sentido
            elif self.sentido == 3:  #Abajo
                if (self.futuro_sentido == 1 and self.pos == POS_VUELTA["3-D"]) or self.pos == POS_VUELTA["3-I"]:
                    self.sentido = self.futuro_sentido
            else:
                print("Sentido inválido.")
                    
        #Movimiento tomando en consideración la dirección y si está libre ese espacio
        free,newPos = self.isFreeMyDirection(freeSpaces,possible_steps)
        if free:
            self.model.grid.move_agent(self,newPos)
            print(f"Se mueve de {myPosition} a {newPos} porque va hacia {self.direccion}\n")
        else:
            print("wat")
            """
            print(f"No se puede mover en sentido {self.sentido}, ubicación ocupada.")
            nuevoSentido = random.randint(0,3)
            while (nuevoSentido == self.sentido):
                nuevoSentido = random.randint(0,3)
            self.sentido = nuevoSentido
            print(f"Cambiando sentido a {self.sentido}\n")
            """
            
    def step(self):
        """ En cada paso moverse aleatoriamente
        self.direccion = random.randint(0,3)
        print(f"Agente: {self.unique_id} movimiento {self.direccion}")
        self.move()
        """
        #if (self.pos[0] == 0 or self.pos[0] == N - 1 or self.pos[1] == 0 or self.pos[1] == N - 1):
            #self.model.grid._remove_agent(self.pos, self)
            #self.model.schedule.remove(self)
            #pass
        #else:
        if self.sentido == 0:
            if self.pos[0] < LARGO_CALLE - 1: 
                self.move()
            elif self.pos[0] == LARGO_CALLE - 1:
                if TrafficLightMaster.fases[0] > 0:
                    self.move()
            else:
                self.move()
        elif self.sentido == 1:
            if self.pos[0] > N - LARGO_CALLE: 
                self.move()
            elif self.pos[0] == N - LARGO_CALLE:
                if TrafficLightMaster.fases[1] > 0:
                    self.move()
            else:
                self.move()
        elif self.sentido == 2:
            if self.pos[1] < LARGO_CALLE - 1: 
                self.move()
            elif self.pos[1] == LARGO_CALLE - 1:
                if TrafficLightMaster.fases[2] > 0:
                    self.move()
            else:
                self.move()
        elif self.sentido == 3:
            if self.pos[1] > N - LARGO_CALLE: 
                self.move()
            elif self.pos[1] == N - LARGO_CALLE:
                if TrafficLightMaster.fases[3] > 0:
                    self.move()
            else:
                self.move()


# In[4]:


class TrafficLightMaster():
    sentido_actual = 0
    fases = [0, 0, 0, 0]                          #Fases por semáforo (los indices son iguales que el sentido)
    t_fase = -1                                   #Tiempo restante del semáforo en turno
    flujos = [0, 0, 0, 0]                         #Cantidad de carros por sentido (los indices son iguales que el sentido)
    
    @classmethod
    def cambiarTurno(cls):
        cls.sentido_actual = (cls.sentido_actual + 1) % 4
        print("Turno actual: " + str(cls.sentido_actual))
        
    @classmethod
    def calcularDuracion(cls, N):
        cls.t_fase = int(N / LARGO_CALLE * TIEMPO_MAXIMO) - 1


# In[5]:


class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, sentido):
        super().__init__(unique_id, model)
        self.fase = 0                            # 0 = rojo, 1 = amarillo, 2 = verde
        self.sentido = sentido
        self.cont = 0
        
    def obtenerFlujo(self, sentido):
        cont = 0
        if sentido == 0:                       #Derecha
            for i in range(LARGO_CALLE):
                for j in range(ANCHO_CALLE):
                    cont += int(not self.model.grid.is_cell_empty((i, POS_CALLES[0][1] + j)))
                
        elif sentido == 1:                     #Izquierda
            for i in range(LARGO_CALLE):
                for j in range(ANCHO_CALLE):
                    cont += int(not self.model.grid.is_cell_empty((POS_CALLES[1][0] - i, POS_CALLES[1][1] - j)))
                    
        elif sentido == 2:                     #Arriba
            for i in range(ANCHO_CALLE):
                for j in range(LARGO_CALLE):
                    cont += int(not self.model.grid.is_cell_empty((POS_CALLES[2][0] - i, j)))
                    
        elif sentido == 3:                     #Abajo
            for i in range(ANCHO_CALLE):
                for j in range(LARGO_CALLE):
                    cont += int(not self.model.grid.is_cell_empty((POS_CALLES[3][0] + i, POS_CALLES[3][1] - j)))
        else:
            print("Sentido inválido")
            
        TrafficLightMaster.flujos[sentido] = cont
        
    def isInterVacia(self):
        for i in range(POS_INTER[0], POS_INTER[0] + L_INTER):
            for j in range(POS_INTER[1], POS_INTER[1] + L_INTER):
                if not self.model.grid.is_cell_empty((i, j)):
                    print("Celda: " + str(i) + " , " + str(j) + " no esta vacia.") 
                    return False
        
        return True
    
    def step(self):
        if self.sentido == TrafficLightMaster.sentido_actual:
            if TrafficLightMaster.t_fase > 0:
                self.fase = 2
                TrafficLightMaster.fases[self.sentido] = 2
                TrafficLightMaster.t_fase -=1
            elif TrafficLightMaster.t_fase == 0:
                self.fase = 1
                TrafficLightMaster.fases[self.sentido] = 1
                TrafficLightMaster.t_fase -=1
            else:
                self.fase = 0
                TrafficLightMaster.fases[self.sentido] = 0
                if self.isInterVacia():
                    TrafficLightMaster.cambiarTurno()
                    self.obtenerFlujo(TrafficLightMaster.sentido_actual)
                    print("Flujo: " + str(TrafficLightMaster.flujos[TrafficLightMaster.sentido_actual]))
                    TrafficLightMaster.calcularDuracion(TrafficLightMaster.flujos[TrafficLightMaster.sentido_actual])
                    


# In[6]:


class ObstacleAgent(Agent):
    """ Modelo para un Obstaculo """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # The agent's step will go here.
        pass  


# In[7]:


class TraficModel(Model):
    """ Modelo para los autos """
    def __init__(self, N,ancho,alto):
        self.num_agents = N
        self.grid = SingleGrid(ancho,alto,True) #NO Es Toroidal
        self.schedule = RandomActivation(self)
        self.running = True #Para la visualizacion
        listaPosLimite = []
        calleAlto = 12
        calleAncho = 12
        posx = [0 , 0, ancho-calleAncho, ancho-calleAncho]
        posy = [0, alto-calleAlto, 0,alto-calleAlto]
        index = 0
        for ii in range(4):
            ix = posx[ii]
            iy = posy[ii]
            for i in range(calleAlto):
                for j in range(calleAncho):
                    a = ObstacleAgent(index, self)
                    index+=1
                    self.schedule.add(a)
                    self.grid.place_agent(a, (ix+i,iy+j))
        #Añadir semáforos
        s0 = TrafficLightAgent(2000, self, 0)
        s1 = TrafficLightAgent(2001, self, 1)
        s2 = TrafficLightAgent(2002, self, 2)
        s3 = TrafficLightAgent(2003, self, 3)
        self.schedule.add(s0)
        self.schedule.add(s1)
        self.schedule.add(s2)
        self.schedule.add(s3)
        self.grid.place_agent(s0 ,POS_SF["S0"])
        self.grid.place_agent(s1 ,POS_SF["S1"])
        self.grid.place_agent(s2 ,POS_SF["S2"])
        self.grid.place_agent(s3 ,POS_SF["S3"])
        #Inician hacia la derecha
        #"""
        a = CarAgent(1000, self)
        b = CarAgent(1001, self)
        a.futuro_sentido = 3
        b.futuro_sentido = 2
        self.schedule.add(a)
        self.schedule.add(b)
        self.grid.place_agent(a ,(1,13))
        self.grid.place_agent(b ,(1,14))
        #"""
        #Inician hacia arriba
        a = CarAgent(1002, self)
        a.sentido = 2
        a.futuro_sentido = 0
        self.schedule.add(a)
        self.grid.place_agent(a ,(18,1))
        #Inician hacia abajo
        #"""
        a = CarAgent(1003, self)
        a.sentido = 3
        a.futuro_sentido = 1
        self.schedule.add(a)
        self.grid.place_agent(a ,(13,30))
        #"""
        #Inician hacia la izquierda
        #"""
        a = CarAgent(1004, self)
        a.sentido = 1
        a.futuro_sentido = 2
        self.schedule.add(a)
        self.grid.place_agent(a ,(30,18))


        a = CarAgent(1005, self)
        a.sentido = 1
        a.futuro_sentido = 2
        self.schedule.add(a)
        self.grid.place_agent(a ,(30,17))


        a = CarAgent(1006, self)
        a.sentido = 1
        a.futuro_sentido = 2
        self.schedule.add(a)
        self.grid.place_agent(a ,(29,17))
        #"""
        #Crear obstaculos en los limites del grid
        """numObs = (ancho * 2) + (alto * 2 - 4)
        listaPosLimite = []
        #Las dos columnas límite
        for col in [0,ancho-1]:
            for ren in range(alto):
                listaPosLimite.append((col,ren))
        #Los dos renglones limite
        for col in range(1,ancho-1):
            for ren in [0,alto-1]:
                listaPosLimite.append((col,ren))
        print(listaPosLimite)
        """
        """for i in range(numObs):
            a = ObstacleAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])"""

        # Create car agents
        """for i in range(self.num_agents):
            a = CarAgent(i+1000, self) #La numeracion de los agentes empieza en el 1000
            self.schedule.add(a)
            # Add the agent to a random empty grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (not self.grid.is_cell_empty((x,y))):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))"""

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
