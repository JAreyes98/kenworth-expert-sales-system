from PyQt5 import uic
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from modelos.conexionDB import Conexion
from modelos.Filter import DataFilter
import math

Ui_app, QBase = uic.loadUiType('./vistas/form_imagen.ui')

class Query(QMainWindow, Ui_app):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_app.__init__(self)
        super().setupUi(self)
        self.detalle()

        self.btnGrafica.clicked.connect(self.graficarEvent)

        self.setStyleSheet('QWidget{background-color: #1D2023;}')

    def detalle(self):

        
        conexion = Conexion()
        cursor = conexion.cursor()

        procedimiento = "sp_sales_per_week" 

        cursor.execute("{CALL " + procedimiento +"}")
        filas = cursor.fetchall()
        conexion.cerrarConexion()

        colum1 = []
        colum2 = []
        colName1 = 'Semana'
        colName2 = 'Venta'

        for data in filas:
            colum1.append(data[0])
            colum2.append(data[1])

        df = pd.DataFrame({colName1:colum1, colName2:colum2})
        df = DataFilter(df, colName1, colName2).filter()

        semana_describe = df[colName2].describe()

        # Algoritmos
        row = 0
        import numpy  as np
        # import matplotlib.pyplot as plt
        from sklearn import linear_model
        from sklearn.metrics import r2_score

        regr = linear_model.LinearRegression()
        log = linear_model.LogisticRegression(solver = 'lbfgs')

        x = df[colName1] # Variable dependiente
        y = df[colName2] # Variable independiente
        # A mayor numero de likes, esperariamos un score mas alto

        fl = []

        contador = 0

        for a in x:
            fl.append(a)

        # dff = pd.DataFrame({'Flotante':fl})
            
        # XX = dff['Flotante']
        XX = df[colName1]

        X = XX[:, np.newaxis] # Le da un formato de arreglo numpy

        plt.scatter(y,x, color='blue', linewidth=3)
        plt.title('Regresión lineal', fontsize=16)
        plt.xlabel('Semana')
        plt.ylabel('Vemtas')
        # plt.show()

        # Seperar los datos en conjuntos para entrenar y para hacer las pruebas
        from sklearn.model_selection import train_test_split
        # Tamaño de la prueba 0.25, valores desde el 0 a 1, decimales en porcentaje
        # random_state: si fijamos un numero nos va permitir obtener la misma semilla donde va obtenerse los numeros aleatorios
        X_train, X_test, y_train, y_test = train_test_split(X, y , test_size = 0.1, random_state = 0)

        #Predicción o el modelo lineal
        regr.fit(X_train,y_train) # Depende de estas variables

        #Coeficiende de regresión lineal
        corre = math.sqrt(regr.score(X,y))
        self.txtcoeficiente.setText(str(corre))

        # Formato como si fuera de la ecuacion de la linea recta, modelo
        m = regr.coef_[0] # Pendiente
        b = regr.intercept_ # Intercept

        y_p = m*X+b # Predice

        # plt.scatter(y,x, color='blue', linewidth=3)
        # plt.title('Regresión lineal', fontsize=16)
        # plt.xlabel(colName1, fontsize=13)
        # plt.ylabel(colName2, fontsize=13)
        # plt.xlim(0, 30)

        #Modelo de regresion lineal
        modelo = 'y={0}*x+{1}'.format(m,b)

        self.txtmodelo.setText(str(modelo))

        score_lineal = str(regr.score(X_test,y_test))

        #nLogaritmica

        # logarithmic function  
        # def func(x, p1,p2):
        #     return p1*np.log(x)+p2

        # popt, pcov = curve_fit(func, X, y,p0=(1.0,10.2))

        # log_a= popt[0]
        # log_b= popt[1]
        # log_coe = popt[2]
        # modelo_log = f'{log_a}*ln(x) {log_b}'
        # self.txtcoeficiente_2.setText(str(log_coe))
        # self.txtmodelo_2.setText(str(modelo_log))

        # Llenando tablas

        # Datos de entrenamientos
        
        analisis = ""

        if(corre > 5):
            analisis = f"""El coeficiente de correlacion de la regresion ejecutada en modo entrenamiento aroja
            un coeficinete de correlacion '{corre}' > 0.5 lo que indica que realizar pronosticos con este 
            modelo arrojaria datos muy acercados a la realidad."""
        else:
            analisis = f"""El coeficiente de correlacion de la regresion ejecutada en modo entrenamiento aroja
            un coeficinete de correlacion '{corre}' < 0.5 lo que indica que realizar pronosticos con este 
            modelo no resultaria muy fieble, por lo que se recomienda utilizar otro modelo."""

        self.txtAnalisis.setText(analisis)

        fila = 0
        
        self.tableWidgetentrenamiento.setColumnCount(2)
        self.tableWidgetentrenamiento.setHorizontalHeaderLabels(['X', 'Y'])

        for dato in X_train:
            fila = fila + 1
        self.tableWidgetentrenamiento.setRowCount(fila)

        for dato in X_train:

            x_entrenaminto = QtWidgets.QTableWidgetItem(str(dato[0]))

            self.tableWidgetentrenamiento.setItem(row, 0, x_entrenaminto)

            row = row + 1

        row=0

        for dato in y_train:

            y_entrenaminto = QtWidgets.QTableWidgetItem(str(dato))

            self.tableWidgetentrenamiento.setItem(row, 1, y_entrenaminto)

            row = row + 1

        self.tableWidgetentrenamiento.verticalHeader().setVisible(False)
        self.tableWidgetentrenamiento.setGeometry(QtCore.QRect(380, 250, 273, 211))

        # Datos de prueba
        
        fila = 0
        
        self.tableWidgetprueba.setColumnCount(2)
        self.tableWidgetprueba.setHorizontalHeaderLabels(['X', 'Y'])

        for dato in X_test:
            fila = fila + 1
        self.tableWidgetprueba.setRowCount(fila)

        row = 0

        for dato in X_test:

            x_prueba = QtWidgets.QTableWidgetItem(str(dato[0]))

            self.tableWidgetprueba.setItem(row, 0, x_prueba)

            row = row + 1

        row=0

        for dato in y_test:

            y_prueba = QtWidgets.QTableWidgetItem(str(dato))

            self.tableWidgetprueba.setItem(row, 1, y_prueba)

            row = row + 1
        self.tableWidgetprueba.verticalHeader().setVisible(False)
        self.tableWidgetprueba.setGeometry(QtCore.QRect(730, 250, 273, 211))
    
    def graficarEvent(self):
        plt.show()
