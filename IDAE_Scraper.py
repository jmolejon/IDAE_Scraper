import time
import re
from selenium import webdriver
import csv
import argparse
import os

# Utilizo la libreria argparse para obtener del usuario si quiere scrapear el test o el dataset entero
parser = argparse.ArgumentParser()
parser.add_argument("--tipo", help='Indica con "test" si quieres probar el script o con "fullDB" si quieres scrapear la base entera')

args = parser.parse_args()

lenDatosParaSacar = 1 # Le doy valor 1 a el número de peticiones que se haran

if args.tipo == "test":
    lenDatosParaSacar = 100 # Asigna 100 a la variable lenDatosParaSacar para hacer un Test en los primeros.
    print("[TEST] Empezando scraper para obtener la información de los 100 primeros IDs disponibles en el IDAE ")

elif args.tipo == "fullDB":
    
    # Abro el navegador de Chrome para hacer el scraping
    driver = webdriver.Chrome('chromedriver/chromedriver.exe')
    driver.get("http://coches.idae.es/base-datos/marca-y-modelo") 

    html = driver.page_source
    time.sleep(2)

    # Obteniendo clave XSRF del HTML

    reHtmlXSFR = r'''<meta name="_token" content="(.*)">'''

    clave_limpia = re.search(reHtmlXSFR, html).group(1)

    # Imprimiendo claves por consola:
    print("[REGEX] La clave XSFR del HTML es la siguiente: " + str(clave_limpia) + "\n")

    scriptFetch = '''return fetch("http://coches.idae.es/ajax", {
    "headers": {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "es-ES,es;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-csrf-token": "''' + clave_limpia + '''",
        "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "http://coches.idae.es/base-datos/marca-y-modelo",
    "referrerPolicy": "no-referrer-when-downgrade",
    "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=''' + str(lenDatosParaSacar) + '''&search%5Bvalue%5D=&search%5Bregex%5D=false&_token=''' + clave_limpia + '''&campo=listado&ciclo=nedc&filtros=_token%3D''' + clave_limpia + '''%26tipo%3Dmarca-y-modelo%26motorizacion%3D%26categoria%3D%26segmento%3D%26marca%3D%26modelo%3D%26datos_nedc_length%3D''' + str(lenDatosParaSacar) + '''",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    })
    .then((response) => response.json())
        .then((responseData) => {
        console.log(responseData);
        return responseData;
        })
        .catch(error => console.warn(error));'''

    resultadoScript = driver.execute_script(scriptFetch) # Ejecuta el script de la llamada AJAX en Javascript en la consola del Chrome para obtener los ID
    lenDatosParaSacar = resultadoScript['recordsFiltered']

    print("[FullDB] Empezando scraper para obtener la información de los " + str(lenDatosParaSacar) + " IDs disponibles en el IDAE")

    driver.quit()


else:
    print('No ha seleccionado un --tipo correcto, por favor, elija entre "test" o "fullDB"')


