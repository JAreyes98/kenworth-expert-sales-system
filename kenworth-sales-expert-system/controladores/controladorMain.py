import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5 import QtWidgets, QtGui, QtCore, Qt

from .controladorOpcionesApp import ControladorOpcionesApp
from .controlerTablaDatos import ControlerTablaDatos
from .controladorConsultas import ControladorConsultas
from modelos.herramientas import Herramientas

Ui_App, QBase = uic.loadUiType('./vistas/app.ui')

class ControladorMain(QMainWindow, Ui_App):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_App.__init__(self)
        super().setupUi(self)
        self.setSyles()
        self.iniciarMenuBar()
        self.setTop()
        self.setFooter()
        self.addSubVentana(ControladorOpcionesApp(self))
    
    def iniciarMenuBar(self):
        menu = self.menuBar()

        #-----------------Menu archivo---------------------------
        menuApp = menu.addMenu('Aplicación')

        #submenu inicio
        subMenuInicio = menuApp.addMenu('Inicio')
        accionInicio   = QtWidgets.QAction('Abrir Inicio', self)
        accionInicio.triggered.connect(self.abrirInicio)
        subMenuInicio.addAction(accionInicio)

        #submenu acerca de
        subMenuAcerca = menuApp.addMenu('Acerca De')

        #submenu ayuda
        subMenuDocs  = menuApp.addMenu('Documentacion')
        accionDocs   = QtWidgets.QAction('Abrir', self)
        accionDocs.triggered.connect(self.docs)
        subMenuDocs.addAction(accionDocs)

        #submenu cerrar
        subMenuCerrar = menuApp.addMenu('Cerrar')
        accionCerrar   = QtWidgets.QAction('Quit', self)
        accionCerrar.triggered.connect(self.cerrar)
        subMenuCerrar.addAction(accionCerrar)

        #-----------------Menu DB---------------------------------
        menuDB = menu.addMenu('DB')

        #submenu consultas
        subConsultas = menuDB.addMenu('Consultas SQL')
        accionConsultas = QtWidgets.QAction('Abrir',self)
        accionConsultas.triggered.connect(self.consultas)
        subConsultas.addAction(accionConsultas)

        #submenu diagrama MR
        subDiagramaMR = menuDB.addMenu('Diagrama de DB')
        accionDiagramaMR = QtWidgets.QAction('Ver',self)
        accionDiagramaMR.triggered.connect(self.verDiagramaMR)
        subDiagramaMR.addAction(accionDiagramaMR)

        #-----------------Menu Gráficos---------------------------
        menuGraficos = menu.addMenu('Gráficos')

        #-----------------Menu Datos------------------------------
        menuDatos = menu.addMenu('Datos')

        #subMenu mostrar csv
        subMostrarCSV = menuDatos.addMenu('Mostrar csv')
        accionCSV = QtWidgets.QAction('Ver', self)
        accionCSV.triggered.connect(self.mostrarCsv)
        subMostrarCSV.addAction(accionCSV)

    #------------------EVENTOS DE MENU-----------------------------
    def cerrar(self):
        QtWidgets.qApp.quit()

    def abrirInicio(self):
        self.addSubVentana(ControladorOpcionesApp(self))

    def docs(self):
        url = os.path.dirname(os.path.realpath(__file__)) + '/recursos/Informe.pdf'

        import webbrowser as wb
        wb.open_new(url)
    
    def consultas(self):
        self.addSubVentana(ControladorConsultas(),550, 100, 580, 445)

    def mostrarCsv(self):
        self.addSubVentana(ControlerTablaDatos(),550, 100, 580, 445)

    def verDiagramaMR(self):
        miWidget = QMainWindow()
        label = QtWidgets.QLabel(miWidget)
        label.setGeometry(0, 0, 350, 600)
        label.setStyleSheet('background-color: #ffffff')
        self.setImagen(label, 'mr.png')

        miWidget.setWindowTitle('Create button')
        miWidget.setGeometry(400, 100, 350, 600)
        miWidget.setStyleSheet('border:3px solid #4e4e4e; background-color: #6e6e6e')
        self.addSubVentana(miWidget)

    def setImagen(self, label, imagenName):
        label.setStyleSheet('background-color: #ffffff')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        img = QtGui.QImage(os.path.join(scriptDir, 'recursos', imagenName))
        pixmap = QtGui.QPixmap.fromImage(img)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def setTop(self):
        self.setImagen(self.lbImgBack, 'icons8-back-64.png')
        self.lbTitulo.setStyleSheet('color: #003485; font-size:20px;')

    def setFooter(self):
        self.setImagen(self.lbLogoUni, 'uni.png')

        #Tipo de letra y estilos
        self.lbTextoUni.setStyleSheet('color: #003485')

    def addSubVentana(self, subVentana, x=8 , y=74, ancho=1850, alto=734):
        subVentana.setWindowIcon(QtGui.QIcon(Herramientas().getDireccionIcono()))
        self.pnCentral.addSubWindow(subVentana)
        #self.pnCentral.resize(ancho, alto)
        self.pnCentral.setGeometry(QtCore.QRect(x, y, ancho, alto))
        subVentana.resize(500,734)
        subVentana.show()
        self.pnCentral.tileSubWindows()

    def setSyles(self):
        self.setStyleSheet("""

            QMainWindow{
                background-color: #ffffff;
            }

            QMenuBar{
                background-color: #494949;
                color: #ffffff;
                font-size: 16px;
            }

            QMenuBar::item{
                background-color: transparent;
            }


            QMenuBar::item:selected{
                background-color: #ffffff;
                color: #494949;
            }

            QMenu{
                background-color: #494949;
                color: #ffffff;
                font-size: 14px;
            }

            QMenu::item:selected{
                background-color: #ffffff;
                color: #494949;
            }
        """)