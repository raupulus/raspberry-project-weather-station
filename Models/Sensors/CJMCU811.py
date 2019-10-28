#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2019/10/27
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

# #           Descripción           # #
# Clase para obtener datos y modelo de datos para DB con el sensor CJMCU811
# Sensor de CO2 y TVOC
# Esta clase puede funcionar de forma autónoma, aún así también es extendida
# por clases hijas para seccionar el tipo de resultado obtenido y tratarse de
# forma independiente en aplicaciones que lo implementen.

import datetime
import time
import board
import busio
import adafruit_ccs811
from Models.Sensors.AbstractModel import AbstractModel


class CJMCU811(AbstractModel):
    table_name = 'table_co2'
    sensor = None

    def __init__(self, mode=None):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_ccs811.CCS811(i2c)

        if mode:
            print('Modificando modo de CJMCU811 a:', mode)
            self.sensor.drive_mode(mode)

    def get_eco2(self):
        """
        Obtiene las partículas de CO2, puede medir máximo 8192ppm.
        :return: Devuelve las partículas de CO2.
        """
        value = self.sensor.eco2
        value = float(value if value is not None else 0)
        return value if 400.0 <= value <= 8192.0 else 400.0

    def get_tvoc(self):
        """
        Obtiene las partículas de TVOC, puede medir máximo 1187ppb.
        :return: Devuelve las partículas de TVOC.
        """
        value = self.sensor.tvoc
        value = float(value if value is not None else 0)
        return value if 0.0 <= value <= 1187.0 else 0.0

    def get_all_datas(self):
        """
        Obtiene la lectura de CO2 y TVOC.
        :return:
        """
        return {
            'eco2': self.get_eco2(),
            'tvoc': self.get_tvoc(),
        }

    def set_temperature_humidity(self, humidity, temperature):
        """
        Establece la humedad y temperatura para calcular las variaciones en
        las lecturas del sensor.
        """
        self.sensor.set_environmental_data(humidity, temperature)

    def tablemodel(self):
        return {
            'eco2': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'tvoc': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'created_at': {
                'type': 'DateTime',
                'params': None,
                'others': {
                    'default': datetime.datetime.utcnow
                },
            },
        }

    def debug(self):
        print('DRIVE_MODE:', self.sensor.drive_mode)
        print('eco2: ', self.get_eco2(), 'PPM')
        print('tvoc: ', self.get_tvoc(), 'PPB')
        print('----------------- - -----------------')
