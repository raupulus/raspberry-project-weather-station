#!/usr/bin/python3
import time

import RPi.GPIO as GPIO
import math
import time
from _thread import start_new_thread

class Anemometer():
    """
    Esta clase representa un sensor que envía pulsos digitales a un pin GPIO
    conociendo de esta forma las vueltas completas que realiza.

    Mediante el método generateWind() se actualizarán los valores de la clase
    calculando y limpiándolos.
    De esta forma queda el modelo para el anemómetro separado de las peticiones
    en tiempo pudiendo pedirse cada una en intervalos distintos se calculará
    siempre la direncia de tiempo dinámicamente.

    La clase quedará siempre tomando datos y se podrán calcular en cualquier
    momento usando para ello los datos recopilados desde la última vez.
    """

    ## Cantidad de pulsos (cierres de circuito) que tiene por vuelta completa.
    pulsos_por_vuelta = 2

    ## Pin sobre el que se toman las lecturas/pulsos digitales.
    PIN = 7

    ## Radio del anemómetro en centímetros.
    RADIO = 9

    ## Pulsos obtenidos en el periodo de tiempo.
    pulsos = 0

    ## Los pulsos totales en el tiempo completo de ejecución.
    pulsos_totales = 0

    ## Velocidad actual de la velocidad del viento en metros por segundos.
    wind_speed = 0

    ## Suma de todas las velocidades (para sacar media con pulsos_totales)
    wind_speed_total = 0

    ## Recuento de todas las veces que se ha calculado los datos.
    wind_recount = 0

    ## Velocidad máxima.
    wind_max = 0

    ## Velocidad mínima.
    wind_min = 0

    ## Velocidad media.
    wind_average = 0

    ## Valores anteriores registrados.
    old_pulsos = 0
    old_wind_max = 0
    old_wind_min = 0
    old_wind_average = 0
    old_s_time = time.time()
    old_time_diff = 0

    ## Contador de tiempo entre cálculos.
    s_time = time.time()
    time_diff = 0  ## Diferencia de tiempo entre comprobaciones

    ## Parámetros para devolver datos del modelo de base de datos
    table_name = 'table_anemometer'

    ## Tiempo en seg. que tarda entre mediciones para recalcular estadísticas
    s_mediciones = 5

    def __init__(self, pin=7, RADIO = 9, pulsos_vuelta=2, s_mediciones=5):
        self.PIN = pin
        self.RADIO = RADIO
        self.pulsos_por_vuelta = pulsos_vuelta
        self.s_mediciones = s_mediciones
        self.killed = False
        self.connect()

    def connect(self):
        """
        Inicializa la conexión con el sensor escuchando pulsos y asignando
        eventos para detectarlos.
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.sumar_pulso,
                              bouncetime=5)

    def disconnect(self):
        """
        Para la conexión con el sensor.
        """
        pass

    def sumar_pulso(self, pin):
        """
        Aumenta el contador de pulsos recibidos por el anemómetro.
        """
        self.pulsos += 1

    def pulsos_to_meters_second(self):
        """
        Convierte pulsos en metros por segundo
        velocidad = distancia / tiempo
        velocidad = (vueltas * circunferencia) / tiempo
        velocidad = ((pulsos / pulsos por vuelta) * (2 * pi * radio)) / tiempo

        Anteriormente se usaba:
            val = self.imp_per_sec
            # y = 8E-09x5 - 2E-06x4 + 0,0002x3 - 0,0073x2 + 0,4503x + 0,11

            calc = float("8e-9") * math.pow(val, 5) - float("2e-6") * \
                math.pow(val, 4) + float("2e-4") * math.pow(val, 3) - float("7.3e-3") * \
                math.pow(val, 2) + 0.4503 * val + 0.11

            if calc < 0.2:
                calc = 0

        :return: m/s
        """

        ## Parámetros base
        pulsos = int(self.pulsos)
        pulsos_por_vuelta = int(self.pulsos_por_vuelta)
        radio = float(self.RADIO)

        ## Cálculo de tiempo desde que inició el contador de pulsos
        time_now = time.time()
        time_diff = time_now - self.s_time

        ## Parámetros calculados
        vueltas = (pulsos / pulsos_por_vuelta)
        circunferencia = 2 * math.pi * (radio / 10)
        velocidad = (circunferencia * vueltas) / time_diff

        ## Reseteo pulsos
        self.old_pulsos = pulsos
        self.pulsos_totales += self.pulsos
        self.pulsos = 0
        self.old_time_diff = self.time_diff
        self.time_diff = time_diff
        self.old_s_time = self.s_time
        self.s_time = time.time()

        return velocidad

    def generate_wind(self):
        """
        Genera los valores para el viento actual, máximo, mínimo y media.
        """

        ## Aumento el contador, será reseteado al llamar a get_all_datas().
        self.wind_recount += 1

        ## Valores anteriores registrados.
        self.old_wind_max = self.wind_max
        self.old_wind_min = self.wind_min
        self.old_wind_average = self.wind_average

        ## Velocidad actual de la velocidad del viento en metros por segundos.
        self.wind_speed = self.pulsos_to_meters_second()

        ## Velocidad máxima.
        if self.wind_speed > self.wind_max:
            self.wind_max = self.wind_speed

        ## Velocidad mínima.
        if (self.wind_min == 0) or (self.wind_speed < self.wind_min):
            self.wind_min = self.wind_speed

        ## Velocidad media.
        self.wind_speed_total += self.wind_speed
        if self.pulsos_totales > 0:
            self.wind_average = self.wind_speed_total / self.wind_recount
        else:
            self.wind_average = 0

    def get_all_datas(self):
        """
        Devuelve todos los datos del modelo para el último periodo de medición.
        """

        ## Almaceno todos los datos a devolver.
        data = {
            'wind_speed': self.wind_speed,
            'wind_average': self.wind_average,
            'wind_min': self.wind_min,
            'wind_max': self.wind_max,
        }

        ## Limpio los datos del modelo.
        self.pulsos = 0
        self.pulsos_totales = 0
        self.wind_speed = 0
        self.wind_speed_total = 0
        self.wind_max = 0
        self.wind_min = 0
        self.wind_average = 0
        self.s_time = time.time()
        self.time_diff = 0
        self.wind_recount = 0

        ## Devuelvo los datos.
        return data

    def start_read(self):
        """
        Comienza la lectura de datos cada un periodo de tiempo para hacer los
        cálculos de los eventos en GPIO recibidos durante ese tiempo.
        Este hilo queda abierto para que al consultar al modelo haya permanecido
        constantemente almacenando datos y sea inmediata su devolución sin
        necesitar realizar los cálculos en ese momento.
        """

        def read_and_sleep():
            """
            Esta función actualiza las estadísticas de las lecturas cada
            cierto tiempo en bucle.
            """
            while True:
                ## Si se ha marcado para detener lecturas, se aborta hilo.
                if self.killed:
                    raise SystemExit
                self.generate_wind()
                time.sleep(self.s_mediciones)

        self.killed = False
        start_new_thread(read_and_sleep, ())

    def stop_read(self):
        """
        Para la lectura de datos y cierra el hilo de trabajo con el anemómetro.
        """
        print('Cerrando hilo de lectura de datos')
        self.killed = True


    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """

        return {
            'name': self.table_name,
            'columns': {
                'id': {
                    'type': 'Integer',
                    'params': {
                        'primary_key': True,
                        'autoincrement': True,
                    }
                },
                'wind_speed': {
                    'type': 'Numeric',
                    'params': {
                        'precision': 15,
                        'asdecimal': True,
                        'scale': 4
                    }
                },
                'wind_average': {
                    'type': 'Numeric',
                    'params': {
                        'precision': 15,
                        'asdecimal': True,
                        'scale': 4
                    }
                },
                'wind_min': {
                    'type': 'Numeric',
                    'params': {
                        'precision': 15,
                        'asdecimal': True,
                        'scale': 4
                    }
                },
                'wind_max': {
                    'type': 'Numeric',
                    'params': {
                        'precision': 15,
                        'asdecimal': True,
                        'scale': 4
                    }
                },
                'created_at': {
                    'type': 'DateTime',
                    'params': {
                        'default': 'datetime.datetime.utcnow'
                    }
                }
            },
        }

    def debug(self):
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        print('Pulsos Totales:', self.pulsos_totales)
        print('Pulsos en esta medición:', self.old_pulsos)
        print('Tiempo recopilando pulsos:', self.old_time_diff)
        print('Metros por segundos:', self.wind_speed)
        print('Media de todas las capturas:', self.wind_average)
        print('Viento mínimo:', self.wind_min)
        print('Viento máximo:', self.wind_max)
        time.sleep(5)
