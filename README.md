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
- postgresql

## Módulos python

- python3-requests
- sqlalchemy para python 3
- python3-dotenv
- python3-smbus
- python3-rpi.gpio
- python3-pip

## Models

- BME280 → Modelo que representa al sensor bosh BME280 para medir 
temperatura, humedad y presión.

## Instalación

### Crear usuario y base de datos sensor_data

sudo -u postgres createuser pi
sudo -u postgres createdb -O pi -T template1 sensor_data

### Clonar repositorio

git clone https://gitlab.com/fryntiz/raspberry-weather-station.git


### Instalar dependencias

sudo apt install python3-dotenv python3-sql python3-sqlalchemy \ 
    python3-psycopg2 python3-smbus python3-requests python3-rpi.gpio \ 
    python3-pip 
    
#### Dependencias para pantalla oled 128x64 con chip ssd1306    

pip3 install Adafruit_SSD1306 Adafruit_GPIO Pillow

### Dar permisos y propietario

### Asignar tarea cron