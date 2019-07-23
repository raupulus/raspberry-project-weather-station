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
cn = engine.connect()

## Creo tablas
humidity = Table(
   'meteorology_humidity', meta,
   Column('id', Numeric(11), primary_key=True),
   Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
   Column('created_at', DateTime),
)

pressure = Table(
   'meteorology_pressure', meta,
   Column('id', Numeric(11), primary_key=True),
   Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
   Column('created_at', DateTime),
)

temperature = Table(
   'meteorology_temperature', meta,
   Column('id', Numeric(11), primary_key=True),
   Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
   Column('created_at', DateTime),
)

meta.create_all(engine)

## Muestro tablas existentes
print(engine.table_names())

## Inserto Datos
#stmt = humidity.insert().values(data='newdata').return_defaults()
#result = connection.execute(stmt)
#server_created_at = result.returned_defaults['created_at']



#######################################
# #             Funciones           # #
#######################################


def storageDB(datos):
    '''
        Almacena el array de datos tomados por los sensores en la base de datos.
    '''

    print(datos)


def main():
    ## Instancio todas las clases
    #bme280 = BME280()

    ## Leo todos los sensores
    #temperature, pressure, humidity = bme280.readBME280All()
    #raspberryTempCPU = func.rpi_cpu_temp()
    temperature, pressure, humidity = [10, 20, 30]

    datos = {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
    }

    ## Almaceno los datos en la DB
    storageDB(datos)


if __name__ == "__main__":
    main()
