#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2019
# Project Name:
# Description:
#
# Dependencies:
#
# Revision 0.01 - File Created
# Additional Comments:

# @copyright  Copyright © 2019 Raúl Caro Pastorino
# @license    https://wwww.gnu.org/licenses/gpl.txt

# Copyright (C) 2019  Raúl Caro Pastorino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Guía de estilos aplicada: PEP8

#######################################
# #           Descripción           # #
#######################################
##
# # Este script recopila datos de los sensores y los almacena en la base
# # de datos.
##

#######################################
# #       Importar Librerías        # #
#######################################
import time  # Importamos la libreria time --> time.sleep
import datetime
import random  # Genera números aleatorios --> random.randrange(1,100)
import functions as func
from dotenv import load_dotenv
import os

## Cargo archivos de configuración desde .env sobreescribiendo variables locales.
load_dotenv(override=True)

# Importo el modelo que interactua con la base de datos.
from Models.Dbconnection import Dbconnection
from Models.Apiconnection import Apiconnection

# Importo modelos para los sensores
from Models.Sensors.BME280 import BME280
from Models.Sensors.BH1750 import BH1750
from Models.Sensors.Anemometer import Anemometer

#######################################
# #             Variables           # #
#######################################
sleep = time.sleep

# Abro conexión con la base de datos instanciando el modelo que la representa.
dbconnection = Dbconnection()

# Parámetros para acceder a la API.
apiconnection = Apiconnection()

# Instancio clase por cada sensor
bme280 = BME280()
bh1750 = BH1750()

########################### REFACTORIZANDO ##############################

# Diccionario con todos los sensores utilizados (Declarados en .env)
sensors = {}

# Compruebo si está habilitado el sensor para instanciarlo
if (os.getenv('S_ANEMOMETER') == 'True') or \
   (os.getenv('S_ANEMOMETER') == 'true'):

    # Establezco la ruta a la API
    api_path = '/ws/winter/add-json'

    sensors['anemometer'] = {
        'sensor': Anemometer(pin=int(os.getenv('S_ANEMOMETER_PIN'))),
        'table': Anemometer.table_name,
        'data': None,
        'api_path': api_path,
    }

    # Inicio Evento de lectura y cálculo de datos para anemómetro.
    sensors['anemometer']['sensor'].start_read()

    # Seteo tabla en el modelo de conexión a la DB.
    dbconnection.table_set_new(
        sensors['anemometer']['table'],  # Nombre de la tabla.
        sensors['anemometer']['sensor'].tablemodel()  # Modelo de tabla con sus columnas.
    )


def read_sensor(method):
    """
    Recibe el método para obtener todos los datos del sensor e intenta
    conseguirlo o en caso contrario anota el error en el registro de logs.
    :param method: Método a intentar ejecutar.
    :return: Resultado de lectura para el sensor.
    """
    try:
        return method()
    except Exception:
        print('Error al leer sensor ', str(method))
        return None


def read_sensors():
    """
    Lee todos los sensores y los añade al diccionario.
    """
    for name, params in sensors.items():
        print('Leyendo sensor: ', name)
        params['data'] = read_sensor(params['sensor'].get_all_datas)


def save_to_db(dbconnection):
    """
    Almacena los datos de los sensores en la base de datos.
    :param dbconnection:
    """

    for name, params in sensors.items():
        dbconnection.table_save_data(
            sensorname=name,
            tablename=sensors[name]['table'],
            params=params['data']
        )

def save_to_api(apiconnection, dbconnection):
    """
    Obtiene los datos para cada sensor de la DB y los envía a la API
    :param apiconnection:
    :param dbconnection:
    """

    for name, params in sensors.items():
        ## Parámetros/tuplas desde la base de datos.
        params_from_db = dbconnection.table_get_data(params['table'])

        ## Columnas del modelo.
        columns = dbconnection.tables[params['table']].columns.keys()

        try:
            response = apiconnection.upload(
                name,
                params['api_path'],
                params_from_db,
                columns,
            )

            # Limpio los datos de la tabla si se ha subido correctamente.
            if response:
                dbconnection.table_truncate(params['table'])
        except():
            print('Error al subir a la api: ', name)


