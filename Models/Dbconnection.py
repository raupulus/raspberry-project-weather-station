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


# TODO → Adecuar nombres de métodos a reglas de estilos
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


    ##################### REFACTORIZANDO
    tables = []
    def table_set_new(self):
        """
        Almacena una nueva tabla en el array de tablas.
        """
        pass

    def table_get_data(self, table):
        """
        Obtiene los datos de una tabla previamente seteada.
        :param table: Tabla desde la que obtener datos.
        """
        pass

    def table_save_data(self, table, data):
        """
        Almacena datos recibidos en la tabla recibida.
        :param table: Tabla sobre la que insertar datos.
        :param data: Los datos a introducir.
        """
        pass

    def table_truncate(self, table):
        """
        Vacia completamente la tabla recibida.
        :param table:
        :return:
        """

    ##################### FIN REFACTORIZADO


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

    table_light = Table(
        'meteorology_light', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('value', Numeric(precision=15, asdecimal=True, scale=4)),
        Column('created_at', DateTime, default=datetime.datetime.utcnow),
    )

    meta.create_all(engine)

    ## Muestro tablas existentes
    print('Tablas en la DB: ', engine.table_names())

    def storageDB(self, table, datos):
        """
            Almacena el array de datos tomados por los sensores en la base de datos.
        """

        print('Guardando: ', table, datos)

        ## Inserto Datos
        try:
            stmt = table.insert().values(datos).return_defaults()
            result = self.connection.execute(stmt)
            # server_created_at = result.returned_defaults['created_at']
        except Exception:
            print('Ha ocurrido un problema al insertar datos', Exception)
            return None

        return result

    def getTable(self, table):
        """
        Recibe el modelo de la tabla y trae todas las entradas que contenga.
        :param table Modelo de tabla:
        :return Devuelve el resultado de la consulta:
        """
        return self.connection.execute(
            select([
                table.columns.value,
                table.columns.created_at,
            ])
        )

    def saveHumidity(self, datos):
        return self.storageDB(self.table_humidity, datos)

    def getHumidity(self):
        return self.getTable(self.table_humidity)

    def truncate_humidity(self):
        '''
        Elimina todos los registros en la tabla humidity
        '''
        print('Vaciando tabla humidity')
        self.truncate_table(self.table_humidity)

    def savePressure(self, datos):
        return self.storageDB(self.table_pressure, datos)

    def getPressure(self):
        return self.getTable(self.table_pressure)

    def truncate_pressure(self):
        '''
        Elimina todos los registros en la tabla pressure
        '''
        print('Vaciando tabla pressure')
        self.truncate_table(self.table_pressure)

    def saveTemperature(self, datos):
        return self.storageDB(self.table_temperature, datos)

    def getTemperature(self):
        return self.getTable(self.table_temperature)

    def truncate_temperature(self):
        '''
        Elimina todos los registros en la tabla temperature
        '''
        print('Vaciando tabla temperature')
        self.truncate_table(self.table_temperature)

    def saveLight(self, datos):
        return self.storageDB(self.table_light, datos)

    def getLight(self):
        return self.getTable(self.table_light)

    def truncate_light(self):
        '''
        Elimina todos los registros en la tabla light
        '''
        print('Vaciando tabla light')
        self.truncate_table(self.table_light)

    # TODO → Limitar obtenidos, ¿500? comprobar cuanto puede subir con JSON/POST
    def getAllData(self):
        '''
        Obtiene todos los datos de la base de datos para organizarlos
        y devolverlos.
        '''

        return {
            'humidity': self.getHumidity(),
            'pressure': self.getPressure(),
            'temperature': self.getTemperature(),
            'light': self.getLight(),
        }

    def truncate_all_sensors_data(self):
        self.truncate_humidity()
        self.truncate_pressure()
        self.truncate_temperature()
        self.truncate_light()

    def truncate_db(self):
        con = self.connection
        trans = con.begin()
        con.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in self.meta.sorted_tables:
            con.execute(table.delete())
        con.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()

    def truncate_table(self, table):
        self.connection.execute(table.delete())

    def closeConnection(self):
        print('Cerrando conexión con la Base de Datos')
        self.connection.close()
