#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import base64
import datetime
import smtplib
import json
from ConfigParser import SafeConfigParser


class Util:

    root_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'

    @staticmethod
    def check_dir_exists(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def load_config():
        try:
            variables = {}
            config = SafeConfigParser()
            config.read(Util.root_dir + 'config/config.ini')

            variables['url_sms'] = config.get('ETR', 'url_sms')
            variables['url_data'] = config.get('ETR', 'url_data')

            if config.get('proxy', 'host'):
                variables['proxy'] = config.get('proxy', 'host') + ':' + config.get('proxy', 'port')
                proxy_user = config.get('proxy', 'user')
                proxy_pass = base64.b64decode(config.get('proxy', 'pass'))

                if proxy_user or proxy_pass:
                    variables['proxy'] = 'http://' + proxy_user + ':' + proxy_pass + '@' + variables['proxy']
            else:
                variables['proxy'] = None

            Util.log_dir = config.get('general', 'log_dir')
            variables['log_dir'] = Util.log_dir
            variables['log_dir'] = config.get('general', 'log_dir')
            variables['timeout'] = int(config.get('general', 'timeout'))
            variables['interval'] = int(config.get('general', 'interval'))

            return variables

        except Exception, e:
            if hasattr(e, 'reason'):
                print 'Error de inicialización: ' + e.reason
            else:
                print 'Error de inicialización'

            sys.exit()

    @staticmethod
    def write_log_file(line, stop, text, error=False):
        now = datetime.datetime.now()
        date_day = now.strftime("%Y-%m-%d")
        date_hour = now.strftime("%H:%M")

        try:
            log_dir = Util.root_dir + Util.log_dir + '/' + line + '/' + date_day
            Util.check_dir_exists(log_dir)

            file_name = str(line) + '_' + str(stop) + '_' + date_day

            if error:
                logfile = open(log_dir + '/' + file_name + '-error.log', 'a')
            else:
                logfile = open(log_dir + '/' + file_name + '.log', 'a')

            logfile.write(date_day + ' ' + date_hour + '\n' + str(text) + '\n')
            logfile.close()

        except OSError, e:
            print e

    @staticmethod
    def write_error_log(line, stop, text):
        Util.write_log_file(line, stop, text, True)

    @staticmethod
    def send_email(receiver, subject, text):
        sender = receiver
        receivers = [receiver]

        message = 'Content-Type: text/plain; charset=utf-8\n'
        message += 'Subject: =?UTF-8?B?{}?=\n'.format(base64.encodestring(subject.encode('utf-8')).strip())
        message += 'To: ' + receiver + '\n\n'
        message += text.encode('utf-8')

        try:
            smtpObj = smtplib.SMTP('proyectos3')
            smtpObj.sendmail(sender, receivers, message)
            print "Se ha enviado un e-mail de notificación."
        except Exception:
            print "ERROR al enviar e-mail de notificación."

    @staticmethod
    def send_notifications(line, response, alert=True, email=None):
        if alert:
            os.system('notify-send \'¿Cuándo llega? - Línea ' + line + '\' \'' + response.encode('utf-8') + '\' &')

        if email:
            Util.send_email(email, u'¿Cuándo llega? - Línea ' + line + ' EN CAMINO', response)

    @staticmethod
    def generate_streets_list(str_streets):
        streets = json.loads(str_streets)

        streets_list = '\n'

        for index, street in enumerate(streets):
            streets_list += str(index + 1) + ' - ' + street['desc'] + '\n'

        return streets, streets_list
