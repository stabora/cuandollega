#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import time
from lib.etr import ETR
from lib.util import Util
from ui.ui import App


####################################
## General configuration

arguments = 'hLaIl:p:i:e:'
arguments_long = ['help', 'log', 'alert', 'interactivo', 'linea=', 'parada=', 'intervalo=', 'email=']

description_text = '\nConsulta de horarios del transporte público de Rosario a través del servicio \'¿Cuando llega?\' del ETR.'

usage_text = '''
Opciones:
    -l / --linea        <número_línea>      El número de línea que desea consultar.
    -p / --parada       <código_parada>     El código de parada que desea consultar.
    -L / --log                              La consulta se realizará en forma periódica y se guardarán los resultados en los archivos de registro.
    -i / --intervalo    <segundos>          El intervalo, en segundos, entre consultas. Esta opción se utiliza en conjunto con la opción anterior.
    -a / --alert                            Muestra un popup de alerta de sistema si hay un servicio en camino.
    -e / --email        <e-mail>            Una dirección de correo electrónico a la cual se notificará en caso de que el servicio est{e en camino.
    -I / --interactivo                      Inicia el programa en modo interactivo por consola. Los datos se cargan manualmente a medida que son solicitados.

Uso:
    cuandollega.py -h / --help    Muestra este texto de ayuda.

    Para obtener horarios sobre una línea en una parada determinada:

    cuandollega.py -l <línea> -p <código_parada>
    cuandollega.py --linea <línea> --parada <código_parada>
'''


####################################
## Read general configuration

config = Util.load_config()
interval = config['interval']
log_dir = config['log_dir']
alert = False
email = None


####################################
## Main

def main(args):
    global description_text, usage_text, arguments, arguments_long, interval, log_dir, alert, email

    log_results = False
    custom_interval = None
    line = None
    stop = None
    interactive = False

    try:
        opts, args = getopt.getopt(args, arguments, arguments_long)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print description_text, usage_text
                sys.exit()
            elif opt in ('-I', '--interactivo'):
                interactive = True
            elif opt in ('-l', '--linea'):
                line = arg.upper()
            elif opt in ('-p', '--parada'):
                stop = arg
            elif opt in ('-L', '--log'):
                log_results = True
            elif opt in ('-i', '--interval'):
                custom_interval = int(arg)
            elif opt in ('-a', '--alert'):
                alert = True
            elif opt in ('-e', '--email'):
                email = arg

        if not opts:
            app = App(args)
            sys.exit(app.exec_())

        elif interactive:
            line, stop = ETR.interactive_mode_wizard()
        elif len(opts) < 2:
            print usage_text
            sys.exit()

        if log_results:
            if custom_interval != None:
                interval = custom_interval

            print 'Guadando registro de consultas en el directorio \'' + log_dir + '\' - Intervalo: ' + str(interval) + ' segundos.\n'

            while True:
                response, incoming = ETR.check_line_schedule(line, stop)
                print response

                if incoming:
                    Util.send_notifications(line, response, alert, email)

                print '--- Espera: ' + str(interval) + ' segundos ---\n'
                time.sleep(interval)
        else:
            response = None
            incoming = False

            print 'Consultando el servicio \'¿Cuándo llega?\' del ETR. Espere, por favor...\n'

            response, incoming = ETR.check_line_schedule(line, stop)

            print response

            if incoming:
                Util.send_notifications(line, response, alert, email)

    except (getopt.GetoptError, UnboundLocalError):
        print usage_text
        sys.exit()

    except KeyboardInterrupt:
        print '\nConsulta interrumpida por el usuario.'
        sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
