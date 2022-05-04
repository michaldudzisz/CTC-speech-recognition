import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from app.model_training.TestFrame import TestFrame

from app.model_training.TrainFrame import TrainFrame

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup()
        self.show()

    def setup(self):
        self.setupState()
        self.loadUi()
        self.initialize_children()
        self.connectActions()
    
    def setupState(self):
        self.filename = None

    def loadUi(self):
        self.ui = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/views/main_window.ui', self)

    def initialize_children(self):
        self.train_frame = TrainFrame(ui = self.ui)
        self.test_frame = TestFrame(ui = self.ui)

    def connectActions(self):        
        self.ui.selectAudioFileButton.clicked.connect(self.selectFile)
        self.ui.processButton.clicked.connect(self.processAudioFile)
        self.ui.closeButton.clicked.connect(self.closeApp)

    def selectFile(self):
        self.filename, _ = QFileDialog.getOpenFileName()
        self.ui.selectedFilenameLabel.setText(os.path.basename(self.filename))
    
    def processAudioFile(self):
        if self.filename is None: return
        print('processing file ' + self.filename)

    def closeApp(self):
        super().close()