def loop():
    # Leo los sensores y los almaceno
    n_lecturas = 0
    while True:
        n_lecturas = n_lecturas + 1

        print('Lecturas de sensores desde la última subida: ' + str(n_lecturas))


        # Guardo el momento que inicia lectura.
        marca_inicio = datetime.datetime.now(tz=None)

        # Leyendo sensores y almacenándolos en el array **sensors**
        read_sensors()

        # Almacena en la base de datos.
        save_to_db(dbconnection)

        # TODO → Controlar por tiempo (unos 5 min) en vez de posición
        if n_lecturas == 1:
            n_lecturas = 0

            try:
                save_to_api(apiconnection, dbconnection)
            except():
                print('Error al subir datos a la api')

        # Muestro tiempo en realizarse la lectura de datos.
        print('Inicio: ', str(marca_inicio))
        marca_fin = datetime.datetime.now(tz=None)
        print('Fin: ', str(marca_fin))

        tiempo_ejecucion = marca_fin - marca_inicio
        print('Tiempo de ejecución: ', str(tiempo_ejecucion))

        # Pausa entre cada lectura
        sleep(10)

    # Acciones tras terminar con error
    # TODO → controlar interrupciones y excepciones para limpiar/reiniciar todo.
    dbconnection.closeConnection()
    anemometer.stop_read()

    exit(0)

loop()
exit(0)


########################### FIN DEL REFACTORIZADO





#######################################
# #             Funciones           # #
#######################################


def readSensor(sensor_method, sensor_name=''):
    try:
        return sensor_method()
    except Exception:
        print('Error al leer sensor ' + sensor_name)
        return None


def readSensors():
    """
    Lee todos los sensores y lo devuelve como diccionario.
    :return:
    """

    # BME280 - Temperatura, presión y humedad.
    #temperature, pressure, humidity = bme280.readBME280All()
    temperature, pressure, humidity = readSensor(bme280.readBME280All, 'BME280')

    # BH1750 - Sensor de luz en medida lux
    light = readSensor(bh1750.read_light, 'BH1750')

    # Anemometer - Sensor de velocidad de viento leyendo impulsos, medida en m/s
    #wind = anemometer.get_all_datas()

    # Datos para probar sin usar sensores
    """
    temperature, pressure, humidity, light = [
        random.randrange(15, 38),
        random.randrange(800, 1200),
        random.randrange(30, 80),
        random.randrange(4, 100000),
    ]
    """

    # Raspberry temperatura de la CPU
    #rasp_cpu_temp = func.rpi_cpu_temp()

    return {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        'light': light,
        #'wind': wind,
        #'rasp_cpu_temp': rasp_cpu_temp,
    }

def saveData(dbconnection, lecturas):
    """
    Almacena los datos de los sensores en la base de datos.
    :param dbconnection:
    :param lecturas:
    :return:
    """


    dbconnection.saveHumidity({'value': lecturas.get('humidity')})
    dbconnection.savePressure({'value': lecturas.get('pressure')})
    dbconnection.saveTemperature({'value': lecturas.get('temperature')})
    dbconnection.saveLight({'value': lecturas.get('light')})


def dataToApi(apiconnection, data):
    """
    Sube todos los datos locales a la API en el VPS externo.
    :return:
    """

    # leer datos desde select
    # subirlos a la api
    # borrarlos de la db local

    print('.......................')
    print('Subiendo datos a la API')
    print('.......................')

    humidity = data.get('humidity')
    pressure = data.get('pressure')
    temperature = data.get('temperature')
    light = data.get('light')

    apiconnection.upload_humidity(humidity)
    apiconnection.upload_pressure(pressure)
    apiconnection.upload_temperature(temperature)
    apiconnection.upload_light(light)


## TODO → Esta función quedará en bucle tomando datos cada 10 o 30 segundos.
def main():
    # Abro conexión con la base de datos.
    dbconnection = Dbconnection()

    # Parámetros para acceder a la API
    apiconnection = Apiconnection()



    # Leo los sensores y los almaceno TODO → Agregar try catch
    n_lecturas = 0
    while True:
        n_lecturas = n_lecturas + 1

        # Guardo el momento que inicia lectura
        marca_inicio = datetime.datetime.now(tz=None)

        print('Lecturas de sensores desde la última subida: ' + str(n_lecturas))

        lecturas = readSensors()

        if lecturas is not None:
            saveData(dbconnection, lecturas)

        # TODO → Controlar por tiempo (unos 5 min) en vez de posición
        if n_lecturas == 2:
            n_lecturas = 0

            try:
                dataToApi(apiconnection, dbconnection.getAllData())
                dbconnection.truncate_all_sensors_data()
            except():
                print('Error al subir datos a la api')

        # Muestro tiempo en realizarse la lectura de datos.
        print('Inicio: ', str(marca_inicio))
        marca_fin = datetime.datetime.now(tz=None)
        print('Fin: ', str(marca_fin))

        tiempo_ejecucion = marca_fin - marca_inicio
        print('Tiempo de ejecución: ', str(tiempo_ejecucion))

        # Pausa entre cada lectura
        sleep(40)

    # Acciones tras terminar con error
    # TODO → controlar interrupciones y excepciones para limpiar/reiniciar todo.
    dbconnection.closeConnection()
    anemometer.stop_read()

    exit(0)


if __name__ == "__main__":
    main()
