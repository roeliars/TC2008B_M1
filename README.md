<img src="https://egresados.exatec.tec.mx/hubfs/Logo%2080%20años%20web%20qs.png" alt="HTML5" style="width:400px;height:100px">

# Modelación de sistemas multiagentes con gráficas computacionales - M1. Actividad (Coches Modificada)


*Instrucciones:*

Para este problema, deberás entregar, de manera individual, un informe en PDF que estudie las estadísticas de un robot de limpieza reactivo, así como el enlace al repositorio en Github del código desarrollado para esta actividad. El código debe ajustarse al estilo solicita en el siguiente documento.

Dado:
<ul>
  <li>Habitación de MxN espacios.</li>
  <li>Número de agentes.</li>
  <li>Porcentaje de celdas inicialmente libres / ocupadas.</li>
  <li>Tiempo máximo de ejecución o  cuántos agentes pueden reocrrer el camino.</li>
</ul>

Realiza la siguiente simulación:

<ul>
  <li>Inicializa las celdas ya sea como camino (espacio libre) o como obstáculo ( banquetas).</li>
  <li>Todos los agentes empiezan en la parte baja del camino y cruzan hacia arriba  evitando otros agentes u obstáculos.</li>
</ul>

En cada paso de tiempo:

<ul>
    <li>El agente revisa si la celda que pretende ocupar al tiempo siguiente está libre.</li>
    <li>Si la celda está libre, el agente elije una dirección aleatoria para moverse (unas de las 3 celdas vecinas al frente, al frente derecha o al frente izquierda) y elije la acción de movimiento (si no puede moverse allí, permanecerá en la misma celda).</li>
    <li>Asigne una pequeña probabilidad de fallo (aún cuando quería ir adelante podría terminar adelante a la derecha).</li>
    <li>Si por "accidente" dos agentes ocupan la misma celda entonces el "choque" deberá permanecer en esa celda . ( Una celda ocupada que reducirá el espacio libre disponible para los agentes coche.</li>
    <li>Proponga una conducta más (por persona) que resulte en segundo tipo de agente ( además del descrito arriba).</li>
</ul>

Deberás recopilar la siguiente información durante la ejecución:

<ul>
  <li>Número de accidentes.</li>
  <li>Velocidad Promedio de los agentes.( Se espera que la velocidad disminuya mientras aumenten los accidentes.</li>
  <li>Número de movimientos realizados por todos los agentes.</li>
  <li>Analiza cómo las diferentes conductas de cada tipo de agente impacta en las métricas de evaluación.</li>
</ul>

Asegúrate de incluir repeticiones , y la métrica de evaluación en el reporte escrito.

#
*Alumnos*
<ul>
  <li>Román Mauricio Elias Valencia - <a href="mailto:a01656603@tec.mx">a01656603@tec.mx</a></li>
  <li>Raúl Armando Vélez Robles - <a href="mailto:a01782488@tec.mx">a01782488@tec.mx</a></li>
</ul>

#
*Profesor*
<ul>
  <li>Oscar Francisco Fuentes Casarrubias - <a href="mailto:ofc1227@tec.mx">ofc1227@tec.mx</a></li>
</ul>
