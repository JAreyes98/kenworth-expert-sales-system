from PyQt5 import uic
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

import matplotlib.pyplot as plt
from modelos.conexionDB import Conexion

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

        row = 0
        conexion = Conexion()
        cursor = conexion.cursor()

        consulta = """SELECT datepart(week, f.fecha_transacciín), sum(df.cantidad) as sumCan
        from detalle_factura df inner join producto p 
        on df.idproducto = p.idproducto
        inner join factura f on df.idfactura = f.idfactura
        group by datepart(week, f.fecha_transacciín)
        order by datepart(week, f.fecha_transacciín) desc;""" 

        # https://www.nosolocodigo.com/como-crear-funciones-en-mysql

        cursor.execute(consulta)
        filas = cursor.fetchall()
        conexion.cerrarConexion()

        # print(filas)
        datos = []
        colum1 = []
        colum2 = []

        for data in filas:
            colum2.append(data[1])
            
        contador = 1
            
        for data in filas:
            colum1.append(contador)
            contador +=1

        datos.append(colum1)
        datos.append(colum2)

        df = pd.DataFrame({'Semana':datos[0], 'Cantidad':datos[1]})

        semana_describe = df['Semana'].describe()

        self.textdescripcion.setText(str(semana_describe))

        # Algoritmos

        import numpy  as np
        # import matplotlib.pyplot as plt
        from sklearn import linear_model
        from sklearn.metrics import r2_score

        regr = linear_model.LinearRegression()
        log = linear_model.LogisticRegression(solver = 'lbfgs')

        x = df['Cantidad'] # Variable dependiente
        y = df['Semana'] # Variable independiente
        # A mayor numero de likes, esperariamos un score mas alto

        fl = []

        contador = 0

        for a in x:
            fl.append(float(a))

        dff = pd.DataFrame({'Flotante':fl})
            
        XX = dff['Flotante']

        X = XX[:, np.newaxis] # Le da un formato de arreglo a los datos que estamos mandando

        # Seperar los datos en conjuntos para entrenar y para hacer las pruebas
        from sklearn.model_selection import train_test_split
        # Tamaño de la prueba 0.25, valores desde el 0 a 1, decimales en porcentaje
        # random_state: si fijamos un numero nos va permitir obtener la misma semilla donde va obtenerse los numeros aleatorios
        X_train, X_test, y_train, y_test = train_test_split(X, y , test_size = 0.5, random_state = 0)

        #Predicción o el modelo lineal
        regr.fit(X_train,y_train) # Depende de estas variables

        #Coeficiende de regresión lineal
        self.txtcoeficiente.setText(str(regr.coef_[0]))

        # Formato como si fuera de la ecuacion de la linea recta, modelo
        m = regr.coef_[0] # Pendiente
        b = regr.intercept_ # Intercept

        y_p = m*X+b # Predice

        plt.scatter(y,x, color='blue')
        plt.title('Regresión lineal', fontsize=16)
        plt.xlabel('Cantidad', fontsize=13)
        plt.ylabel('Semana', fontsize=13)
        plt.xlim(0, 30)

        #Modelo de regresion lineal
        modelo = 'y={0}*x+{1}'.format(m,b)

        self.txtmodelo.setText(str(modelo))

        score_lineal = str(regr.score(X_test,y_test))
        self.txtscore_lineal.setText(score_lineal)

        #nLogaritmica

        log.fit(X_train,y_train) # Entranar el algoritmo

        score_logaritmica = log.score(X, y)

        self.txtscore_logaritmico.setText(str(score_logaritmica))

        # Llenando tablas

        # Datos de entrenamientos

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
