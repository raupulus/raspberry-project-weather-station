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
from sqlalchemy import create_engine, Table, Column, Integer, String, \
    MetaData, DateTime, Numeric

## Cargo archivos de configuración desde .env
from dotenv import load_dotenv
load_dotenv(override=True)
import os

#######################################
# #             Variables           # #
#######################################
sleep = time.sleep

## Datos desde .env
DB_CONNECTION = os.getenv("DB_CONNECTION")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

## Conexión a la base de datos
engine = create_engine(DB_CONNECTION +'://' + DB_USERNAME +
                       ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT
                       + '/' + DB_DATABASE)
meta = MetaData()
connection = engine.connect()

## Creo tablas
table_humidity = Table(
   'meteorology_humidity', meta,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
   Column('created_at', DateTime, default=datetime.datetime.utcnow),
)

table_pressure = Table(
   'meteorology_pressure', meta,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
   Column('created_at', DateTime, default=datetime.datetime.utcnow),
)

table_temperature = Table(
   'meteorology_temperature', meta,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
   Column('created_at', DateTime, default=datetime.datetime.utcnow),
)

meta.create_all(engine)

## Muestro tablas existentes
print(engine.table_names())

#######################################
# #             Funciones           # #
#######################################


def storageDB(table, dato):
    '''
        Almacena el array de datos tomados por los sensores en la base de datos.
    '''

    print(dato)

    ## Inserto Datos
    stmt = table.insert().values(value=dato).return_defaults()
    result = connection.execute(stmt)
    # server_created_at = result.returned_defaults['created_at']

    return result


## TODO → Esta función quedará en bucle tomando datos cada 30 segundos.
def main():
    ## Instancio todas las clases
    ## TODO → Refactorizar de forma que la toma de datos y guardado se pueda
    ## repetir para un sensor concreto si este falla al tomar dato o guardar.
    #bme280 = BME280()

    ## Leo todos los sensores
    #temperature, pressure, humidity = bme280.readBME280All()
    #raspberryTempCPU = func.rpi_cpu_temp()
    temperature, pressure, humidity = [10, 20, 30]

    ## Almaceno los datos en la DB
    ## TODO → Comprobar si guardado falla para retomar medición
    storageDB(table_temperature, temperature)
    storageDB(table_pressure, pressure)
    storageDB(table_humidity, humidity)


if __name__ == "__main__":
    main()
