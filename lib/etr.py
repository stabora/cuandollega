#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import datetime
import sys
from lib.util import Util


class ETR:

    config = Util.load_config()
    proxy = config['proxy']
    url_sms = config['url_sms']
    url_data = config['url_data']
    timeout = config['timeout']

    lines_ids = {
        '101': '1,2',
        '102': '3,4',
        '103': '5,6',
        '106': '7, 8',    # 106 Negro / Rojo
        '107': '9, 10',    # 107 Negro - Distrito Sur / 107 Rojo - Necochea
        '110': '11',
        '112': '12,13',
        '113': '14',
        '115': '15',
        '116': '16',
        '120': '17',
        '121': '18',
        '122': '19,20',
        '123': '21',
        '125': '22',
        '126': '23,24',
        '127': '25',
        '128': '26,27',
        '129': '28',
        '130': '29',
        '131': '30',
        '132': '31',
        '133': '32,33',
        '134': '34',
        '135': '35',
        '136': '36',
        '137': '37',
        '138': '38,39',
        '139': '40,41',
        '140': '43',
        '141': '44',
        '142': '45,46,47',
        '143': '48,49',
        '144': '50,51',
        '145': '52,53',
        '146': '54,55',
        '153': '56,57,58',
        # '35-9': '59, 60, 61',    # 35/9 Negro / Rojo / Verde (no habilitados)
        'ENO': '63',    # Enlace NorOeste
        'K': '64',
        'LC': '65',
        'RC': '66'
    }

    @staticmethod
    def __query_sms(line, stop):
        response = None

        if line[0].isdigit():
            line = re.sub('[^0-9]', '', line)

        params = {
          'linea': line,
          'parada': stop
        }

        response = ETR.__query_server(ETR.url_sms, params)

        return response

    @staticmethod
    def __get_line_id(line):
        line = str(line)

        if line in ETR.lines_ids:
            return ETR.lines_ids[line]

    @staticmethod
    def __query_server(url, params=None):
        try:
            url_params = urllib.urlencode(params) if params else None

            if ETR.proxy:
                proxy_handler = urllib2.ProxyHandler({'http': ETR.proxy})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)

            ws = urllib2.urlopen(url, url_params, timeout=ETR.timeout)
            response = ws.read()
            ws.close()

            return response

        except Exception, e:
            if hasattr(e, 'reason'):
                text = 'Error al intentar abrir la URL del host: ' + str(e.reason)
            else:
                text = 'Error al intentar abrir la URL del host: Tiempo de espera agotado'

            try:
                Util.write_error_log(getattr(params, 'linea'), getattr(params, 'parada'), text)
            except Exception, e:
                print 'Error al intentar guardar error en el registro.'

            return text

    @staticmethod
    def __parse_response(line, stop, text):
        response = ''
        incoming = False

        pattern_incoming = re.compile(r'(.+)?Linea\s(.+):\s([0-9]+)min.?\.?\s([0-9]+)mts.?\.?')
        pattern_idle = re.compile(r'(.+)?Linea\s(.+):\sProx.(.+)([0-9]{2}:[0-9]{2})hs\sllega\s([0-9]+)min\.')

        if text:
            results = text.split(' - ')

        response = '--- Consulta realizada a las ' + datetime.datetime.now().strftime("%H:%M") + ' ---\n\n'

        for result in results:
            if result:
                match_incoming = pattern_incoming.match(result)
                match_idle = pattern_idle.match(result)

                if match_incoming:
                    if line in match_incoming.group(2):
                        response += 'Línea: ' + match_incoming.group(2) + '\n'
                        response += 'Parada: ' + str(stop) + '\n'
                        response += 'Estado: EN CAMINO\n'
                        response += 'Tiempo de llegada: ' + match_incoming.group(3) + ' minutos\n'
                        response += 'Distancia: ' + match_incoming.group(4) + 'mts.\n\n'

                        incoming = True
                elif match_idle:
                    if line in match_idle.group(2):
                        response += 'Línea: ' + match_idle.group(2) + '\n'
                        response += 'Parada: ' + str(stop) + '\n'
                        response += 'Estado: EN ESPERA\n'
                        response += 'Hora de salida: ' + match_idle.group(4) + '\n\n'
                else:
                    response += 'Línea: ' + line + '\n'
                    response += 'Parada: ' + str(stop) + '\n'
                    response += 'Respuesta no procesada: ' + result + '\n\n'

        return response, incoming

    @staticmethod
    def list_lines():
        lines = []
        lines_list = ''
        cont = 0

        for line in sorted(ETR.lines_ids):
            lines_list += line + '\t'
            lines += [line]
            cont += 1

            if cont % 4 == 0:
                lines_list += '\n'

        lines_list += '\n'

        return lines_list, lines

    @staticmethod
    def get_line_streets(line):
        response = None

        line_id = ETR.__get_line_id(line)

        if line_id:
            params = {
                'accion': 'getCalle',
                'idLinea': line_id
            }

            response = ETR.__query_server(ETR.url_data + '?' + urllib.urlencode(params))

        return response

    @staticmethod
    def get_line_intersections(line, street):
        response = None
        line_id = ETR.__get_line_id(line)

        if line_id:
            params = {
                'accion': 'getInterseccion',
                'idLinea': line_id,
                'idCalle': street
            }

            response = ETR.__query_server(ETR.url_data + '?' + urllib.urlencode(params))

        return response

    @staticmethod
    def get_line_stops(line, street, intersection):
        response = None

        line_id = ETR.__get_line_id(line)

        if line_id:
            params = {
                'accion': 'getInfoParadas',
                'idLinea': line_id,
                'idCalle': street,
                'idInt': intersection
            }

            response = ETR.__query_server(ETR.url_data + '?' + urllib.urlencode(params))

        return response

    @staticmethod
    def check_line_schedule(line, stop):
        response = ETR.__query_sms(line, stop)
        Util.write_log_file(line, stop, response)
        response, incoming = ETR.__parse_response(line, stop, response)

        return response, incoming

    @staticmethod
    def interactive_mode_wizard():
        print 'Consulta \'¿Cuándo llega?\' del ETR - Asistente de consulta interactiva.\n'

        lines_list, lines = ETR.list_lines()
        print lines_list

        line = raw_input("Línea: ")

        if not line:
            print 'Debe ingresar una línea para poder continuar.'
            sys.exit()

        line = line.upper()

        if line not in lines:
            print 'La línea ingresada no es válida.'
            sys.exit()

        print '\nRecuperando las calles para la línea seleccionada. Espere, por favor...'

        str_streets = ETR.get_line_streets(line)

        if str_streets == 'error':
            print 'Error al obtener el listado de calles para la línea ingresada.'
            sys.exit()
        else:
            if str_streets:
                try:
                    streets, streets_list = Util.generate_streets_list(str_streets)
                    print streets_list
                except Exception:
                    print 'Error al obtener el listado de calles. Inténtenlo nuevamente.'
                    sys.exit()
            else:
                print 'No se encontraron calles para la línea ingresada.'
                sys.exit()

        street = raw_input("Calle: ")

        if not street:
            print 'Debe seleccionar una calle para poder continuar.'
            sys.exit()
        else:
            try:
                street = int(street) - 1
            except Exception:
                print 'El valor ingresado no tiene un formato válido.'
                sys.exit()

            if street > len(streets) - 1:
                print 'El valor ingresado no corresponde a una calle válida.'
                sys.exit()

            print '\nRecuperando las intersecciones para la calle seleccionada. Espere, por favor...'

            str_intersections = ETR.get_line_intersections(line, int(streets[int(street)]['id']))

            if str_intersections:
                try:
                    intersections, intersections_list = Util.generate_streets_list(str_intersections)
                except Exception:
                    print 'Error al obtener el listado de intersecciones. Inténtenlo nuevamente.'
                    sys.exit()

                print intersections_list
            else:
                print 'No se encontraron intersecciones para la calle ingresada.'
                sys.exit()

        intersection = raw_input("Intersección: ")

        if not intersection:
            print 'Debe seleccionar una intersección para poder continuar.'
            sys.exit()
        else:
            try:
                intersection = int(intersection) - 1
            except Exception:
                print 'El valor ingresado no tiene un formato válido.'
                sys.exit()

            if intersection > len(intersections) - 1:
                print 'El valor ingresado no corresponde a una intersección válida.'
                sys.exit()

            print '\nRecuperando las paradas para la línea ingresada. Espere, por favor...\n'

            str_stops = ETR.get_line_stops(line, int(streets[int(street)]['id']), int(intersections[int(intersection)]['id']))

            if str_stops:
                elements = re.findall(r'<td[^>]*?>(.+)<\/td>', str_stops)

                for index, element in enumerate(elements):
                    print re.sub(r'<[^>]*?>', '', element),

                    if (index + 1) % 2 == 0:
                        print '\n'
                    else:
                        print '-',

                if (index + 1) % 2 != 0:
                    print '\n'
            else:
                print 'No se encontraron paradas para la línea ingresada.'
                sys.exit()

        stop = raw_input("Parada: ")

        if not stop:
            print 'Debe seleccionar una parada para poder continuar.'
            sys.exit()
        else:
            try:
                stop = int(stop)
            except Exception:
                print 'El valor ingresado no tiene un formato válido.'
                sys.exit()

        print '\n'

        return line, stop
