# Proyecto de Sistemas de Información 

## Como seguir esta guia
    * Esta guia de instalacion rapida muestra como realizar la instalacion de la aplicacion en 2 fases
    * La primera fase consiste en la instalacion del programa en python
    * La segunda fase consiste en la instalacion de la base de datos que consume el programa

## Instalacion del programa en python
    1 - Instalacion de python 3:  
        * Ve al sitio de python para descargar python para: 
            - Windows: https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe
            - Linux: Ya esta instalado por defecto
            - Mac OS X: https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe

        * Ahora procede e instala python en tu pc atraves del instalador

        * Verificar si esta instalado python:
            - Abre una terminal (linux y mac) o un CMD (Windows) y ejecuta
                ~~~
                python -V
                ~~~

    2 - Instalando dependencias (Se necesita internet)
        * Abre una terminal de tu sistema operativo

        * Ejecuta: 
            ~~~
            pip install pyodbc pandas PyQt5 numpy matplotlib sklearn PySide seaborn
            ~~~

    3 - Instalando el controlador ODBC
        * Si estas usando Linux o MAC deberas descargar e instalar en controlador ODBC
          * Linux: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
  
          * https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15
          * Si usas Arch linux descarga e instala en controlador desde AUR: https://aur.archlinux.org/msodbcsql.git 

## Pasos para montar la base de datos SQLServer

### Para poner en funcionamiento la base de datos se proporcionan 3 metodos:
    1.- Atraves de un programa de migraciones que se en cuentra adjunto al proyecto en la carpeta migration-dataframe-sqlserver

    2.- Atraves de un backup que se encuentra en la carpeta db_backup

    3.- Atraves de un script que se encuentra en la Carpeta scripts y se llama Full Script.sql

#### Manera 1 - Programa de migraciones
##### 1.- Ejecutar el query Panadería.sql
    "Este query crea la base de datos en SQL Server, en total se crean 7 tablas de las cuales 5 corresponden
    a la base de datos final y las otras son tablas que se utilizan para almacenar los datos temporal mente
    durante la migración de estos mismos a sus respectivas tablas de forma estructurada.
    
    Ademas se crea un procedimiento que servirá para realizar las insercicones masivas de un dataset a la base de datos y una funcion que auto general el codigo del producto la cual es utilizada mas adelante en la inserción de estos productos."

##### 2.- Entra ejecutar el archivo main.py que se encuentra en el proyeco llamado migration-dataframe-sqlserver
######     Para esto es necesario utilizar la libreria pyodbc de sqlserver y el de pandas.
    "Este pequeño programa inserta los datos de un dataset a la base de datos, especificamente a la tabla llamada trasactions. ***Hay que tener cuidado de cambiar los datos de su gestor, como el nombre del servidor,
    usuario y contraseña, estos datos estan en el archivo de configuracion llamado config.json***Este proceso puede tardar varios minutos ya que son 21293 registros!"

##### 3.- Ejecuta el query EB-build-goods.sql
    "En este query se encuentran los datos del precio de los productos y estos son ingresados en la tabla goods."

##### 4.- Ejecuta el query Datos.sql
    "En este query se encuentran las migraciones de las tablas temporales que se llenaron por la inserccion masiva del dataset a la base de datos y se reinsertan en tablas relacionales de la base de datos final."


##### 5.- Finalmente se debe ejecutar el query Cursores.sql
    "Finalmente se crean cursores que insertan y actualizan datos y tablas en la base de datos, dejandola lista para su respectivo funcionamiento." 

#### Manera 2 - Restaurar el backup (que se encuentra en Querys/db_backup)
##### 1.- Ejecutar el siguiente comando
        ~~~
        RESTORE FILELISTONLY
        FROM DISK = 'C:\Kenworth.bak' ;
        GO
        RESTORE DATABASE Kenworth
        FROM DISK = 'C:\Kenworth.bak'
        WITH FILE = 1
        RECOVERY;
        ~~~
#### Manera 3 - Script con todos los datos
##### 1.- Ejecutar el Script llamado Full Query.sql que se encuentra en la carpeta sqlserver

# Cambiar las credenciales y datos del gestor
    "En la carpeta principal del proyecto kenworth-sales-expert-system hay un archivo llamado 
    config.json, en este esta la configuracion que la aplicacion usa para conectarse a tu gestor de base de datos por lo que es indispensable que la cambies"

# Finalmente puede ejecutar la aplicacion
    "Entre a la carpeta kenworth-sales-expert-system en su terminal y ejecute:"
    ~~~
    python main.py
    ~~~