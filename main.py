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
#from Models.Sensors.BME280 import BME280

## Cargo archivos de configuración desde .env
from dotenv import load_dotenv

#from Models.Sensors.BME280 import BME280

load_dotenv(override=True)

## Importo el modelo que interactua con la base de datos.
from Models.Dbconnection import Dbconnection
from Models.Apiconnection import Apiconnection


#######################################
# #             Variables           # #
#######################################
sleep = time.sleep

## Instancio clase por cada sensor
#bme280 = BME280()

#######################################
# #             Funciones           # #
#######################################


def readSensors():
    '''
    Lee todos los sensores y lo devuelve como diccionario.
    :return:
    '''

    # BME280 - Temperatura, presión y humedad.
    #temperature, pressure, humidity = bme280.readBME280All()
    temperature, pressure, humidity = [
        random.randrange(15, 38),
        random.randrange(800, 1200),
        random.randrange(30, 80)
    ]

    # Raspberry temperatura
    # rasp_cpu_temp = func.rpi_cpu_temp()

    return {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        #'rasp_cpu_temp': rasp_cpu_temp,
    }

def saveData(dbconnection, lecturas):
    '''
    Almacena los datos de los sensores en la base de datos.
    :param dbconnection:
    :param lecturas:
    :return:
    '''

    dbconnection.saveHumidity({'value': lecturas.get('humidity')})
    dbconnection.savePressure({'value': lecturas.get('pressure')})
    dbconnection.saveTemperature({'value': lecturas.get('temperature')})


def dataToApi(apiconnection, data):
    '''
    Sube todos los datos locales a la API en el VPS externo.
    :return:
    '''

    # leer datos desde select
    # subirlos a la api
    # borrarlos de la db local

    print('.......................')
    print('Subiendo datos a la API')
    print('.......................')

    humidity = data.get('humidity')
    pressure = data.get('pressure')
    temperature = data.get('temperature')

    apiconnection.upload_humidity(humidity)
    apiconnection.upload_pressure(pressure)
    apiconnection.upload_temperature(temperature)


## TODO → Esta función quedará en bucle tomando datos cada 10 o 30 segundos.
def main():
    # Abro conexión con la base de datos.
    dbconnection = Dbconnection()
    apiconnection = Apiconnection()

    # Parámetros para acceder a la API
    api = ''

    marca_inicio = datetime.datetime.now(tz=None)

    # Leo los sensores y los almaceno TODO → Agregar try catch
    for pos in range(10):
        print('Lectura de sensor nº ' + str(pos))
        lecturas = readSensors()

        if lecturas is not None:
            saveData(dbconnection, lecturas)

        # TODO → Controlar por tiempo (unos 5 min) en vez de posición
        if pos == 9:
            dataToApi(apiconnection, dbconnection.getAllData())
            dbconnection.truncate_all_sensors_data()

        #sleep(10)

    dbconnection.closeConnection()

    print('Inicio: ', str(marca_inicio))
    marca_fin = datetime.datetime.now(tz=None)
    print('Fin: ', str(marca_fin))

    tiempo_ejecucion = marca_fin - marca_inicio
    print('Tiempo de ejecución: ', str(tiempo_ejecucion))


    exit(0)


if __name__ == "__main__":
    main()
