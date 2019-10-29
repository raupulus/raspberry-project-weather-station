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

# #           Descripción           # #
# Clase para obtener datos y modelo de datos para DB con el sensor veml6070
# Sensor rayos UV

import datetime
import busio
import board
import adafruit_veml6070
from Models.Sensors.AbstractModel import AbstractModel


class VEML6070(AbstractModel):
    table_name = 'table_uva'
    uv = ''

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.uv = adafruit_veml6070.VEML6070(i2c)
        # Alternative constructors with parameters
        # uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_1_T')
        # uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_HALF_T', True)

    def read_uv(self):
        """
        Obtiene la lectura UV en bruto y el nivel de riesgo establecido.
        :return:
        """
        uv_raw = self.uv.uv_raw
        risk_level = self.uv.get_index(uv_raw)

        return uv_raw, risk_level

    def get_all_datas(self):
        uv_raw, risk_level = self.read_uv()
        return {
            'value': uv_raw,
        }

    def tablemodel(self):
        return {
            'value': {
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
        uv_raw, risk_level = self.read_uv()
        print('Reading: {0} | Risk Level: {1}'.format(uv_raw, risk_level))
