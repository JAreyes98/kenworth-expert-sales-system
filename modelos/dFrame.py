import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from  sklearn.preprocessing import StandardScaler

class DFrame:

    def __init__(self):
        # Obtiene la ubicacion del directorio actual para cargar el data Frame
        dir_path = os.path.dirname(os.path.realpath(__file__)).replace('modelos','')
        self.url = dir_path + '/csv/BreadBasket_DMS.csv'
        self.name_columns = ['Date','Time','Transaction','Item']

        self.dataframe = pd.read_csv(self.url, names=self.name_columns)

    def shape(self):
        return self.dataframe.shape

    def los_primeros_20(self):
        return self.dataframe.head(20)

    def descripcion(self):
        return self.dataframe.describe()

    def read_all(self):
        return self.dataframe
    
    def update_person(Person):
        pass

    def delete_person():
        pass

    def read_by_slice(self, limSup=None, limInf=None):
        return self.read_all().loc[:, self.name_columns][limInf:limSup]