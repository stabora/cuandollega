# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/designer/mainWindow.ui'
#
# Created: Fri Jan 11 22:21:34 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.setWindowModality(QtCore.Qt.NonModal)
        mainWindow.resize(750, 330)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        mainWindow.setMinimumSize(QtCore.QSize(750, 330))
        mainWindow.setMaximumSize(QtCore.QSize(750, 330))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        mainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox_consulta = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_consulta.setGeometry(QtCore.QRect(10, 20, 371, 261))
        self.groupBox_consulta.setObjectName(_fromUtf8("groupBox_consulta"))
        self.pushButton_consultar = QtGui.QPushButton(self.groupBox_consulta)
        self.pushButton_consultar.setGeometry(QtCore.QRect(250, 180, 91, 24))
        self.pushButton_consultar.setObjectName(_fromUtf8("pushButton_consultar"))
        self.layoutWidget = QtGui.QWidget(self.groupBox_consulta)
        self.layoutWidget.setGeometry(QtCore.QRect(21, 51, 321, 118))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_lineas = QtGui.QLabel(self.layoutWidget)
        self.label_lineas.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_lineas.setObjectName(_fromUtf8("label_lineas"))
        self.horizontalLayout_4.addWidget(self.label_lineas)
        self.comboBox_linea = QtGui.QComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_linea.sizePolicy().hasHeightForWidth())
        self.comboBox_linea.setSizePolicy(sizePolicy)
        self.comboBox_linea.setEditable(False)
        self.comboBox_linea.setObjectName(_fromUtf8("comboBox_linea"))
        self.horizontalLayout_4.addWidget(self.comboBox_linea)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_calle = QtGui.QLabel(self.layoutWidget)
        self.label_calle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_calle.setObjectName(_fromUtf8("label_calle"))
        self.horizontalLayout.addWidget(self.label_calle)
        self.comboBox_calle = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_calle.setEditable(False)
        self.comboBox_calle.setObjectName(_fromUtf8("comboBox_calle"))
        self.horizontalLayout.addWidget(self.comboBox_calle)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_interseccion = QtGui.QLabel(self.layoutWidget)
        self.label_interseccion.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_interseccion.setObjectName(_fromUtf8("label_interseccion"))
        self.horizontalLayout_2.addWidget(self.label_interseccion)
        self.comboBox_interseccion = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_interseccion.setEditable(False)
        self.comboBox_interseccion.setObjectName(_fromUtf8("comboBox_interseccion"))
        self.horizontalLayout_2.addWidget(self.comboBox_interseccion)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_parada = QtGui.QLabel(self.layoutWidget)
        self.label_parada.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_parada.setObjectName(_fromUtf8("label_parada"))
        self.horizontalLayout_3.addWidget(self.label_parada)
        self.comboBox_parada = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_parada.setEditable(False)
        self.comboBox_parada.setObjectName(_fromUtf8("comboBox_parada"))
        self.horizontalLayout_3.addWidget(self.comboBox_parada)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.checkBox_consultaBatch = QtGui.QCheckBox(self.groupBox_consulta)
        self.checkBox_consultaBatch.setGeometry(QtCore.QRect(110, 180, 111, 21))
        self.checkBox_consultaBatch.setObjectName(_fromUtf8("checkBox_consultaBatch"))
        self.tabWidget_resultados = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_resultados.setGeometry(QtCore.QRect(390, 20, 341, 261))
        self.tabWidget_resultados.setAutoFillBackground(False)
        self.tabWidget_resultados.setProperty("accessibleName", _fromUtf8(""))
        self.tabWidget_resultados.setObjectName(_fromUtf8("tabWidget_resultados"))
        self.tab_resultados = QtGui.QWidget()
        self.tab_resultados.setProperty("accessibleName", _fromUtf8(""))
        self.tab_resultados.setObjectName(_fromUtf8("tab_resultados"))
        self.plainTextEdit_resultados = QtGui.QPlainTextEdit(self.tab_resultados)
        self.plainTextEdit_resultados.setEnabled(True)
        self.plainTextEdit_resultados.setGeometry(QtCore.QRect(10, 10, 311, 211))
        self.plainTextEdit_resultados.setUndoRedoEnabled(False)
        self.plainTextEdit_resultados.setReadOnly(True)
        self.plainTextEdit_resultados.setObjectName(_fromUtf8("plainTextEdit_resultados"))
        self.tabWidget_resultados.addTab(self.tab_resultados, _fromUtf8(""))
        self.tab_historico = QtGui.QWidget()
        self.tab_historico.setObjectName(_fromUtf8("tab_historico"))
        self.tableWidget_resultados = QtGui.QTableWidget(self.tab_historico)
        self.tableWidget_resultados.setGeometry(QtCore.QRect(10, 10, 311, 211))
        self.tableWidget_resultados.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tableWidget_resultados.setFrameShadow(QtGui.QFrame.Sunken)
        self.tableWidget_resultados.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_resultados.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.tableWidget_resultados.setProperty("showDropIndicator", False)
        self.tableWidget_resultados.setAlternatingRowColors(True)
        self.tableWidget_resultados.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tableWidget_resultados.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_resultados.setWordWrap(True)
        self.tableWidget_resultados.setColumnCount(2)
        self.tableWidget_resultados.setObjectName(_fromUtf8("tableWidget_resultados"))
        self.tableWidget_resultados.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_resultados.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_resultados.setHorizontalHeaderItem(1, item)
        self.tabWidget_resultados.addTab(self.tab_historico, _fromUtf8(""))
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAyuda = QtGui.QMenu(self.menubar)
        self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
        self.menuInicio = QtGui.QMenu(self.menubar)
        self.menuInicio.setObjectName(_fromUtf8("menuInicio"))
        self.menu_ultimas_consultas = QtGui.QMenu(self.menuInicio)
        self.menu_ultimas_consultas.setObjectName(_fromUtf8("menu_ultimas_consultas"))
        self.menuRegistro = QtGui.QMenu(self.menubar)
        self.menuRegistro.setObjectName(_fromUtf8("menuRegistro"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)
        self.actionAcercaDe = QtGui.QAction(mainWindow)
        self.actionAcercaDe.setObjectName(_fromUtf8("actionAcercaDe"))
        self.actionSalir = QtGui.QAction(mainWindow)
        self.actionSalir.setCheckable(False)
        self.actionSalir.setMenuRole(QtGui.QAction.TextHeuristicRole)
        self.actionSalir.setObjectName(_fromUtf8("actionSalir"))
        self.actionAbrir_archivo_de_registro = QtGui.QAction(mainWindow)
        self.actionAbrir_archivo_de_registro.setObjectName(_fromUtf8("actionAbrir_archivo_de_registro"))
        self.actionAnalizar_archivo_de_registro = QtGui.QAction(mainWindow)
        self.actionAnalizar_archivo_de_registro.setObjectName(_fromUtf8("actionAnalizar_archivo_de_registro"))
        self.actionConsulta_1 = QtGui.QAction(mainWindow)
        self.actionConsulta_1.setObjectName(_fromUtf8("actionConsulta_1"))
        self.actionConsulta_2 = QtGui.QAction(mainWindow)
        self.actionConsulta_2.setObjectName(_fromUtf8("actionConsulta_2"))
        self.actionConsulta_3 = QtGui.QAction(mainWindow)
        self.actionConsulta_3.setObjectName(_fromUtf8("actionConsulta_3"))
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menu_ultimas_consultas.addAction(self.actionConsulta_1)
        self.menu_ultimas_consultas.addAction(self.actionConsulta_2)
        self.menu_ultimas_consultas.addAction(self.actionConsulta_3)
        self.menuInicio.addAction(self.menu_ultimas_consultas.menuAction())
        self.menuInicio.addSeparator()
        self.menuInicio.addAction(self.actionSalir)
        self.menuRegistro.addAction(self.actionAbrir_archivo_de_registro)
        self.menuRegistro.addAction(self.actionAnalizar_archivo_de_registro)
        self.menubar.addAction(self.menuInicio.menuAction())
        self.menubar.addAction(self.menuRegistro.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(mainWindow)
        self.comboBox_linea.setCurrentIndex(-1)
        self.comboBox_calle.setCurrentIndex(-1)
        self.comboBox_interseccion.setCurrentIndex(-1)
        self.tabWidget_resultados.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "Servicio ¿Cuando llega? del ETR", None))
        self.groupBox_consulta.setTitle(_translate("mainWindow", "Consultar horario", None))
        self.pushButton_consultar.setText(_translate("mainWindow", "Consultar", None))
        self.pushButton_consultar.setShortcut(_translate("mainWindow", "Ctrl+C", None))
        self.label_lineas.setText(_translate("mainWindow", "Línea:", None))
        self.label_calle.setText(_translate("mainWindow", "Calle:", None))
        self.label_interseccion.setText(_translate("mainWindow", "Intersección:", None))
        self.label_parada.setText(_translate("mainWindow", "Parada:", None))
        self.checkBox_consultaBatch.setText(_translate("mainWindow", "Consulta batch", None))
        self.checkBox_consultaBatch.setShortcut(_translate("mainWindow", "Ctrl+B", None))
        self.tabWidget_resultados.setTabText(self.tabWidget_resultados.indexOf(self.tab_resultados), _translate("mainWindow", "Resultado", None))
        item = self.tableWidget_resultados.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "Fecha / hora", None))
        item = self.tableWidget_resultados.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "Resultado", None))
        self.tabWidget_resultados.setTabText(self.tabWidget_resultados.indexOf(self.tab_historico), _translate("mainWindow", "Histórico", None))
        self.menuAyuda.setTitle(_translate("mainWindow", "?", None))
        self.menuInicio.setTitle(_translate("mainWindow", "Inicio", None))
        self.menu_ultimas_consultas.setTitle(_translate("mainWindow", "Últimas consultas", None))
        self.menuRegistro.setTitle(_translate("mainWindow", "Registro", None))
        self.actionAcercaDe.setText(_translate("mainWindow", "Acerca de...", None))
        self.actionSalir.setText(_translate("mainWindow", "Salir", None))
        self.actionSalir.setShortcut(_translate("mainWindow", "Ctrl+Q", None))
        self.actionAbrir_archivo_de_registro.setText(_translate("mainWindow", "Ver  archivo de registro...", None))
        self.actionAnalizar_archivo_de_registro.setText(_translate("mainWindow", "Analizar archivo de registro...", None))
        self.actionConsulta_1.setText(_translate("mainWindow", "Consulta 1", None))
        self.actionConsulta_2.setText(_translate("mainWindow", "Consulta 2", None))
        self.actionConsulta_3.setText(_translate("mainWindow", "Consulta 3", None))

import resources_rc
