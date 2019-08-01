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
# # Conexión a la base de datos.
##

#######################################
# #       Importar Librerías        # #
#######################################

import datetime

## Cargo archivos de configuración desde .env
from dotenv import load_dotenv
load_dotenv(override=True)
import os
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

#######################################
# #             Variables           # #
#######################################
sleep = time.sleep

#######################################
# #             Funciones           # #
#######################################


class Apiconnection:
    API_URL = os.getenv("API_URL")
    API_TOKEN = os.getenv("API_TOKEN")

    def requests_retry_session (
            retries=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            session=None,
    ):
        """
        Crea una sesión para reintentar envío HTTP cuando falla.
        :param backoff_factor:
        :param status_forcelist:
        :param session:
        :return:
        """
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def send(self, path, datas_json):
        '''
        Envía la petición a la API.
        :param path: Directorio dentro de la api (ex: /api/ws/humidity)
        '''

        url = self.API_URL
        token = self.API_TOKEN
        full_url = url + path

        data = {
            'data': datas_json,
            'info': 'Enviado desde Raspberry Pi'
        }

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'Authorization': 'Bearer ' + str(token),
        }

        try:
            req = self.requests_retry_session().post(
                full_url,
                data=json.dumps(data),
                headers=headers,
                timeout=30
            )

            print('Código de envío: ', req.status_code)
            print('Recibido: ', req.text)
        except Exception as e:
            print('Ha fallado la petición http :', e.__class__.__name__)
            sleep(20)

    def parseToJson(self, datas):
        return json.dumps(
            [
                {
                    'value': str(d.value),
                    'created_at': str(d.created_at)
                } for d in datas
            ],
            default=None,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
        )

    def upload_humidity(self, datas):
        if datas:
            print('Subiendo humidity')
            datas_json = self.parseToJson(datas)
            #print(datas_json)
            self.send('/ws/humidity/add-json', datas_json)

    def upload_pressure(self, datas):
        if datas:
            print('Subiendo pressure')
            datas_json = self.parseToJson(datas)
            #print(datas_json)
            self.send('/ws/pressure/add-json', datas_json)

    def upload_temperature(self, datas):
        if datas:
            print('Subiendo temperature')
            datas_json = self.parseToJson(datas)
            #print(datas_json)
            self.send('/ws/temperature/add-json', datas_json)

    def upload_light(self, datas):
        if datas:
            print('Subiendo light')
            datas_json = self.parseToJson(datas)
            #print(datas_json)
            self.send('/ws/light/add-json', datas_json)
