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
# Clase que extiende de CJMCU811 para representar el modelo del sensor solo
# para la parte de ECO2
import datetime
from time import sleep

from Models.Sensors.CJMCU811 import CJMCU811


class CJMCU811_eco2(CJMCU811):
    table_name = 'table_eco2'

    ## Marca con el momento en el que comienza a tomar datos.
    started_at = datetime.datetime.now()

    def get_all_datas(self):
        """
        Devuelve un diccionario con los datos (coincidiendo con el tablemodel)
        según lo tomado con el sensor.
        """
        sleep(1)

        minutes = (datetime.datetime.now() - self.started_at).total_seconds() / 60.0

        ## Espera de 20 minutos para calibrar sensor.
        if minutes < 20:
            print('Calibrando CJMU811_eco2', self.get_eco2())
            return None

        return {
            'value': self.get_eco2(),
        }

    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
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
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        print('El valor ECO2 actual es: ', self.get_eco2())
