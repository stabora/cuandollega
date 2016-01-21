#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import datetime
from PyQt4 import QtCore, QtGui
from mainWindow import Ui_mainWindow
from lib.etr import ETR
from lib.util import Util


class App(QtGui.QApplication):

    def __init__(self, args):
        QtGui.QApplication.__init__(self, args)

        self.main = MainWindow()
        self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.exitApp)
        self.main.show()

    def exitApp(self):
        self.exit()


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.statusbar.showMessage(u'Seleccione una línea')

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon('ui/res/img/icon.png'))
        self.trayIcon.show()
        self.trayIcon.setContextMenu(self.ui.menuInicio)

        self.ui.comboBox_linea.addItem('', '')
        self.ui.comboBox_linea.addItems(ETR.list_lines()[1])

        self.connect(self.ui.comboBox_linea, QtCore.SIGNAL("currentIndexChanged(QString)"), self.on_line_change)
        self.connect(self.ui.comboBox_calle, QtCore.SIGNAL("currentIndexChanged(QString)"), self.on_street_change)
        self.connect(self.ui.comboBox_interseccion, QtCore.SIGNAL("currentIndexChanged(QString)"), self.on_intersection_change)
        self.connect(self.ui.pushButton_consultar, QtCore.SIGNAL("released()"), self.on_button_query)
        self.connect(self.ui.actionSalir, QtCore.SIGNAL("triggered()"), self.on_menu_exit)

    def on_line_change(self):
        self.ui.comboBox_calle.clear()

        if self.ui.comboBox_linea.currentText():
            self.ui.statusbar.showMessage(u'Consultando el listado de calles. Espere, por favor...')
            str_streets = ETR.get_line_streets(str(self.ui.comboBox_linea.currentText()))
            self.ui.comboBox_calle.addItem('', -1)

            for street in Util.generate_streets_list(str_streets)[0]:
                self.ui.comboBox_calle.addItem(street['desc'], street['id'])

            self.ui.statusbar.showMessage(u'Seleccione una calle')

    def on_street_change(self):
        self.ui.comboBox_interseccion.clear()

        if self.ui.comboBox_calle.currentText():
            self.ui.statusbar.showMessage(u'Consultando el listado de intersecciones. Espere, por favor...')
            line = self.ui.comboBox_linea.currentText()
            street = self.ui.comboBox_calle.itemData(self.ui.comboBox_calle.currentIndex()).toInt()[0]

            str_intersections = ETR.get_line_intersections(line, street)

            self.ui.comboBox_interseccion.addItem('')

            for intersection in Util.generate_streets_list(str_intersections)[0]:
                self.ui.comboBox_interseccion.addItem(intersection['desc'], intersection['id'])

            self.ui.statusbar.showMessage(u'Seleccione una intersección')

    def on_intersection_change(self):
        self.ui.comboBox_parada.clear()

        if self.ui.comboBox_interseccion.currentText():
            self.ui.statusbar.showMessage(u'Consultando el listado de paradas. Espere, por favor...')
            line = self.ui.comboBox_linea.currentText()
            street = self.ui.comboBox_calle.itemData(self.ui.comboBox_calle.currentIndex()).toInt()[0]
            intersection = self.ui.comboBox_interseccion.itemData(self.ui.comboBox_interseccion.currentIndex()).toInt()[0]

            str_stops = ETR.get_line_stops(line, int(street), int(intersection))

            self.ui.comboBox_parada.addItem('')

            elements = re.findall(r'<td[^>]*?>(.+)<\/td>', str_stops)

            for index, element in enumerate(elements):
                stop = re.sub(r'<[^>]*?>', '', element)

                if (index + 1) % 2 != 0:
                    self.ui.comboBox_parada.addItem(stop.decode('utf-8'), int(stop))

            if len(self.ui.comboBox_parada) == 2:
                self.ui.comboBox_parada.setCurrentIndex(1)

            self.ui.statusbar.showMessage(u'Seleccione una parada')

    def on_button_query(self):
        if self.ui.checkBox_consultaBatch.isChecked():
            # self.ui.pushButton_consultar.setText('Detener')
            self.trayIcon.showMessage('Consulta batch', u'Próximamente...')

        else:
            line = self.ui.comboBox_linea.currentText()
            stop = self.ui.comboBox_parada.itemData(self.ui.comboBox_parada.currentIndex()).toInt()[0]

            if line and stop:
                self.ui.statusbar.showMessage(u'Consultando el servicio del ETR. Espere, por favor...')

                response, incoming = ETR.check_line_schedule(str(line), stop)

                self.ui.plainTextEdit_resultados.clear()
                self.ui.plainTextEdit_resultados.insertPlainText(response.decode('utf-8'))

                self.ui.tableWidget_resultados.insertRow(0)

                item = QtGui.QTableWidgetItem(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                if incoming:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(164, 255, 164)))

                self.ui.tableWidget_resultados.setItem(0, 0, item)

                item = QtGui.QTableWidgetItem(re.sub("---\s[.]+\s---", '', response.decode('utf-8')))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                item.setToolTip(response.decode('utf-8'))

                if incoming:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(164, 255, 164)))

                self.ui.tableWidget_resultados.setItem(0, 1, item)
                self.ui.tableWidget_resultados.resizeColumnsToContents()

                self.ui.statusbar.showMessage(u'Consulta finalizada')

                if incoming:
                    self.trayIcon.showMessage('EN CAMINO', response.decode('utf-8'))

    def on_menu_exit(self):
        self.close()
