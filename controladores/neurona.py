import pandas as pd
import numpy as np
from PyQt5 import QtWidgets,QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.pyplot import pause
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn import decomposition

#Ui_MainWindow, QBaseApplication = uic.loadUiType('./form_canva.ui')

Ui_app, QBase = uic.loadUiType('./vistas/form_canva.ui')

class MainWindow(QMainWindow, Ui_app):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_app.__init__(self)
        self.setupUi(self)

        # Widguet
        self.canvas = FigureCanvasQTAgg(Figure())
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.canvas)
        self.widget_canva.setLayout(vLayout)

        self.llenar_combo()
        self.btngraficar.clicked.connect(self.graphTraining)

    def llenar_combo(self):

        iteraciones = []
        
        for a in range(100,1000,100):
            iteraciones.append(str(a))

        self.cbxiteraciones.addItems(iteraciones)

    
    def getAxes(self, nRows, nColumns, position):
        return self.canvas.figure.add_subplot(nRows, nColumns, position)

    def toGraph(self):
        self.canvas.figure.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()
        pause(.0001)

    def graphTraining(self):
        axes = self.getAxes(1, 2, 1)
        axesFunc = self.getAxes(1, 2, 2)

        df = pd.read_csv('./csv/bateria.csv')
        x = df['Tiempo']
        y = df['Carga']

        X = x[:, np.newaxis] # Realizas un array de los datos dependientes para tener una mejor estructura de ellos.

        X_train, X_test, y_train, y_test = train_test_split(X, y)


        # Llenado de las tablas entrenamiento

        fila = 0
        row = 0
        
        self.tableWidgetentrenamiento.setColumnCount(2)
        self.tableWidgetentrenamiento.setHorizontalHeaderLabels(['Tiempo/Minuto', 'Carga'])
        self.tableWidgetentrenamiento.setGeometry(QtCore.QRect(110, 200, 274, 250))

        for dato in X_train:
            fila = fila + 1
        
        self.tableWidgetentrenamiento.setRowCount(fila)

        for dato in X_train:

            x1 = QtWidgets.QTableWidgetItem(str(dato[0]))

            self.tableWidgetentrenamiento.setItem(row, 0, x1)

            row = row + 1

        row=0

        for dato in y_train:

            x2 = QtWidgets.QTableWidgetItem(str(dato))

            self.tableWidgetentrenamiento.setItem(row, 1, x2)

            row = row + 1

        self.tableWidgetentrenamiento.verticalHeader().setVisible(False)

        # Llenado de las tablas pruebas

        fila = 0
        row = 0
        
        self.tableWidgetprueba.setColumnCount(2)
        self.tableWidgetprueba.setHorizontalHeaderLabels(['Tiempo/Minuto', 'Carga'])
        self.tableWidgetprueba.setGeometry(QtCore.QRect(540, 200, 274, 250))

        for dato in X_train:
            fila = fila + 1
        
        self.tableWidgetprueba.setRowCount(fila)

        for dato in X_test:

            x1 = QtWidgets.QTableWidgetItem(str(dato[0]))

            self.tableWidgetprueba.setItem(row, 0, x1)

            row = row + 1

        row=0

        for dato in y_test:

            x2 = QtWidgets.QTableWidgetItem(str(dato))

            self.tableWidgetprueba.setItem(row, 1, x2)

            row = row + 1

        self.tableWidgetprueba.verticalHeader().setVisible(False)

        row=0

        #lr = 0.001
        #alpha = 0.0001
        #nn = [9, 1]
        max_iter = int(self.cbxiteraciones.currentText())

        # hidden_layer_sizes = cantidad de neurona que poseera el algoritmo en la capa oculta

        mlp = MLPRegressor(solver='sgd', alpha=1e-4, hidden_layer_sizes=(60), max_iter=int(self.cbxiteraciones.currentText()), tol=1e-4, random_state=1)

        i = 1

        while i <= max_iter:
            mlp.partial_fit(X_train, y_train)
            score1 = r2_score(y_test, mlp.predict(X_test))
            score2 = mlp.score(X_train, y_train)

            axesFunc.clear()
            axesFunc.set_title('Trining')
            axesFunc.plot('Tiempo', 'Carga', data=df,
                          c='blue', label='Real Data - Value')
            axesFunc.plot(df['Tiempo'], mlp._predict(
                X), 'r--', c='red', label='Neural Network Model')
            axesFunc.grid(True)
            axesFunc.tick_params(labelleft=False)
            axesFunc.legend(loc='upper right')

            axes.clear()
            axes.set_title('Loss')
            axes.plot(range(len(mlp.loss_curve_)), mlp.loss_curve_,
                      label='Epoch {}/{} - Score {:.2f}'.format(i, max_iter, score2))
            axes.grid(True)
            axes.legend(loc='upper right')
            axes.tick_params(labelleft=False)
            self.toGraph()
            if score1 > .95 and score2 > .95:
                break
            i += 1