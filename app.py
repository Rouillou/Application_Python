import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import j2l.pytactx.agent as pytactx
import automatique
agent = None
modeAutoActif = False

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pseudo = ""
        self.arena = ""
        self.password = ""
        # On crée un timer pour régulièrement envoyer les requetes de l'agent au server et actualiser son état 
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.onTimerUpdate)
        self.ui = uic.loadUi("formulaire.ui", self)

    def onPseudoChange(self, pseudo):
        self.pseudo = pseudo
    def onArenaChange(self, arena):
        self.arena = arena
    def onPasswordChange(self, password):
        self.password = password

    def onValideClicked(self):
        global agent
        self.timer.start()
        agent = pytactx.AgentFr(
        nom= self.pseudo, 
        arene=self.arena, 
        username="demo",
        password=self.password, 
        url="mqtt.jusdeliens.com", 
        verbosite=3
        )
        automatique.setAgent(agent)


    def onDownClicked(self):
        agent.deplacer(0, 1)
    def onUpClicked(self):
        agent.deplacer(0, -1)
    def onRightClicked(self):
        agent.deplacer(1, 0)
    def onLeftClicked(self):
        agent.deplacer(-1, 0)

    def onShootClicked(self):
        agent.tirer(True)
    
    def onDownViewClicked(self):
        agent.orienter(3)
    def onUpViewClicked(self):
        agent.orienter(1)
    def onRightViewClicked(self):
        agent.orienter(0)
    def onLeftViewClicked(self):
        agent.orienter(2)

    def onModeClicked(self, isChecked):
        global modeAutoActif
        modeAutoActif = isChecked

    
    def onTimerUpdate(self):
        if ( agent != None ):
            if modeAutoActif == True:
                automatique.actualiserAgent()
            agent.actualiser()
            # MAJ de la ui selon l'état du robot
            if ( agent.vie > self.ui.lifeBar.maximum() ):
                self.ui.lifeBar.setMaximum(agent.vie)
            self.ui.lifeBar.setValue(agent.vie)
            if ( agent.vie > self.ui.ammoBar.maximum() ):
                self.ui.ammoBar.setMaximum(agent.munitions)
            self.ui.ammoBar.setValue(agent.munitions)
            self.ui.pseudolabel.setText(self.pseudo)
            self.ui.areneLabel.setText(self.arena)
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()