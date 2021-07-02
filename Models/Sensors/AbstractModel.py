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
# Modelo que implementa las clases básicas para todos los sensores y asegurar
# de esta forma que funciona la aplicación al cargarlos dinámicamente.

from abc import ABC, abstractmethod


class AbstractModel(ABC):
    # Parámetros para devolver datos del modelo de base de datos
    @property
    def table_name(self):
        pass

    @abstractmethod
    def get_all_datas(self):
        """
        Devuelve un diccionario con los datos (coincidiendo con el tablemodel)
        según lo tomado con el sensor.
        """
        pass

    @abstractmethod
    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        pass

    @abstractmethod
    def debug(self):
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        pass

    def msg(self, message):
        """
        Muestra mensajes solo cuando está activado el modo debug.
        :param message:
        :return:
        """
        if not self.has_debug:
            return

        print('\n')
        print(message)
