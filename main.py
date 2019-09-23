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
#from Models.Sensors.BME280 import BME280
from Models.Sensors.BME280_humidity import BME280_humidity
from Models.Sensors.BME280_temperature import BME280_temperature
from Models.Sensors.BME280_pressure import BME280_pressure
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

# Diccionario con todos los sensores utilizados (Declarados en .env)
sensors = {}

# Anemómetro (leyendo pulsos pin GPIO)
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

# Sensor de luz BH1750
if (os.getenv('S_BH1750') == 'True') or \
   (os.getenv('S_BH1750') == 'true'):
    # Establezco la ruta a la API
    api_path = '/ws/light/add-json'

    sensors['bh1750'] = {
        'sensor': BH1750(),
        'table': BH1750.table_name,
        'data': None,
        'api_path': api_path,
    }

    # Seteo tabla en el modelo de conexión a la DB.
    dbconnection.table_set_new(
        sensors['bh1750']['table'],  # Nombre de la tabla.
        sensors['bh1750']['sensor'].tablemodel()  # Modelo de tabla y columnas.
    )

# Sensor de temperatura/presión/humedad
if (os.getenv('S_BME280') == 'True') or \
   (os.getenv('S_BME280') == 'true'):
    # Establezco la ruta a la API
    api_path_humidity = '/ws/humidity/add-json'
    api_path_temperature = '/ws/temperature/add-json'
    api_path_pressure = '/ws/pressure/add-json'

    sensors['bme280_humidity'] = {
        'sensor': BME280_humidity(),
        'table': BME280_humidity.table_name,
        'data': None,
        'api_path': api_path_humidity,
    }

    sensors['bme280_temperature'] = {
        'sensor': BME280_temperature(),
        'table': BME280_temperature.table_name,
        'data': None,
        'api_path': api_path_temperature,
    }

    sensors['bme280_pressure'] = {
        'sensor': BME280_pressure(),
        'table': BME280_pressure.table_name,
        'data': None,
        'api_path': api_path_pressure,
    }

    # Seteo tabla en el modelo de conexión a la DB.
    dbconnection.table_set_new(
        sensors['bme280_humidity']['table'],  # Nombre de la tabla.
        sensors['bme280_humidity']['sensor'].tablemodel()  # Modelo de tabla y columnas.
    )

    dbconnection.table_set_new(
        sensors['bme280_temperature']['table'],  # Nombre de la tabla.
        sensors['bme280_temperature']['sensor'].tablemodel()  # Modelo de tabla y columnas.
    )

    dbconnection.table_set_new(
        sensors['bme280_pressure']['table'],  # Nombre de la tabla.
        sensors['bme280_pressure']['sensor'].tablemodel()  # Modelo de tabla y columnas.
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
    # Contador de lecturas desde la última subida a la API
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
        if n_lecturas == 2:
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
        sleep(40)

    # Acciones tras terminar con error
    # TODO → controlar interrupciones y excepciones para limpiar/reiniciar todo.
    dbconnection.close_connection()
    anemometer.stop_read()

    exit(0)


def main():
    print('Iniciando Aplicación')
    loop()
    exit(0)


if __name__ == "__main__":
    main()
