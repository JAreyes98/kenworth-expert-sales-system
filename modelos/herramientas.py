import os

class Herramientas:
    def __init__(self):
        pass

    def getDireccionIcono(self):
        direccion = os.path.dirname(os.path.realpath(__file__)).replace('modelos','controladores/')
        return os.path.join(direccion, 'recursos', 'icons8-bot-100.ico')