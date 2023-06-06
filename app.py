import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pseudo = ""
        self.arena = ""
        self.password = ""
        uic.loadUi("formulaire.ui", self)

    def onPseudoChange(self, pseudo):
        print("Pseudo a changer", pseudo)
        self.pseudo = pseudo
    def onArenaChange(self, arena):
        print("arena a changer", arena)
        self.arena = arena
    def onPasswordChange(self, password):
        print("password a changer", password)
        self.password = password

    def onButtonClicked(self, Button):
        self.close()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()