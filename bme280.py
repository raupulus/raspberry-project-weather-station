#!/usr/bin/python
# --------------------------------------
#  Test bme.280
#
# Author : Raúl Caro Pastorino
# Date   : 10/07/2019
#
# --------------------------------------

from Models.Sensors.BME280 import BME280

def main ():
    bme280 = BME280()

    (chip_id, chip_version) = bme280.readBME280ID()
    print("Chip ID     :", chip_id)
    print("Version     :", chip_version)

    temperature, pressure, humidity = bme280.readBME280All()

    print("Temperature : ", temperature, "ºC")
    print("Pressure : ", pressure, "hPa")
    print("Humidity : ", humidity, "%")


if __name__ == "__main__":
    main()
