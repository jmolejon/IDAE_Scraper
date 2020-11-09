# IDAE Scraper
## Descripción

Practica realizada para la asignatura _Tipología y ciclo de vida de los datos_ perteneciente al Maáster en Ciencia de Datos de la UOC. 
En esta se aplican tecnicas de _web scraping_ en Python (y una pequeña parte en Javascript) para **extraer la información almacenada en la web del IDAE** (Instituto para la Diversificación y Ahorro de la Energia de España) **referente a todos los vehículos registrados**.

## Miembros del equipo

La actividad ha sido realizada de manera individual por **José Diego Molejón Lanuza**.

## Instrucciones

Para ejecutar el script es necesario instalar las siguientes librerias y utilizar Python 3:
```
pip install selenium
```

Las siguientes librerias tambien son necesarias, aunque lo más normal es que ya vengan con la distribución de Python:
```
pip install csv
pip install re
pip install time
```

A su vez, se deja en el proyecto en la carpeta *chromedriver/** un **.exe** del software Chrome en su versión _86.0.4240.22_ para **windows** .
Este archivo es necesario para la ejecución del script por Selenium pero solo funcionara en Windows, en caso de querer ejecutar el script en una maquina Linux o Mac se debera descargar el archivo correspondiente indicado en <https://chromedriver.chromium.org/downloads> y sustituirlo en la carpeta **chromedriver/** .

El script se debe ejecutar de la siguiente manera:
```
python3 IDAE_Scraper.py --tipo "fullDB"
```

Donde **tipo** hace referencia a si se quiere descargar la base de datos entera (60 minutos aproximadamente a dia de hoy) o solo se quiere descargar las 100 primeras fichas para hacer un test.
Los posibles valores que puede tomar **tipo** son **"test"** o **"fullDB"**
Una vez recopilada toda la información por el script, esta sera guardada en la carpeta **csv/** en un archivo de tipo CSV.

En este dataset se podra encontrar la siguiente información:
- **ID en el IDAE** referente al ID que le proporciona el IDAE en su base de datos al vehículo en cuestión.
- **Nombre del vehículo** en la que podemos encontrar información de la **marca** , **version** o **MY** (Model Year), entre otras, del vehículo en cuestión.
- **Segmento comercial** al que pertenece el vehículo.
- Tipo de **Motorización** del vehículo como _gasolina, gasoleo, etc..._
- **Cilindrada** en centímetros cúbicos del vehículo
- **Tipo de cambio** del vehículo, siendo esta "M" para manual o "A" para automático.
- La masa máxima técnicamente admisible o **MTMA** .
- **Potencia en CV** del vehículo.
- **Potencia termica** del vehículo
- **Potencia eléctrica** en caso de tenerla para los _hibridos o vehículos eléctricos_ .
- **Autonomía eléctrica** en caso de tenerla para los _hibridos o vehículos eléctricos_ .
- **Consumo NEDC** de combustible en ciclo combinado en litros por 100 km.
- **Consumo WLTP** de combustible en ciclo combinado en litros por 100 km.
- **Emisiones NEDC** de combustible en ciclo combinado en gramos de CO2 por KM.
- **Emisiones WLTP** de combustible en ciclo combinado en gramos de CO2 por KM.
- **Dimensiones del vehículo** en _largo x ancho x alto_ .
- **Número de plazas máximas** admitidas en el vehículo.
- **Clasificación por consumo relativo** que es una clasificación energética dada por el IDAE a los vehículos en relación a sus consumos y dimensiones en relación a los coches registrados. Este dato es utilizado para las ayudas del plan RENOVE lanzado por el gobierno de España este 2020.

## Dataset adjunto

En la carpeta **csv/** de este repositorio podremos encontrar un archivo CSV con la información sacada a dia 09/11/2020 de los 17.692 registros que existian en la web.

## Recursos

1. Documentación de la libreria Selenium para Python https://selenium-python.readthedocs.io/
2. Documentación de la libreria re para Python https://docs.python.org/3/library/re.html
3. Pregunta en StackOverflow sobre X-CSRF Token https://stackoverflow.com/questions/24196140/adding-x-csrf-token-header-globally-to-all-instances-of-xmlhttprequest
