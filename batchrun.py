import numpy as np
from M1 import City
import matplotlib.pyplot as plt

def run_model(gridWidth, gridHeight, n_steps):
    # Creamos una instancia del modelo
    model = City(gridWidth, gridHeight)

    # Almacenamos datos por paso
    collisions_per_step = []
    autos_base_per_step = []
    autos_diagonal_per_step = []
    autos_erratico_per_step = []

    for _ in range(n_steps):
        model.step()
        # Recopilamos los datos de colisiones
        collisions_per_step.append(model.totalCollisions)

        # Recopilamos los datos de los tipos de autos
        model.types_dataCollector.collect(model)
        autos_base_per_step.append(model.types_dataCollector.get_model_vars_dataframe()["Auto Base"].iloc[-1])
        autos_diagonal_per_step.append(model.types_dataCollector.get_model_vars_dataframe()["Auto en diagonal"].iloc[-1])
        autos_erratico_per_step.append(model.types_dataCollector.get_model_vars_dataframe()["Auto erratico"].iloc[-1])

    return collisions_per_step, autos_base_per_step, autos_diagonal_per_step, autos_erratico_per_step

if __name__ == "__main__":
    # Definimos los parámetros del modelo
    gridWidth = 10
    gridHeight = 20
    n_steps = 100  # Damos el número de pasos por ejecución

    # Ejecutar el modelo n veces
    n_executions = 100
    all_collisions = []
    all_autos_base = []
    all_autos_diagonal = []
    all_autos_erratico = []

    for _ in range(n_executions):
        collisions, autos_base, autos_diagonal, autos_erratico = run_model(gridWidth, gridHeight, n_steps)
        all_collisions.append(collisions)
        all_autos_base.append(autos_base)
        all_autos_diagonal.append(autos_diagonal)
        all_autos_erratico.append(autos_erratico)

    # Calculamos el promedio para colisiones y cada tipo de auto por paso
    average_collisions_per_step = [sum(step) / n_executions for step in zip(*all_collisions)]
    average_autos_base = [sum(step) / n_executions for step in zip(*all_autos_base)]
    average_autos_diagonal = [sum(step) / n_executions for step in zip(*all_autos_diagonal)]
    average_autos_erratico = [sum(step) / n_executions for step in zip(*all_autos_erratico)]

    # Gráficamos de colisiones en una ventana separada
    fig1 = plt.figure(figsize=(10, 6))
    ax1 = fig1.add_subplot(111)
    ax1.plot(average_collisions_per_step, color='black')
    ax1.set_title("Promedio de Colisiones Totales por Paso")
    ax1.set_xlabel("Pasos")
    ax1.set_ylabel("Promedio de Colisiones Totales")
    plt.show()

    # Gráficamos de tipos de autos en otra ventana separada
    fig2 = plt.figure(figsize=(10, 6))
    ax2 = fig2.add_subplot(111)
    ax2.plot(average_autos_base, label='Autos Base', color='green')
    ax2.plot(average_autos_diagonal, label='Autos Diagonal', color='blue')
    ax2.plot(average_autos_erratico, label='Autos Erráticos', color='red')
    ax2.set_title("Promedio de Autos por Tipo por Paso")
    ax2.set_xlabel("Pasos")
    ax2.set_ylabel("Promedio de Autos")
    ax2.legend()
    plt.show()