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
# Clase para obtener datos y modelo de datos para DB con el sensor veml6070
# Sensor rayos UV
# Esta clase puede funcionar de forma autónoma, aún así también es extendida
# por clases hijas para seccionar el tipo de resultado obtenido y tratarse de
# forma independiente en aplicaciones que lo implementen.

import datetime
import busio
import board
import adafruit_veml6075
from Models.Sensors.AbstractModel import AbstractModel


class VEML6075(AbstractModel):
    table_name = 'table_uv'
    sensor = None

    def __init__(self, integration_time=100):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_veml6075.VEML6075(
            i2c, integration_time=integration_time)

    def get_uv_index(self):
        """
        Obtiene el índice UV.
        :return: Devuelve el índice UV.
        """
        value = self.sensor.uv_index

        return value if value >= 0.0 else 0.0

    def get_uva(self):
        """
        Obtiene el índice UVA.
        :return: Devuelve el índice UVA.
        """
        value = self.sensor.uva

        return value if value >= 0.0 else 0.0

    def get_uvb(self):
        """
        Obtiene el índice UVB.
        :return: Devuelve el índice UVA.
        """
        value = self.sensor.uvb

        return value if value >= 0.0 else 0.0

    def get_all_datas(self):
        """
        Obtiene la lectura del índice en bruto y el nivel de riesgo establecido.
        :return:
        """
        return {
            'uv_index': self.get_uv_index(),
            'uva': self.get_uva(),
            'uvb': self.get_uvb(),
        }

    def tablemodel(self):
        return {
            'uv_index': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'uva': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'uvb': {
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
        print('uv_index: ', self.get_uv_index())
        print('uva: ', self.get_uva())
        print('uvb: ', self.get_uvb())
        print("Integration time: %d ms" % self.sensor.integration_time)
        print('----------------- - -----------------')
