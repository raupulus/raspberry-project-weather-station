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

## Cargo archivos de configuración desde .env
from dotenv import load_dotenv
load_dotenv(override=True)

## Importo el modelo que interactua con la base de datos.
from Models.Dbconnection import Dbconnection


#######################################
# #             Variables           # #
#######################################
sleep = time.sleep


#######################################
# #             Funciones           # #
#######################################


## TODO → Esta función quedará en bucle tomando datos cada 30 segundos.
def main():
    ## Abro conexión con la base de datos.
    dbconnection = Dbconnection()

    ## Instancio todas las clases
    ## TODO → Refactorizar de forma que la toma de datos y guardado se pueda
    ## repetir para un sensor concreto si este falla al tomar dato o guardar.
    #bme280 = BME280()

    ## Leo todos los sensores
    #temperature, pressure, humidity = bme280.readBME280All()
    #raspberryTempCPU = func.rpi_cpu_temp()
    temperature, pressure, humidity = [99, 88, 77]

    ## Almaceno los datos en la DB
    ## TODO → Comprobar si guardado falla para retomar medición
    dbconnection.saveHumidity({'value': temperature});
    dbconnection.savePressure({'value': pressure});
    dbconnection.saveTemperature({'value': humidity});


if __name__ == "__main__":
    main()
