# M1. Actividad (Coches Modificada)

#Alumnos
#Román Mauricio Elias Valencia - a01656603@tec.mx
#Raúl Armando Vélez Robles - a01782488@tec.mx

#Profesor
#Oscar Francisco Fuentes Casarrubias - ofc1227@tec.mx

import mesa
import random

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

# Agente camino: por aquí pueden pasar autos
class Path(mesa.Agent):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)

# Agente obstaculo: al encontrarse el agente aunto con este se realizara un choque 
class Obstacle(mesa.Agent):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)

# Agente auto: Este es el agente principal en movimiento de la simulación
class Car(mesa.Agent):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.hasCollided = False
        self.counter = 1
        self.speedReduction = 1
        self.movements = 0

    # Verificamos si la posición está dentro de los límites de la cuadrícula y no está ocupada por un obstáculo
    def isPositionValid(self, position):
        x, y = position
        if 0 <= x < self.model.gridWidth and 0 <= y < self.model.gridHeight:
            cellContents = self.model.grid.get_cell_list_contents([(x, y)])
            for agent in cellContents:
                if isinstance(agent, Obstacle):
                    return random.random() < 0.2

                # Permite que del total de autos que tenemos, al menos el 20% choquen
                if isinstance(agent, Car):
                    return random.random() < 0.2
            # Si la celda está vacía, el movimiento está permitido
            return True 
        else:
            # La posición está fuera de la cuadricula
            return False  

    def getNextMovement(self):
        # Determinamos los próximos movimientos válidos para el auto
        x, y = self.pos
        # Movimientos válidos con envolvimiento vertical pero restricción horizontal
        potentialMovements = [(x, (y+1) % self.model.gridHeight), # Moverse hacia arriba
                            (x-1 if x > 0 else x, (y+1) % self.model.gridHeight), # Moverse arriba a la izquierda si no está en el borde izquierdo
                            (x+1 if x < self.model.gridWidth - 1 else x, (y+1) % self.model.gridHeight)] # Moverse arriba a la derecha si no está en el borde derecho
        validMovements = [move for move in potentialMovements if self.isPositionValid(move)]
        return validMovements

    # El step maneja al auto y las colisiones 
    def step(self):
        # Si el auto no ha colisionado, se mueve
        if self.counter % self.speedReduction == 0 and not self.hasCollided:
            validMovements = self.getNextMovement()
            # Si hay movimientos válidos, elegimos uno al azar y se ejecuta
            if validMovements:
                newPosition = random.choice(validMovements)
                self.model.grid.move_agent(self, newPosition)
                self.movements += 1

            # Verificar colisiones en la nueva posición
            cellContents = self.model.grid.get_cell_list_contents([self.pos])
            for agent in cellContents:
                # Si el agente es un auto y no es el mismo en la casilla, hay una colisión
                if isinstance(agent, Car) and agent is not self and random.random() < 0.2:
                    self.hasCollided = True
                    agent.hasCollided = True
                    self.model.collisions += 1
                # Si el agente es un obstáculo, hay una colisión
                elif isinstance(agent, Obstacle) and agent is not self:
                    self.hasCollided = True
                    self.model.collisions += 1
            self.counter = 1
        if not self.hasCollided:
            self.counter += 1

class CarNormal(Car):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)

class CarDiagonal(Car):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)

    def getNextMovement(self):
        # Determinamos los próximos movimientos válidos para el auto
        x, y = self.pos
        # Los movimientos válidos son a la izquierda y a la derecha
        potentialMovements = [(x-1 if x > 0 else x, (y+1) % self.model.gridHeight), # Moverse arriba-izquierda si no está en el borde izquierdo
                            (x+1 if x < self.model.gridWidth - 1 else x, (y+1) % self.model.gridHeight)] # Moverse arriba-derecha si no está en el borde derecho
        validMovements = [move for move in potentialMovements if self.isPositionValid(move)]
        return validMovements
    
class CarErratic(Car):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)

    def getNextMovement(self):
        # Determinamos los próximos movimientos válidos para el auto
        x, y = self.pos
        # Los movimientos válidos son en todas las direcciones
        potentialMovements = [(x, (y + 1) % self.model.gridHeight),  # Arriba
                              (x, (y - 1) % self.model.gridHeight),  # Abajo
                              (x - 1 if x > 0 else x, y),  # Izquierda
                              (x + 1 if x < self.model.gridWidth - 1 else x, y),  # Derecha
                              (x - 1 if x > 0 else x, (y + 1) % self.model.gridHeight),  # Arriba-Izquierda
                              (x + 1 if x < self.model.gridWidth - 1 else x, (y + 1) % self.model.gridHeight),  # Arriba a la derecha
                              (x - 1 if x > 0 else x, (y - 1) % self.model.gridHeight),  # Abajo a la izquierda
                              (x + 1 if x < self.model.gridWidth - 1 else x, (y - 1) % self.model.gridHeight)]  # Abajo a la derecha

        validMovements = [move for move in potentialMovements if self.isPositionValid(move)]
        return validMovements