if args.tipo == "test" or args.tipo == "fullDB":
        
    # Saco la hora de inicio del Script
    tic = time.time()

    # Defino la función para sacar información de cada ID
    def SacarInformacionID(id, claveXSFR):

        # Defino la llamada "fetch" de javascript que utilizare para sacar la información de los ID en la web
        scriptFetchID = '''return fetch("http://coches.idae.es/ajax", {
    "headers": {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "es-ES,es;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-csrf-token": "''' + claveXSFR + '''",
        "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "http://coches.idae.es/base-datos/marca-y-modelo",
    "referrerPolicy": "no-referrer-when-downgrade",
    "body": "campo=detalle&id=''' + str(id) + '''",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }).then((response) => response.json())
        .then((responseData) => {
        console.log(responseData);
        return responseData;
        })
        .catch(error => console.warn(error));'''

        resultadoScriptID = driver.execute_script(scriptFetchID) # Ejecuta el script del ID en cuestión

        htmlID = resultadoScriptID['cuerpo'] # Saco solo el cuerpo del HTML que tiene la información

        # Quito los "(" y los ")" del resultado del HTML para que la función regex funcione sin errores
        htmlIDTratado = htmlID.replace("(","X").replace(")","X")

        # Funciones REGEX para obtener la información del HTML
        reID = r'''value=\'(.*)\'>\r\n<table width'''
        reNombre = r'''<td class="titulo">Nombre</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Segmento comercial</td>\r\n'''
        reSegmentoComercial = r'''<td class="titulo">Segmento comercial</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Motorización</td>\r\n'''
        reMotorizacion = r'''<td class="titulo">Motorización</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Cilindrada</td>\r\n'''
        reCilindrada = r'''<td class="titulo">Cilindrada</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Tipo de cambio</td>\r\n'''
        reTipoDeCambio = r'''<td class="titulo">Tipo de cambio</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">MTMA</td>\r\n'''
        reMTMA = r'''<td class="titulo">MTMA</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Potencia</td>\r\n'''
        rePotencia = r'''<td class="titulo">Potencia</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Potencia térmica</td>\r\n'''
        rePotenciaTermica = r'''<td class="titulo">Potencia térmica</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Potencia eléctrica</td>\r\n'''
        rePotenciaElectrica = r'''<td class="titulo">Potencia eléctrica</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Autonomía eléctrica</td>\r\n'''
        reAutonomiaElectrica = r'''<td class="titulo">Autonomía eléctrica</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n            <tr>\r\n            <td class="titulo">Consumo según ciclo NEDC</td>\r\n'''
        reConsumoNEDC = r'''<td class="titulo">Consumo según ciclo NEDC</td>\r\n            <td>(.*)\r\n                                    litros/100 kms\r\n                            </td>\r\n        </tr>\r\n        <tr>\r\n            <td class="titulo">Consumo según ciclo WLTP</td>\r\n'''
        reConsumoWLTP = r'''<td class="titulo">Consumo según ciclo WLTP</td>\r\n            <td>(.*)\r\n                                    litros/100 kms\r\n                            </td>\r\n        </tr>\r\n        <tr>\r\n        <td class="titulo">Emisiones según ciclo NEDC</td>\r\n'''
        reEmisionesNEDC = r'''<td class="titulo">Emisiones según ciclo NEDC</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Emisiones según ciclo WLTP</td>\r\n'''
        reEmisionesWLTP = r'''<td class="titulo">Emisiones según ciclo WLTP</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Dimensiones'''
        reDimensiones = r'''<td class="titulo">Dimensiones Xlargo x ancho x altoX</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Nº de Plazas Máximas</td>\r\n'''
        rePlazasMaximas = r'''<td class="titulo">Nº de Plazas Máximas</td>\r\n        <td>(.*)</td>\r\n    </tr>\r\n    <tr>\r\n        <td class="titulo">Clasificación por Consumo Relativo</td>\r\n'''
        reClasificacionPorConsumoRelativo = r'''<td class="titulo">Clasificación por Consumo Relativo</td>\r\n        <td><img src="http://coches.idae.es/img/clasificacion/(.*).gif" title="Clasificación:'''

        # Creo una lista con las funciones regex
        listaAtributos = [reID, reNombre, reSegmentoComercial, reMotorizacion, reCilindrada, reTipoDeCambio, reMTMA, rePotencia, rePotenciaTermica, rePotenciaElectrica, reAutonomiaElectrica, reConsumoNEDC, reConsumoWLTP, reEmisionesNEDC, reEmisionesWLTP, reDimensiones, rePlazasMaximas, reClasificacionPorConsumoRelativo]

        # Creo una lista vacia para guardar los datos a retornar por la función
        listaARetornar = []

        # Itero sobre la lista de atributos para obtener la información
        for i in listaAtributos:
            #Creo un IF para diferenciar cuando hay datos de cuando no, y cuando no los hay añadir a la lista un NA:
            if re.search(i, htmlIDTratado) is None:
                listaARetornar.append("NA")
            else:
                listaARetornar.append(re.search(i, htmlIDTratado).group(1).replace('<sup>','').replace('</sup>','').replace('<sub>','').replace('</sub>',''))

        # Devuelvo la lista en la función
        return(listaARetornar)

    driver = webdriver.Chrome('chromedriver/chromedriver.exe') # Abro el navegador
    driver.get("http://coches.idae.es/base-datos/marca-y-modelo")  # Accedo a la url en cuestión

    html = driver.page_source
    time.sleep(2)

    # Obteniendo clave XSRF del HTML

    reHtmlXSFR = r'''<meta name="_token" content="(.*)">'''

    clave_limpia = re.search(reHtmlXSFR, html).group(1)

    # Imprimiendo claves por consola:
    print("[REGEX] La clave XSFR del HTML es la siguiente: " + str(clave_limpia) + "\n")

    scriptFetch = '''return fetch("http://coches.idae.es/ajax", {
    "headers": {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "es-ES,es;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-csrf-token": "''' + clave_limpia + '''",
        "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "http://coches.idae.es/base-datos/marca-y-modelo",
    "referrerPolicy": "no-referrer-when-downgrade",
    "body": "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=''' + str(lenDatosParaSacar) + '''&search%5Bvalue%5D=&search%5Bregex%5D=false&_token=''' + clave_limpia + '''&campo=listado&ciclo=nedc&filtros=_token%3D''' + clave_limpia + '''%26tipo%3Dmarca-y-modelo%26motorizacion%3D%26categoria%3D%26segmento%3D%26marca%3D%26modelo%3D%26datos_nedc_length%3D''' + str(lenDatosParaSacar) + '''",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    })
    .then((response) => response.json())
        .then((responseData) => {
        console.log(responseData);
        return responseData;
        })
        .catch(error => console.warn(error));'''

  
    resultadoScript = driver.execute_script(scriptFetch) # Ejecuta el script en la consola del Chrome para hacer fetch con Javascript y obtener la información
   

    # Creo una lista con el encabezado del CSV donde guardar la información de cada ID:
    resultadoScraper = [['ID en el IDAE', 'Nombre del vehículo', 'Segmento comercial', 'Motorizacion', 'Cilindrada', 'Tipo de cambio', 'MTMA', 'Potencia en CV', 'Potencia termica', 'Potencia Electrica', 'Autonomia Electrica', 'Consumo NEDC', 'Consumo WLTP', 'Emisiones NEDC', 'Emisiones WLTP', 'Dimensiones (largo x ancho x alto)', 'Nº de plazas maximas', 'Clasificacion por consumo relativo']]

    # Obtengo el número de IDs para imprimire el progreso por pantalla y creo una variable para guardar cuantos ha realizado:
    lenIDS = len(resultadoScript['data'])
    peticionesCompletadas = 0

    # Itero sobre los datos obtenidos para sacar los ID y operar sobre los mismos:
    for id in resultadoScript['data']:
        resultadoScraper.append(SacarInformacionID(id[-1], clave_limpia))
        peticionesCompletadas += 1
        print("Proceso al " + str( round( (peticionesCompletadas/lenIDS)*100, 1) ) + "%")
        #time.sleep(3) # Tiempo entre petición y petición

    with open('csv/resultado.csv', 'w', newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=';')
        escritor.writerows(resultadoScraper)

    # Cierro el navegador:
    driver.quit()

    toc = time.time()-tic
    print('Proceso finalizado en ' + str(round(toc)) + " segundos, con una media de " + str(round(toc/lenDatosParaSacar, 2)) + " segundos por ID.")