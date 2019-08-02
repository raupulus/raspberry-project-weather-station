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
import smbus
import time


class BH1750:
    DEVICE = 0x23      # Default device I2C address
    POWER_DOWN = 0x00  # No active state
    POWER_ON = 0x01    # Power on
    RESET = 0x07       # Reset data register value
    ONE_TIME_HIGH_RES_MODE = 0x20
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

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
