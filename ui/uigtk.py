#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from threading import Thread
from time import sleep
sys.path.append('..')
from lib.etr import ETR
from lib.util import Util


try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Notify', '0.7')
    from gi.repository import Gtk
    from gi.repository import Notify
except:
    sys.exit('Error')


class CuandoLlegaApp:

    def __init__(self):
        app_icon_path = os.path.join('res', 'img', 'icon.png')

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join('glade', 'cuandoLlega.glade'))
        self.builder.connect_signals(self)

        self.mainWindow = self.builder.get_object('mainWindow')
        self.mainWindow.set_icon_from_file(app_icon_path)
        self.mainWindow.show_all()

        self.statusbar = self.builder.get_object('statusBar')
        self.statusbar.push(0, 'Seleccione una línea.')

        self.statusIcon = Gtk.StatusIcon()
        self.statusIcon.set_from_file(app_icon_path)
        self.statusIcon.set_has_tooltip(True)
        self.statusIcon.set_visible(True)

        self.line = self.builder.get_object('cboLine')
        self.linesList = self.builder.get_object('linesList')

        for line in sorted(ETR.lines_ids):
            self.linesList.append([line, int(ETR.lines_ids[line]['id'])])

        self.street = self.builder.get_object('cboStreet')
        self.streetsList = self.builder.get_object('streetsList')
        self.intersection = self.builder.get_object('cboIntersection')
        self.intersectionsList = self.builder.get_object('intersectionsList')
        self.stop = self.builder.get_object('cboStop')
        self.stopsList = self.builder.get_object('stopsList')
        self.batch = self.builder.get_object('swtBatch')
        self.result = self.builder.get_object('resultTextBuffer')

        self.mainWindow.connect('destroy', self.closeMainWindow)
        self.statusIcon.connect('activate', self.toggleMainWindow)
        self.builder.get_object('mainMenu_helpMenu_about').connect('activate', self.showAboutWindow)
        self.builder.get_object('mainMenu_fileMenu_quit').connect('activate', self.closeMainWindow)
        self.line.connect('changed', self.selectLine)
        self.street.connect('changed', self.selectStreet)
        self.intersection.connect('changed', self.selectIntersection)
        self.builder.get_object('btnSubmit').connect('clicked', self.submit)

        Notify.init('CuandoLlegaApp')
        Gtk.main()

    def closeMainWindow(self, *args):
        Gtk.main_quit(*args)

    def showAboutWindow(self, *args):
        self.aboutWindow = self.builder.get_object('aboutDialog')
        self.aboutWindow.run()
        self.aboutWindow.hide()

    def toggleMainWindow(self, *args):
        if self.mainWindow.get_visible():
            self.mainWindow.hide()
        else:
            self.mainWindow.show()

    def selectLine(self, combo):
        line = combo.get_model()[combo.get_active()][0]

        if line:
            self.streetsList.clear()
            self.intersectionsList.clear()
            self.stopsList.clear()

            str_streets = ETR.get_line_streets(line)

            for street in Util.generate_streets_list(str_streets)[0]:
                self.streetsList.append([street['desc'], int(street['id'])])

            self.statusbar.push(0, 'Seleccione una calle.')

    def selectStreet(self, combo):
        line = self.line.get_model()[self.line.get_active()][0]
        street_id = combo.get_model()[combo.get_active()][1] if combo.get_active() > -1 else None

        if line and street_id:
            str_intersections = ETR.get_line_intersections(line, street_id)

            self.intersectionsList.clear()

            for intersection in Util.generate_streets_list(str_intersections)[0]:
                self.intersectionsList.append([intersection['desc'], int(intersection['id'])])

            if len(self.intersectionsList) == 1:
                self.intersection.set_active(0)

            self.statusbar.push(0, 'Seleccione una intersección.')

    def selectIntersection(self, combo):
        line = self.line.get_model()[self.line.get_active()][0]
        street_id = self.street.get_model()[self.street.get_active()][1] if self.street.get_active() > -1 else None
        intersection_id = self.intersection.get_model()[self.intersection.get_active()][1] if self.intersection.get_active() > -1 else None

        if line and street_id and intersection_id:
            self.stopsList.clear()

            for stop in ETR.get_line_stops(line, street_id, intersection_id):
                self.stopsList.append(['{} - {}'.format(stop['id'], stop['desc']), int(stop['id'])])

            if len(self.stopsList) == 1:
                self.stop.set_active(0)

            self.statusbar.push(0, 'Seleccione una parada.')

    def submit(self, button):
        if not self.batch.get_active():
            self.getSchedule(button)
        else:
            while self.batch.get_active():
                thread = Thread(target=self.getSchedule, args=(button))
                thread.start()
                thread.join()
                sleep(10)

    def getSchedule(self, button):
        line = self.line.get_model()[self.line.get_active()][0] if self.line.get_active() > -1 else None
        stop = self.stop.get_model()[self.stop.get_active()][1] if self.stop.get_active() > -1 else None

        if not line or not stop:
            self.statusbar.push(0, 'Seleccione todos los datos para conitnuar.')
        else:
            minutes_to_next, schedule = ETR.check_line_schedule(line, stop)
            self.result.set_text(schedule)

            if minutes_to_next <= 10:
                Notify.Notification.new('Servicio de consultas ¿Cuando llega?', schedule).show()

        return

if __name__ == '__main__':
    app = CuandoLlegaApp()
