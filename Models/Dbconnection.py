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
# # Conexión a la base de datos.
##

#######################################
# #       Importar Librerías        # #
#######################################

import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, \
    MetaData, DateTime, Numeric, select

## Cargo archivos de configuración desde .env
from dotenv import load_dotenv
load_dotenv(override=True)
import os

#######################################
# #             Variables           # #
#######################################

#######################################
# #             Funciones           # #
#######################################


class Dbconnection:
    ## Datos desde .env
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Conexión a la base de datos
    engine = create_engine(DB_CONNECTION + '://' + DB_USERNAME +
                           ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT
                           + '/' + DB_DATABASE)
    meta = MetaData()
    connection = engine.connect()

    # Creo tablas
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
    print('Tablas en la DB: ', engine.table_names())

    def storageDB (self, table, datos):
        '''
            Almacena el array de datos tomados por los sensores en la base de datos.
        '''

        print('Guardando: ', table, datos)

        ## Inserto Datos
        stmt = table.insert().values(datos).return_defaults()
        result = self.connection.execute(stmt)
        # server_created_at = result.returned_defaults['created_at']

        return result

    def saveHumidity(self, datos):
        return self.storageDB(self.table_humidity, datos)

    def getHumidity(self):
        return self.connection.execute(
            select([
                self.table_humidity.columns.value,
                self.table_humidity.columns.created_at,
            ])
        )

    def savePressure(self, datos):
        return self.storageDB(self.table_pressure, datos)

    def getPressure(self):
        return self.connection.execute(
            select([
                self.table_pressure.columns.value,
                self.table_pressure.columns.created_at,
            ])
        )

    def saveTemperature(self, datos):
        return self.storageDB(self.table_temperature, datos)

    def getTemperature(self):
        return self.connection.execute(
            select([
                self.table_temperature.columns.value,
                self.table_temperature.columns.created_at,
            ])
        )

    def getAllData(self):
        '''
        Obtiene todos los datos de la base de datos para organizarlos
        y devolverlos.
        :return:
        '''

        return {
            'humidity': self.getHumidity(),
            'pressure': self.getPressure(),
            'temperature': self.getTemperature(),
        }

    def deleteAll(self):
        pass

    def closeConnection(self):
        print('Cerrando conexión con la Base de Datos')
        self.connection.close()
