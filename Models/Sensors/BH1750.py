#!/usr/bin/python
# --------------------------------------
#  Read data from a digital light sensor.
#
#  Official datasheet available from :
#  https://www.mouser.com/ds/2/348/bh1750fvi-e-186247.pdf
#
# Author : Raúl Caro Pastorino
# Date   : 01/08/2019
#
# --------------------------------------
import datetime

import smbus
import time


class BH1750:
    DEVICE = 0x23      # Dirección i2c
    POWER_DOWN = 0x00  # Estado inactivo
    POWER_ON = 0x01    # Power on
    RESET = 0x07       # Reset data register value
    ONE_TIME_HIGH_RES_MODE = 0x20
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    ## Parámetros para devolver datos del modelo de base de datos
    table_name = 'table_light'

    def __init__(self, device=0x23):
        self.DEVICE = device

    def data_to_decimal(self, data):
        """
        Convierte los datos de 2 bytes que entra en "data" a número decimal.
        :param data:
        :return:
        """
        return ((data[1] + (256 * data[0])) / 1.2)

    def read_light(self):
        """
        Realiza la lectura del sensor.
        :return:
        """
        data = self.bus.read_i2c_block_data(
            self.DEVICE,
            self.ONE_TIME_HIGH_RES_MODE
        )

        return self.data_to_decimal(data)

    def read_light_format_string(self):
        """
        Devuelve la cantidad de lux formateado en una cadena.
        :return:
        """
        lux = self.read_light()
        str_lux = 'Light Level : ' + str(lux) + " lux"

        return str_lux

    def get_all_datas(self):
        """
        Devuelve un diccionario con los datos (coincidiendo con el tablemodel)
        según lo tomado con el sensor.
        """
        return {
            'value': self.read_light(),
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
        print('Cantidad de luz actual:', self.read_light())
        time.sleep(5)
