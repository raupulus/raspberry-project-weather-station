#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      raul@fryntiz.dev
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2020
# Project Name:
# Description:
#
# Dependencies:
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
# Modelo que implementa las clases básicas para el detector de rayo CJMCU-3935
# usando el chip AS3935 por i2c en raspberry


from RPi_AS3935.RPi_AS3935 import RPi_AS3935
import datetime
import time
import os
from Models.Sensors.AbstractModel import AbstractModel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class CJMCU3935(AbstractModel):
    table_name = 'table_lightning'
    sensor = None
    has_debug = False
    lightnings = []

    def __init__(self, address=0x03, bus=1, mode_debug=False, indoor=True, pin=26):
        # Marco el modo debug para el modelo.
        self.has_debug = mode_debug

        # Instancio el sensor como atributo de este modelo.
        self.sensor = RPi_AS3935(address, bus=bus)

        # Aplico parámetros de configuración para que trabaje el modelo.
        time.sleep(1)
        self.sensor.set_indoors(indoor)
        time.sleep(1)
        self.sensor.set_noise_floor(0)
        time.sleep(1)
        self.sensor.calibrate(tun_cap=0x0F)
        time.sleep(1)

        # Establezco parámetros de configuración en el modelo.
        self.pin = pin

        # Configuro el pin
        GPIO.setup(self.pin, GPIO.IN)

        # Inicio Callback para en cada detección registrar rayo
        GPIO.add_event_detect(self.pin, GPIO.RISING,
                              callback=self.handle_interrupt)

        if self.has_debug:
            self.msg(
                'Inicializado sensor de rayos y esperando detectar campos electromagnéticos para procesarlos.')

            """
            fo = open("log_rayos.log", "a+")
            str = 'Inicializado sensor de rayos y esperando detectar campos electromagnéticos para procesarlos.'
            fo.write(str + os.linesep)
            fo.close()
            """

    def handle_interrupt(self, channel):
        """
        Función que se ejecuta cuando detecta un rayo para registrarlo
        en el array de objetos con los datos registrados.
        :return:
        """
        time.sleep(0.003)
        sensor = self.sensor

        # Momento actual en formato timestamp.
        now = datetime.datetime.utcnow()

        reason = sensor.get_interrupt()

        if reason == 0x01:
            sensor.raise_noise_floor()

            if self.has_debug:
                print('El nivel de ruido es demasiado alto → Ajustando')

                self.msg('--------------------------')
                self.msg('El nivel de ruido es demasiado alto → Ajustando')
                self.msg('Timestamp: ' + str(now))
                self.msg('--------------------------')

                """
                fo = open("log_rayos.log", "a+")
                fo.write('--------------------------' + os.linesep)
                fo.write(
                    'El nivel de ruido es demasiado alto → Ajustando' + os.linesep)
                fo.write('Timestamp: ' + str(now) + os.linesep)
                fo.write('--------------------------' + os.linesep)
                fo.write('' + os.linesep)
                fo.close()
                """

        elif reason == 0x04:
            sensor.set_mask_disturber(True)

            if self.has_debug:
                self.msg('--------------------------')
                self.msg('Se ha detectado una perturbación → Enmascarándola')
                self.msg('Timestamp: ' + str(now))
                self.msg('--------------------------')

                """
                fo = open("log_rayos.log", "a+")
                fo.write('--------------------------' + os.linesep)
                fo.write(
                    'Se ha detectado una perturbación → Enmascarándola' + os.linesep)
                fo.write('Timestamp: ' + str(now) + os.linesep)
                fo.write('--------------------------' + os.linesep)
                fo.write('' + os.linesep)
                fo.close()
                """

        elif reason == 0x08:
            # En este punto, parece una detección correcta y la guardo.
            self.lightnings.append({
                "strike": self.strike(),
                "distance": self.distance(),
                "type": self.type(),
                "energy": self.energy(),
            })

            if self.has_debug:
                distance = sensor.get_distance()

                self.msg('--------------------------')
                self.msg('¡Se ha detectado un posible RAYO!')
                self.msg('Timestamp: ' + str(now))
                print('rayo detectado')
                self.msg(
                    "Está a " + str(distance) + "km de distancia. (%s)" % now)
                self.msg("------------------------")
                self.msg("All Data:")
                self.msg('Distance:' + str(self.sensor.get_distance()))
                self.msg('Interrupt:' + str(self.sensor.get_interrupt()))
                self.msg('Energy:' + str(self.sensor.get_energy()))
                self.msg('Noise Floor:' + str(self.sensor.get_noise_floor()))
                self.msg('In Indoor:' + str(self.sensor.get_indoors()))
                self.msg(
                    'Mask Disturber:' + str(self.sensor.get_mask_disturber()))
                self.msg('Dis.lco:' + str(self.sensor.get_disp_lco()))
                self.msg('--------------------------')

                # Añado información al archivo de log común
                """
                fo = open("log_rayos.log", "a+")
                fo.write('--------------------------' + os.linesep)
                fo.write('¡Se ha detectado un posible RAYO!' + os.linesep)
                fo.write('Timestamp: ' + str(now) + os.linesep)
                fo.write('Distance:' +
                         str(self.sensor.get_distance()) + os.linesep)
                fo.write('Interrupt:' +
                         str(self.sensor.get_interrupt()) + os.linesep)
                fo.write('Energy:' + str(self.sensor.get_energy()) + os.linesep)
                fo.write('Noise Floor:' +
                         str(self.sensor.get_noise_floor()) + os.linesep)
                fo.write('In Indoor:' +
                         str(self.sensor.get_indoors()) + os.linesep)
                fo.write('Mask Disturber:' +
                         str(self.sensor.get_mask_disturber()) + os.linesep)
                fo.write('Dis.lco:' + str(self.sensor.get_disp_lco()) + os.linesep)
                fo.write('--------------------------' + os.linesep)
                fo.write('' + os.linesep)
                fo.close()

                # Añado registro a un archivo JSON (timestamp, distance, energy)
                fo = open("rayos.csv", "a+")
                fo.write(os.linesep)
                fo.write(str(self.sensor.get_energy()) + ';')  # Energy
                fo.write(str(self.sensor.get_distance()) + ';')  # Distance
                fo.write(str(now) + ';')  # Timestamp
                fo.close()
                """
        else:
            if self.has_debug:
                self.msg('Se ha detectado algo no controlado aún')

                """
                fo = open("log_rayos.log", "a+")
                fo.write('--------------------------' + os.linesep)
                fo.write('Se ha detectado algo no controlado aún' + os.linesep)
                fo.write('Timestamp: ' + str(now) + os.linesep)
                fo.write('El código *reason* es:' + str(reason) + os.linesep)
                fo.write('--------------------------' + os.linesep)
                fo.write('' + os.linesep)
                fo.close()
                """

    def strike(self):
        return None

    def distance(self):
        return self.sensor.get_distance()

    def type(self):
        return self.sensor.get_interrupt()

    def energy(self):
        return self.sensor.get_energy()

    def get_all_datas(self):
        """
        Devuelve una lista con todas las lecturas si se han podido tomar.
        :return:
        """

        if self.lightnings and len(self.lightnings):
            reads = self.lightnings
            self.lightnings = []

            return reads

        return None

    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        return {
            'strike': {
                'type': 'String',
                'params': {},
                'others': None,
            },
            'distance': {
                'type': 'String',
                'params': {},
                'others': None,
            },
            'type': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'energy': {
                'type': 'String',
                'params': {},
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
        datas = self.get_all_datas()

        """
        if datas:
            print('Pintando debug para CJMCU 3935')

            for sensor, data in datas.items():
                print('Valor del sensor ' + str(sensor) + ': ' + str(data))
        """
