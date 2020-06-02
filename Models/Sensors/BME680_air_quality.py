#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2020
#
# Revision 0.01 - File Created
# Additional Comments:

# @copyright  Copyright © 2020 Raúl Caro Pastorino
# @license    https://wwww.gnu.org/licenses/gpl.txt

# Copyright (C) 2020  Raúl Caro Pastorino
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
# Clase que extiende de BME680 para representar el modelo del sensor solo
# para la parte de temperatura.
import datetime

from Models.Sensors.BME680 import BME680


class BME680_air_quality(BME680):
    table_name = 'table_air_quality'

    def get_all_datas(self):
        """
        Devuelve un diccionario con los datos (coincidiendo con el tablemodel)
        según lo tomado con el sensor.
        """
        return {
            'gas_resistance': self.read_gas_resistance(),
            'air_quality': self.read_air_quality(),
        }

    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        return {
            'gas_resistance': {
                'type': 'Numeric',
                'params': {
                    'precision': 22,
                    'asdecimal': True,
                    'scale': 11
                },
                'others': None,
            },
            'air_quality': {
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
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        print('La Resistencia de gas es de: ', self.read_gas_resistance())
        print('La Calidad actual del aire es: ', self.read_air_quality())
