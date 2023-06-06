import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import j2l.pytactx.agent as pytactx


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pseudo = ""
        self.arena = ""
        self.password = ""
        uic.loadUi("formulaire.ui", self)

    def onPseudoChange(self, pseudo):
        self.pseudo = pseudo
    def onArenaChange(self, arena):
        self.arena = arena
    def onPasswordChange(self, password):
        self.password = password

    def onButtonClicked(self, Button):
        agent = pytactx.AgentFr(
        nom= self.pseudo, 
        arene=self.arena, 
        username="demo",
        password=self.password, 
        url="mqtt.jusdeliens.com", 
        verbosite=3
        )

        while True:
            agent.orienter((agent.orientation+1)%4)
            agent.actualiser()
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()