class City(mesa.Model):
    """ Modelo para calle. Alumnos: Román Mauricio Elias Valencia - a01656603@tec.mx y Raúl Armando Vélez Robles - a01782488@tec.mx """
    def __init__(self, gridWidth, gridHeight):
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(gridWidth, gridHeight, True)
        
        self.movements = 0

        self.running = True
        self.averageSpeed = 0.0

        self.gridWidth = gridWidth
        self.gridHeight = gridHeight

        self.collisions = 0
        self.totalCollisions = 0

        # Añadimos un DataCollector para poder visualizarlos
        self.collisions_dataCollector = mesa.DataCollector(
            model_reporters={
                "Colisiones totales": lambda m: m.totalCollisions
            }
        )
        # Añadimos un DataCollector para poder visualizarlos
        self.types_dataCollector = mesa.DataCollector(
            model_reporters={
                "Auto Base": lambda m: sum(1 for a in m.schedule.agents if isinstance(a, CarNormal) and not a.hasCollided),
                "Auto en diagonal": lambda m: sum(1 for a in m.schedule.agents if isinstance(a, CarDiagonal) and not a.hasCollided),
                "Auto erratico": lambda m: sum(1 for a in m.schedule.agents if isinstance(a, CarErratic) and not a.hasCollided)
            }
        )

        positions = [(x, y) for x in range(gridWidth) for y in range(1, gridHeight-1)]
        uniqueId = 0

        # Colocamos los agentes en la cuadrícula
        for position in positions:
            if random.randint(1, 100) <= 10:
                agent = Obstacle(uniqueId, self)
            else:
                agent = Path(uniqueId, self)
            uniqueId += 1
            self.grid.place_agent(agent, position)

        # Define your car types in a list
        car_types = [CarNormal, CarDiagonal, CarErratic]

        # Colocamos los autos en la fila inferior
        for i in range(gridWidth):
            # Select a random car type
            car_type = random.choice(car_types)
            # Create a car of the selected type
            car = car_type(uniqueId, self)
            uniqueId += 1
            self.schedule.add(car)
            self.grid.place_agent(car, (i, 0))
        
        self.types_dataCollector.collect(self)

    def step(self):
        # Avanza el modelo un paso
        self.schedule.step()
        # Manejamos colisiones
        # Si se han registrado colisiones durante el último paso de la simulación, se procesan
        if self.collisions > 0:
            # Aumentamos el contador total de colisiones ocurridas durante la simulación
            self.totalCollisions += self.collisions
            # Recorremos todos los agentes para actualizar su estado post-colisión
            for agent in self.schedule.agents:
                # Si el agente Auto colisionó, aumentamos su velocidad de reducción
                if isinstance(agent, Car) and agent.hasCollided:
                    agent.speedReduction += 1
            self.collisions = 0

        nonCollidedCars = 0
        speedSum = 0.0

        for agent in self.schedule.agents:
            # Si el agente es un Auto, sumamos sus movimientos a los movimientos totales
            if isinstance(agent, Car):
                self.movements += agent.movements
                agent.movements = 0
                # Si el auto no ha colisionado, lo contamos para el promedio de velocidad
                if not agent.hasCollided:
                    nonCollidedCars += 1
                    speedSum += 1 / agent.speedReduction

        self.averageSpeed = speedSum / nonCollidedCars if nonCollidedCars else 0
        self.running = nonCollidedCars > 0

        # Añadimos los datos al DataCollector
        self.collisions_dataCollector.collect(self)
        self.types_dataCollector.collect(self)

# Configuración de la visualización
def agentPortrayal(agent):
    # Definimos cómo se instancian los agentes en la visualización
    if isinstance(agent, Path):
        portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "white", "w": 1, "h": 1}
    elif isinstance(agent, Obstacle):
        portrayal = {"Shape": "rect", "Filled": "true", "Layer": 1, "Color": "black", "w": 0.89, "h": 0.89}
    elif isinstance(agent, CarErratic):
        portrayal = {"Shape": "circle", "Filled": "false", "Layer": 2, "Color": "purple", "r": 0.5}
        if agent.hasCollided:
            portrayal["Color"] = "red"
            portrayal["Filled"] = "true"
    elif isinstance(agent, CarDiagonal):
        portrayal = {"Shape": "circle", "Filled": "false", "Layer": 2, "Color": "blue", "r": 0.5}
        if agent.hasCollided:
            portrayal["Color"] = "red"
            portrayal["Filled"] = "true"
    elif isinstance(agent, CarNormal):
        portrayal = {"Shape": "circle", "Filled": "false", "Layer": 2, "Color": "green", "r": 0.5}
        if agent.hasCollided:
            portrayal["Color"] = "red"
            portrayal["Filled"] = "true"
    return portrayal

GRID_WIDTH = 10
GRID_HEIGHT = 20

grid = CanvasGrid(agentPortrayal, GRID_WIDTH, GRID_HEIGHT, 400, 800)
parameters = {"gridWidth": GRID_WIDTH, "gridHeight": GRID_HEIGHT}

collisions_chart = ChartModule(
    [{"Label": "Colisiones totales", 
      "Color": "Red"}],
    data_collector_name='collisions_dataCollector'
)

types_chart = ChartModule(
    [{"Label": "Auto Base", "Color": "Green"},
        {"Label": "Auto en diagonal", "Color": "Blue"},
        {"Label": "Auto erratico", "Color": "Purple"}],
    data_collector_name='types_dataCollector'
)

server = ModularServer(City, [grid,collisions_chart,types_chart], "M1. Actividad (Coches Modificada)", parameters)
# Comentar la siguiente LC si vamos a correr el batchrun.py
server.launch()