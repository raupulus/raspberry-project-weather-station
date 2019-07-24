# raspberry-weather-station

Proyecto de estación meteorológica con Raspberry Pi

Este proyecto se describe para la distribución Raspbian stable, con otros 
sistemas operativos o distribuciones pueden variar dependencias y tal vez
el código.

## Hardware 

El hardware con el que ha sido utilizado y probado, esto no descarta funcionar
en otro tipo de hardware similar o con pequeñas modificaciones.

- Raspberry PI 4
- Sensor bosh BME280


## Software

- python 3.7
- sqlalchemy para python 3
- python3-dotenv
- postgresql

## Models

- BME280 → Modelo que representa al sensor bosh BME280 para medir 
temperatura, humedad y presión.

## Instalación

### Crear base de datos sensor_data

sudo -u postgres createdb -O pi -T template1 sensor_data

### Clonar repositorio

git clone https://gitlab.com/fryntiz/raspberry-weather-station.git


### Instalar dependencias

sudo apt install python3-dotenv python3-sql python3-sqlalchemy python3-psycopg2

### Dar permisos y propietario

### Asignar tarea cron