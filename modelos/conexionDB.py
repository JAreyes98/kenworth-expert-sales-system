import os
import platform
import pyodbc
import json

class Conexion():

    def __init__(self):
        self.conexionIsOpened = False
        self.coneccion = None
        self.datosConexion = ()


    def conctar(self, datosConexion):
        self.datosConexion = datosConexion
        if(not self.conexionIsOpened):
            driver = ''
            csv_location = ''

            with open("config.json") as json_data_file:
                data = json.load(json_data_file)

            if (platform.system() == 'Linux'):
                drivers = [item for item in pyodbc.drivers()]
                driver = drivers[-1]
            else:
                driver = 'SQL Server'

            self.coneccion = pyodbc.connect(f"Driver={driver};Server={data['sqlserver']['server']};Database={data['sqlserver']['database']};UID={data['sqlserver']['user']};PWD={data['sqlserver']['password']}")
            
            self.conexionIsOpened = True

        return self.coneccion

    def conectarDefault(self):
        with open("config.json") as json_data_file:
            data = json.load(json_data_file)

        return self.conctar((data['sqlserver']['server'],1433,data['sqlserver']['database'],data['sqlserver']['user'],data['sqlserver']['password']))
    
    def cursor(self):
        if(len(self.datosConexion) == 0):
            return self.conectarDefault().cursor()
        return self.conctar(self.datosConexion).cursor()

    def cerrarConexion(self):
        if(self.conexionIsOpened):
            self.coneccion.close()
            self.conexionIsOpened = False

    # Otro metodo

    def conexion(self):
        with open("config.json") as json_data_file:
            data = json.load(json_data_file)

        driver = ''
        csv_location = ''

        if (platform.system() == 'Linux'):
            drivers = [item for item in pyodbc.drivers()]
            driver = drivers[-1]
        else:
            driver = 'SQL Server'

        coneccion = pyodbc.connect(f"Driver={driver};Server={data['sqlserver']['server']};Database={data['sqlserver']['database']};UID={data['sqlserver']['user']};PWD={data['sqlserver']['password']}")

        
        return coneccion

    def cursor3(self):

        cursor = self.conexion().cursor()
        return cursor

    def cerrar_conexion(self):
        self.conexion().close()


        