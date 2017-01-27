#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
from lib.util import Util
from bs4 import BeautifulSoup


class ETR:

    config = Util.load_config()
    proxy = config['proxy']
    url_sms = config['url_sms']
    url_data = config['url_data']
    timeout = config['timeout']

    lines_ids = {
        '101': {'id': '1130', 'label': None},
        '102': {'id': '1141', 'label': None},
        '103': {'id': '1142', 'label': None},
        '106': {'id': '1143', 'label': None},
        '107': {'id': '1144', 'label': None},
        '110': {'id': '1145', 'label': None},
        '112': {'id': '1131', 'label': None},
        '113': {'id': '1120', 'label': None},
        '115': {'id': '1132', 'label': None},
        '116': {'id': '1122', 'label': None},
        '120': {'id': '1032', 'label': None},
        '121': {'id': '1121', 'label': None},
        '122': {'id': '1123', 'label': None},
        '123': {'id': '1124', 'label': None},
        '125': {'id': '1146', 'label': None},
        '126': {'id': '1133', 'label': None},
        '127': {'id': '1134', 'label': None},
        '128': {'id': '1147', 'label': None},
        '129': {'id': '1148', 'label': None},
        '130': {'id': '1149', 'label': None},
        '131': {'id': '1135', 'label': None},
        '132': {'id': '1136', 'label': None},
        '133': {'id': '1125', 'label': None},
        '134': {'id': '1128', 'label': None},
        '135': {'id': '1166', 'label': None},
        '136': {'id': '1129', 'label': None},
        '137': {'id': '1167', 'label': None},
        '138': {'id': '1137', 'label': None},
        '139': {'id': '1138', 'label': None},
        '140': {'id': '1139', 'label': None},
        '141': {'id': '1140', 'label': None},
        '142': {'id': '1150', 'label': None},
        '143': {'id': '1151', 'label': None},
        '144': {'id': '1152', 'label': None},
        '145': {'id': '1153', 'label': None},
        '146': {'id': '1154', 'label': None},
        '153': {'id': '1126', 'label': None},
        'K': {'id': '1164', 'label': None},
        'LC': {'id': '1156', 'label': 'Línea de la costa'},
        'RC': {'id': '1155', 'label': 'Ronda del centro'},
        'CS': {'id': '1163', 'label': 'Ronda CUR-SUR'}
    }

    @staticmethod
    def __query_sms(line, stop):
        response = None

        if line[0].isdigit():
            line = re.sub('[^0-9]', '', line)

        line = ETR.lines_ids[line]['id']

        params = {
          'linea': line,
          'parada': stop,
          'accion': 'getSmsEfisat'
        }

        response = ETR.__query_server(ETR.url_sms, params)
        return response

    @staticmethod
    def __get_line_id(line):
        line = str(line)

        if line in ETR.lines_ids:
            return ETR.lines_ids[line]['id']

    @staticmethod
    def __query_server(url, params=None):
        try:
            response = requests.post(
                url,
                timeout=ETR.timeout,
                data=params if params else None,
                proxies={
                    'http': ETR.proxy,
                    'https': ETR.proxy,
                } if ETR.proxy else None
            )

            return response.text

        except Exception, e:
            if hasattr(e, 'reason'):
                text = 'Error al intentar abrir la URL del host: ' + str(e.reason)
            else:
                text = 'Error al intentar abrir la URL del host: Tiempo de espera agotado'

            try:
                Util.write_error_log(getattr(params, 'linea'), getattr(params, 'parada'), text)
            except Exception, e:
                print 'Error al intentar guardar en el registro.'

            return text

    @staticmethod
    def __parse_response(line, stop, text):
        response = ''
        index = 0
        minutes_to_next = None
        headers = ()
        parser = BeautifulSoup(text)

        for header in parser.find_all('th'):
            headers += header.get_text().strip(),

        for cell in parser.find_all('td'):
            index += 1

            response += headers[index - 1] + ': '
            response += cell.get_text().strip()

            if index == 2 and not minutes_to_next:
                response += ' - '
                try:
                    minutes_to_next = int(cell.get_text().strip().split(' ')[0])
                except:
                    minutes_to_next = 0
            elif index == 3:
                response += '\n'
                index = 0
            else:
                response += ' - '

        return minutes_to_next, response

    @staticmethod
    def list_lines():
        lines = []
        lines_list = ''
        lines_cont = 0

        for line_key in sorted(ETR.lines_ids):
            lines_cont += 1

            lines_list += '{}{}{}'.format(
                line_key,
                ' - ' + ETR.lines_ids[line_key]['label'] if ETR.lines_ids[line_key]['label'] else '',
                '\t'
            )

            lines += [line_key]

            if lines_cont % 4 == 0:
                lines_list += '\n'

        lines_list += '\n\n'

        return lines_list, lines

    @staticmethod
    def get_line_streets(line):
        response = None
        line_id = ETR.__get_line_id(line)

        if line_id:
            params = {
                'line': line,
                'accion': 'getCalle',
                'idLinea': line_id
            }

            response = ETR.__query_server(ETR.url_data, params)

        return response

    @staticmethod
    def get_line_intersections(line, street):
        response = None
        line_id = ETR.__get_line_id(line)

        if line_id:
            params = {
                'line': line,
                'accion': 'getInterseccion',
                'idLinea': line_id,
                'idCalle': street
            }

            response = ETR.__query_server(ETR.url_data, params)

        return response

    @staticmethod
    def get_line_stops(line, street, intersection):
        line_id = ETR.__get_line_id(line)
        stops = []
        last_stop_id = None

        if line_id:
            params = {
                'line': line,
                'accion': 'getParadasXCalles',
                'idLinea': line_id,
                'idCalle': street,
                'idInt': intersection
            }

            str_stops = ETR.__query_server(ETR.url_data, params)

            if str_stops:
                parser = BeautifulSoup(str_stops)

                for row in parser.find_all('tr'):
                    cells = row.find_all('td')

                    if cells:
                        try:
                            cell_stop_id = int(cells[0].get_text().strip())
                        except:
                            cell_stop_id = None

                        try:
                            cell_stop_description = cells[1].get_text().strip()
                        except:
                            cell_stop_description = None

                        if cell_stop_id and cell_stop_id not in [stop['id'] for stop in stops]:
                            last_stop_id = cell_stop_id
                            stops.append({'id': cell_stop_id, 'desc': cell_stop_description})
                        elif cell_stop_description:
                            for stop in stops:
                                if stop['id'] == last_stop_id:
                                    stop['desc'] = ', '.join([stop['desc'], cell_stop_description])

        return stops

    @staticmethod
    def check_line_schedule(line, stop):
        response = ETR.__query_sms(line, stop)
        minutes_to_next, response = ETR.__parse_response(line, stop, response)
        Util.write_log_file(line, stop, response)

        return minutes_to_next, response

    @staticmethod
    def interactive_mode_wizard():
        print 'Consulta \'¿Cuándo llega?\' del ETR - Asistente de consulta interactiva.\n'

        lines_list, lines = ETR.list_lines()
        print lines_list,

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

            stops = ETR.get_line_stops(line, int(streets[int(street)]['id']), int(intersections[int(intersection)]['id']))

            if stops:
                for stop in stops:
                    print '{} - {}'.format(stop['id'], stop['desc'])

                print
            else:
                print 'No se encontraron paradas para la línea ingresada.'
                sys.exit()

        if len(stops) == 1:
            stop = stops[0]['id']
        else:
            stop = raw_input('Parada: ')

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
