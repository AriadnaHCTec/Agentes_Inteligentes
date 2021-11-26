# -*- coding: utf-8 -*-
"""
Modelos de Agente y del medio ambiente
Version 2 - Movimiento aleatorio del auto en el grid

Solución al reto de TC2008B semestre AgostoDiciembre 2021
Autor: Jorge Ramírez Uresti
"""

from mesa import Agent, Model, model
from mesa.time import RandomActivation
from mesa.space import Grid, SingleGrid
import random



class CarAgent(Agent):
    """ Modelo para un auto """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        random.seed()
        self.direccion = 0 #Frente 0, Derecha 1, Izquierda 2, Atras 3
        self.sentido = 3 #Derecha 0, Izquierda 1, Arriba 2, Abajo 3
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

        #Movimiento tomando en consideración la dirección y si está libre ese espacio
        free,newPos = self.isFreeMyDirection(freeSpaces,possible_steps)
        if free:
            self.model.grid.move_agent(self,newPos)
            print(f"Se mueve de {myPosition} a {newPos} porque va hacia {self.direccion}\n")
        else:
            print(f"No se puede mover en sentido {self.sentido}, ubicación ocupada.")
            nuevoSentido = random.randint(0,3)
            while (nuevoSentido == self.sentido):
                nuevoSentido = random.randint(0,3)
            self.sentido = nuevoSentido
            print(f"Cambiando sentido a {self.sentido}\n")

    def step(self):
        """ En cada paso moverse aleatoriamente """
        self.direccion = random.randint(0,3)
        print(f"Agente: {self.unique_id} movimiento {self.direccion}")
        self.move()

# $$$
class TrafficLightsAgent(Agent):
    """Modelo para un semáforo"""
    """Sólo van a existir 2 semáforos"""
    """Semáforo 1: Carril Horizontal
       Semáfoto 2: Carril Vertical"""
    """Estado
       0 = Rojo
       1 = Amarillo
       2 = Verde"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.estado = 0

    def contarCarros(self, idSemaforo):
        """Opcion: True -> verificar solo las casillas del semáforo actual
           Opcion: False -> verificar las casillas de ambos"""
        """Coordenadas primero avanza x y luego y"""
        if(self.unique_id == idSemaforo):
            for i in range(12,20):
                for j in range(12):
                    cellmate = self.model.grid.get_cell_list_contents((i,j))
                    if(cellmate != []):
                        if type(cellmate[0]) is CarAgent:
                            self.model.contSemaforo1+=1
                            print("carro gg en semaforo 1")
            print("contSemaforo1=",self.model.contSemaforo1)
        else:
            for i in range(12):
                for j in range(12,20):
                    cellmate = self.model.grid.get_cell_list_contents((i,j))
                    if(cellmate != []):
                        if type(cellmate[0]) is CarAgent:
                            self.model.contSemaforo2+=1
                            print("carro gg en semaforo 2")
            print("contSemaforo2=",self.model.contSemaforo2)

    def cambiarEstado(self, semaforoVerde):
        """Se le puede agregar un parametro que se haga valido cuando ya vaya a cambiar a rojo
           y que se cambie el color a amarillo"""
        if semaforoVerde == 3001:
            print("Semaforo 1 esta en verde")
            print("Semaforo 2 esta rojo")
            self.luzSemaforo1 = 0
            self.luzSemaforo2 = 2
        else:
            print("Semaforo 1 esta en rojo")
            print("Semaforo 2 esta en verde")
            self.luzSemaforo1 = 2
            self.luzSemaforo2 = 0

    def calcularPrioridad(self):
        self.contarCarros(3001)
        self.contarCarros(3002)
        cont_s1 = self.model.contSemaforo1
        cont_s2 = self.model.contSemaforo2
        if cont_s1 > 0 and cont_s2 > 0:
            maxValue = max(cont_s1,cont_s2)
            if maxValue == cont_s1:
                self.model.prioridadSemaforo1 = cont_s1 + 6 #dar tiempo (steps) del numero del carro más 6
                self.model.controlPrioridad = 3001
                #self.model.prioridadSemaforo2 = 0
            else:
                #self.model.prioridadSemaforo1 = 0
                self.model.prioridadSemaforo2 = cont_s2 + 6 #dar tiempo (steps) del numero del carro más 6
                self.model.controlPrioridad = 3002

        elif cont_s1 > 0 and cont_s2 == 0:
            self.model.prioridadSemaforo1 = cont_s1 + 6 #dar tiempo (steps) del numero del carro más 6
            self.model.controlPrioridad = 3001

        elif cont_s1 == 0 and cont_s2 > 0:
            self.model.prioridadSemaforo2 = cont_s2 + 6 #dar tiempo (steps) del numero del carro más 6
            self.model.controlPrioridad = 3002

        else:
            if random.randint(3001,3002) == 3001:
                self.model.prioridadSemaforo1 = 4 #dar tiempo de 4
                self.model.controlPrioridad = 3001
            else:
                self.model.prioridadSemaforo2 = 4 #dar tiempo de 4
                self.model.controlPrioridad = 3002
            
    def checarPrioridad(self):
        if self.model.controlPrioridad == 3001:
            self.model.prioridadSemaforo1 -= 1
            self.cambiarEstado(3001)
            #return 3001, self.model.prioridadSemaforo1
        else:
            self.model.prioridadSemaforo2 -= 1
            self.cambiarEstado(3002)
            #return 3002, self.model.prioridadSemaforo2
        
    def move(self):
        if self.model.controlPrioridad == 3001:
            if self.model.prioridadSemaforo1 == 0:
                self.calcularPrioridad()
            else:
                self.checarPrioridad()
        else:
            if self.model.prioridadSemaforo2 == 0:
                self.calcularPrioridad()
            else:
                self.checarPrioridad()

    def step(self):
        self.move()


class ObstacleAgent(Agent):
    """ Modelo para un Obstaculo """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # The agent's step will go here.
        pass  

class TraficModel(Model):
    """ Modelo para los autos """
    def __init__(self, N,ancho,alto):
        self.num_agents = N
        self.grid = SingleGrid(ancho,alto,False) #NO Es Toroidal
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
                    #Eliminar obstaculos en las posiciones donde irán los semáforos
                    if(ix+i ==11 and iy+j==20 or ix+i ==20 and iy+j==11):
                        self.grid._remove_agent((ix+i,iy+j), a)

        #  $$$
        self.contSemaforo1 = 0
        self.contSemaforo2 = 0
        self.prioridadSemaforo1 = 1
        self.prioridadSemaforo2 = 1
        self.luzSemaforo1 = 0
        self.luzSemaforo2 = 2
        self.tiempo = 1
        self.controlPrioridad = 3001
        #Crear semáforos
        tlPos = [(20,11),(11,20)]
        for i,positionTL in enumerate(tlPos):
            trafficLights = TrafficLightsAgent(3000+i+1,self)
            self.schedule.add(trafficLights)
            self.grid.place_agent(trafficLights, positionTL)
            print("Semaforo",i,3000+1+i)

        a = CarAgent(8000, self)
        self.schedule.add(a)
        self.grid.place_agent(a, (10,14))

        b = CarAgent(8001, self)
        self.schedule.add(b)
        self.grid.place_agent(b, (10,15))
        # $$$

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
        self.contSemaforo1 = 0# $$$
        self.contSemaforo2 = 0#  $$$
        self.schedule.step()
