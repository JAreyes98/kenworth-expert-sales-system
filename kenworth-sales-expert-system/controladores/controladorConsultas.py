import os
import pyodbc
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QTableView
import pandas as pd

from modelos.conexionDB import Conexion
from modelos.tableModel import MyTableModel

Ui_Consultas, QBase = uic.loadUiType('./vistas/consultas.ui')

class ControladorConsultas(QMainWindow, Ui_Consultas):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Consultas.__init__(self)
        super().setupUi(self)

        #imagenes 
        self.setImagen(self.lbSQL,'icons8-sql-100.png')
        self.setImagen(self.lbRun,'icons8-play-100.png')

        #evento de ejecutar query
        self.lbRun.mouseReleaseEvent = lambda event:self.ejecutar()

    def ejecutar(self):
        #Se tiene el query
        sql = self.txtConsultas.toPlainText()
        
        #conexion a la base de datos
        conexion = Conexion()
        cursor = conexion.cursor()
        
        sql_data = pd.DataFrame()

        try:
            #ejecuta la consulta
            cursor.execute(sql)

            #convierte la consulta en un dataframe
            sql_data = pd.DataFrame(cursor.fetchall())
           
            #modelo de tabla
            modelo = MyTableModel(sql_data)

            #Carga el modelo a la tabla
            self.tabla.setSelectionBehavior(QTableView.SelectRows)
            self.tabla.setSelectionMode(QTableView.SingleSelection)
            self.tabla.setModel(modelo)

        except pyodbc.ProgrammingError as error:
            self.lbResult.setText('Consulta erronea!')
            self.lbResult.setStyleSheet('color:red;')
        else:
            self.lbResult.setText('Filas obtenidas: ' + str(sql_data.shape[0]))
            self.lbResult.setStyleSheet('color:green;')
        finally:
            #cierra la conexion
            conexion.cerrarConexion()
    
    
    def setImagen(self, label, imagenName):
        label.setStyleSheet('QLabel{background-color: #ffffff;}')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        img = QtGui.QImage(os.path.join(scriptDir, 'recursos', imagenName))
        pixmap = QtGui.QPixmap.fromImage(img)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
