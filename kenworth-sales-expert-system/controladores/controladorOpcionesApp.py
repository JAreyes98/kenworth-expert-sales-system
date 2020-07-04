import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore, Qt

from .descripcion_lineal import Query
from .controladorFiltroProducto import ControladorFiltroProducto
from .controladorMLPCLASSIFIER import MLP
from .neurona import MainWindow

Ui_OpcionesApp, QBase = uic.loadUiType('./vistas/opcionesApp.ui')

class ControladorOpcionesApp(QMainWindow, Ui_OpcionesApp):
    def __init__(self, padre):
        QMainWindow.__init__(self)
        Ui_OpcionesApp.__init__(self)
        super().setupUi(self)
        self.padre = padre
        self.cargarItems()

    def cargarItems(self):
        #Editando los QWidgets
        qwidgetStyle = '{background-color: #ffffff; border: 1px solid #494949; border-radius: 10px;}'
        self.widget.setStyleSheet('#widget' + qwidgetStyle)
        self.widget2.setStyleSheet('#widget2' + qwidgetStyle)
        self.widget3.setStyleSheet('#widget3' + qwidgetStyle)
        self.widget4.setStyleSheet('#widget4' + qwidgetStyle)
        self.widget5.setStyleSheet('#widget5' + qwidgetStyle)

        #Cargando las imagenes
        self.setImagen(self.lbImgItem1,'icons8-statistics-100.png')
        self.setImagen(self.lbImgItem2,'icons8-data-grid-48.png')
        self.setImagen(self.lbImgItem3,'icons8-new-product-100.png')
        self.setImagen(self.lbImgItem4,'icons8-categorize-100.png')
        self.setImagen(self.lbImgItem5,'mind-map.png')

        #Editando los labels
        labelStyles= 'QLabel{color: #494949; font-size:14px;}'
        self.lbTextItem1.setStyleSheet(labelStyles)
        self.lbTextItem2.setStyleSheet(labelStyles)
        self.lbTextItem3.setStyleSheet(labelStyles)
        self.lbTextItem4.setStyleSheet(labelStyles)
        self.lbTextItem5.setStyleSheet(labelStyles)

        #Eventons de los items
        self.widget.mouseReleaseEvent = lambda event:self.abrirRegresion()
        self.btnItem1.clicked.connect(self.abrirRegresion)

        self.widget2.mouseReleaseEvent = lambda event:self.abrirTablaDatos()
        self.btnItem2.clicked.connect(self.abrirTablaDatos)

        self.widget3.mouseReleaseEvent = lambda event:self.abrirFiltroProducto()
        self.btnItem3.clicked.connect(self.abrirFiltroProducto)

        self.widget4.mouseReleaseEvent = lambda event:self.abrirNeuronalClasificacion()
        self.btnItem4.clicked.connect(self.abrirNeuronalClasificacion)

        self.widget5.mouseReleaseEvent = lambda event:self.abrirNeuronalRegresion()
        self.btnItem5.clicked.connect(self.abrirNeuronalRegresion)

    def setImagen(self, label, imagenName):
        label.setStyleSheet('QLabel{background-color: #ffffff;}')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        img = QtGui.QImage(os.path.join(scriptDir, 'recursos', imagenName))
        pixmap = QtGui.QPixmap.fromImage(img)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
    
    def abrirRegresion(self):
        regresion = Query()
        regresion.resize(1089,531)
        self.padre.pnCentral.closeAllSubWindows()
        self.padre.addSubVentana(regresion,350,70,1170,550)
        regresion.show()

    def abrirTablaDatos(self):
        print('tablas')
    
    def abrirFiltroProducto(self):
        filtro = ControladorFiltroProducto()
        filtro.resize(1089,531)
        self.padre.pnCentral.closeAllSubWindows()
        self.padre.addSubVentana(filtro,550, 100, 690, 550)
        filtro.show()
        
    def abrirNeuronalClasificacion(self):
        redClasificacion = MLP()
        redClasificacion.resize(1080,734)
        self.padre.pnCentral.closeAllSubWindows()
        self.padre.addSubVentana(redClasificacion,430,70,1185,790)
        redClasificacion.show()

    def abrirNeuronalRegresion(self):
        redRegresion = MainWindow()
        redRegresion.resize(1089,531)
        self.padre.pnCentral.closeAllSubWindows()
        self.padre.addSubVentana(redRegresion,450,70,990,838)
        redRegresion.show()