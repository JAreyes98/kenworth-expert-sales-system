if __name__ == '__main__':
    import sys
    from PyQt5 import QtGui
    from PyQt5.QtWidgets import QApplication, QWidget
    from modelos.herramientas import Herramientas
    from controladores.controladorMain import ControladorMain

    app = QApplication(sys.argv)

    main = ControladorMain()
    main.setWindowIcon(QtGui.QIcon(Herramientas().getDireccionIcono()))
    main.showMaximized()
    sys.exit(app.exec_())