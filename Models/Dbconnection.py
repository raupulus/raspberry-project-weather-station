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


class Dbconnection:
    # Datos desde .env
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

    tables = {}

    def table_set_new(self, tablename, parameters):
        """
        Almacena una nueva tabla en el array de tablas.
        :param tablename: Nombre de la tabla.
        :param parameters: Parámetros para cada columna.
        """
        columns = []

        # Seteo la columna **id**
        columns.append(Column('id', Integer, primary_key=True, autoincrement=True))

        # Seteo el resto de columnas.
        for name, datas in parameters.items():
            data_type = datas['type']
            data_params = datas['params']
            type_column = None
            other_data = datas['others']

            # Creo el campo según el tipo de dato.
            if data_type == 'Numeric':
                type_column = Numeric(**data_params)
            elif data_type == 'DateTime':
                type_column = DateTime
            elif data_type == 'Integer':
                type_column = Integer
            elif data_type == 'String':
                type_column = String(**data_params)

            if datas['others']:
                columns.append(Column(name, type_column, **other_data))
            else:
                columns.append(Column(name, type_column))

        # Creo la tabla con las columnas antes seteadas.
        self.tables[tablename] = Table(
            tablename,
            self.meta,
            *columns,
        )

        self.meta.create_all(self.engine)

        print('Tablas en la DB: ', self.engine.table_names())

    def table_get_data(self, tablename):
        """
        Obtiene los datos de una tabla previamente seteada.
        :param tablename: Nombre de la tabla desde la que obtener datos.
        """

        table = self.tables[tablename]

        # Ejecuto la consulta para traer las tuplas de la tabla completa
        return self.connection.execute(
            select([table])
        ).fetchall()

    def table_save_data(self, sensorname, tablename, params):
        """
        Almacena datos recibidos en la tabla recibida.
        :param sensorname: Nombre del sensor sobre el que se trabaja.
        :param tablename: Nombre de la tabla en la que guardar.
        :param params: Diccionario con los parámetros del sensor.
        """

        table = self.tables[tablename]

        print('Guardando en DB: ', table, params)

        # Inserto Datos
        try:
            stmt = table.insert().values(params).return_defaults()
            result = self.connection.execute(stmt)
            # server_created_at = result.returned_defaults['created_at']
        except Exception as e:
            print('Ha ocurrido un problema al insertar datos', e.__class__.__name__)
            return None

    def table_truncate(self, tablename):
        """
        Vacia completamente la tabla recibida.
        :param tablename: Nombre de la tabla.
        """
        self.connection.execute(self.tables[tablename].delete())

    def get_all_data(self):
        '''
        Obtiene todos los datos de la base de datos para todos los
        sensores y los devuelve organizados.
        '''
        pass

    def truncate_all_sensors_data(self):
        """
        Limpia todas las tablas para los sensores establecidos.
        """
        pass

    def truncate_db(self):
        """
        Limpia la Base de datos completamente para comenzar a recopilar
        información desde una base de datos saneada/limpia.
        """
        con = self.connection
        trans = con.begin()
        con.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in self.meta.sorted_tables:
            con.execute(table.delete())
        con.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()

    def close_connection(self):
        print('Cerrando conexión con la Base de Datos')
        self.connection.close()
