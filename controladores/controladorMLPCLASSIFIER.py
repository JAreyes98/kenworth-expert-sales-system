# -*- coding: utf-8 -*-
"""
Editor de Spyder

"""

"""
La clasificación te permitirá hacer predicciones, en base a características, aquí utilizamos dos métodos: KNeighbors y RandomForest, 
para predecir en base a las ventas, a cuál género pertenece un video juego

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn import decomposition
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

Ui_app, QBase = uic.loadUiType('./vistas/form_clasificacion.ui')

class MLP(QMainWindow, Ui_app):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_app.__init__(self)
        self.setupUi(self)

        self.llenar_cb()
        self.btnentrenar.clicked.connect(self.graphTraining)
        self.btnpredecir.clicked.connect(self.predecir)
        self.btnmatriz.clicked.connect(self.matriz)

    def llenar_cb(self):

        separacion = []

        for a in range(10,100,10):
            separacion.append(str(a/100))

        self.cbxseparar.addItems(separacion)
            
        iteraciones = []

        for a in range(100,1000,100):
            iteraciones.append(str(a))

        self.cbxinteraccion.addItems(iteraciones)

        self.cbxsolver.addItems(['adam','lbfgs','sgd'])

    def graphTraining(self):

        juegos = pd.read_csv('./csv/vgsales.csv')
        juegos = juegos.replace(np.nan, '0') # Si encuantra espacios lo rellena con ceros
        juegos['Platform'] = juegos['Platform'].replace('2600','Atari')

        # Exportar los datos a un archivo csv
        #juegos.to_csv('juegos2.csv', sep='\t')
        df = pd.DataFrame(juegos)

        # Alimentaremos la red neuroanl con las ventas, quien los saco, plataforma -> entradas
        # Tratar de predecir que genero pertenece

        # Es necesario cambiar los datos que estan en letras a tipo numerico

        from sklearn.preprocessing import LabelEncoder # Metodo que nos permita codificar

        encoder = LabelEncoder()

        juegos['plataforma'] = encoder.fit_transform(juegos.Platform.values) # Nueva columna que depende de los valores 
        juegos['publica'] = encoder.fit_transform(juegos.Publisher.values)

        #print(juegos.plataforma.unique())

        X = juegos[['plataforma','publica', 'Global_Sales']] # Definir las entradas de la red neuronal
        y = juegos['Genre']

        # Estrenar la red neuronal
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = float(self.cbxseparar.currentText()))

        fila = 0
        row = 0
        
        self.tabledatosentrenamiento.setColumnCount(4)
        self.tabledatosentrenamiento.setHorizontalHeaderLabels(['Plataforma', 'Autor', 'Ventas', 'Genero'])

        for dato in X_train['plataforma']:
            fila = fila + 1
        
        self.tabledatosentrenamiento.setRowCount(fila)

        # LLena tipo de plataforma

        for dato in X_train['plataforma']:

            x1 = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosentrenamiento.setItem(row, 0, x1)

            row = row + 1

        row=0

        # Llena autor

        for dato in X_train['publica']:

            x2 = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosentrenamiento.setItem(row, 1, x2)

            row = row + 1

        row=0

        #llena venta

        for dato in X_train['Global_Sales']:

            x3 = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosentrenamiento.setItem(row, 2, x3)

            row = row + 1

        row=0

        # LLena genero

        for dato in y_train:

            y_entrenaminto = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosentrenamiento.setItem(row, 3, y_entrenaminto)

            row = row + 1

        self.tabledatosentrenamiento.verticalHeader().setVisible(False)
        self.tabledatosentrenamiento.setGeometry(QtCore.QRect(50, 260, 523, 211))

        # Datos de prueba
        
        fila = 0
        row = 0
        
        self.tabledatosprueba.setColumnCount(4)
        self.tabledatosprueba.setHorizontalHeaderLabels(['Plataforma', 'Autor', 'Ventas', 'Genero'])

        for dato in X_test['plataforma']:
            fila = fila + 1
        
        self.tabledatosprueba.setRowCount(fila)

        # LLena tipo de plataforma

        for dato in X_test['plataforma']:

            x1 = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosprueba.setItem(row, 0, x1)

            row = row + 1

        row=0

        # Llena autor

        for dato in X_test['publica']:

            x2 = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosprueba.setItem(row, 1, x2)

            row = row + 1

        row=0

        #llena venta

        for dato in X_test['Global_Sales']:

            x3 = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosprueba.setItem(row, 2, x3)

            row = row + 1

        row=0

        # LLena genero

        for dato in y_test:

            y_prueba = QtWidgets.QTableWidgetItem(str(dato))

            self.tabledatosprueba.setItem(row, 3, y_prueba)

            row = row + 1

        self.tabledatosprueba.verticalHeader().setVisible(False)
        self.tabledatosprueba.setGeometry(QtCore.QRect(610, 260, 523, 211))

        # Preprocesamiento de datos

        # Scaler: Dejara los datos de tal forma que se puedar una desviasion estandar de 1 
        # y se recomienda mucho para las redes neuronales para que todos los datos queden con una distribucion normal 
        # evitando que algunos datos se lleven un peso mas importante

        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test) # A las 'y' no se le hace nada, solo a los datos numericos

        # Traer la red neuronal

        from sklearn.neural_network import MLPClassifier
        
        # hidden_layer_sizes: tamaño de las capas ocultas, cuantas hay que tener
        # solver: Especifica el tipo de funciones para resolverlo

        mlp = MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=int(self.cbxinteraccion.currentText()), alpha=0.0001, solver=str(self.cbxsolver.currentText()), random_state=21, tol= 0.000000001) # Esta opcion trae de todo pero hay otra mas sencilla

        #mlp = MLPClassifier(hidden_layer_sizes=(5,5,5,5), max_iter=500)

        # Realizar predicciones y entrenar la red

        #print('\nRealizar predicciones y entrenar la red\n')
        mlp.fit(X_train, y_train)
        prediction = mlp.predict(X_test)

        self.prd = prediction
        self.test = y_test

        #print('Score')
        score = mlp.score(X_test,y_test)
        self.scr = score

        from sklearn.metrics import classification_report
        modelo = classification_report(y_test, prediction) # Dependiendo de los datos predecidos que tan acertados son con respecto a la variable independiente de prueba

        self.txtresumen.setText(modelo)
        self.resize(1190,865)
        
        self.predictt = mlp

    def predecir(self):
        
        plataforma = self.txtplataforma.text()
        publicado = self.txtpublicado.text()
        venta = self.txtventas.text()

        predecir = self.predictt.predict([[ int(plataforma), int(publicado), float(venta)]])

        self.lbl_resultado.setText(str(predecir))

    def matriz(self):
        cm = metrics.confusion_matrix(self.test, self.prd)

        plt.figure(figsize=(30,15))
        sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
        plt.ylabel('Actual label');
        plt.xlabel('Predicted label');
        all_sample_title = 'Accuracy Score: {0}'.format(self.scr)
        plt.title(all_sample_title, size = 15)
        plt.show()
