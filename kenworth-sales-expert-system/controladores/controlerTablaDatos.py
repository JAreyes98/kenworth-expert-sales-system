from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableView,QMessageBox

from modelos.dFrame import DFrame
from modelos.tableModel import MyTableModel

Ui_tablaDatos, QBase = uic.loadUiType('./vistas/tablaDatos.ui')

class ControlerTablaDatos(QMainWindow, Ui_tablaDatos):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_tablaDatos.__init__(self)
        super().setupUi(self)

        self.tabla.setSelectionBehavior(QTableView.SelectRows)
        self.tabla.setSelectionMode(QTableView.SingleSelection)

        self.dframe = DFrame()
        self.datos = self.dframe.read_all()

        tableModel = MyTableModel(self.datos)
        self.tabla.setModel(tableModel)
