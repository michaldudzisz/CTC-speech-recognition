import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from app.model_training.TestFrame import TestFrame

from app.model_training.TrainFrame import TrainFrame
from app.words_spotting.AudioFrame import AudioFrame
from app.words_spotting.DictionaryFrame import DictionaryFrame

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
        self.dictionary_frame = DictionaryFrame(ui = self.ui)
        self.audio_frame = AudioFrame(ui = self.ui)

    def connectActions(self):        
        self.ui.closeButton.clicked.connect(self.closeApp)

    def closeApp(self):
        super().close()

