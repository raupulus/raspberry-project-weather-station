import os
import time


def rpi_cpu_temp():
    """
    Devuelve la temperatura de la CPU de la Raspberry
    """
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=","").replace("\'C", ""))
