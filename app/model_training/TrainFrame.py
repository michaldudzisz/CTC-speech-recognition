import os
import yaml
from threading import Thread
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog

from pkg_resources import run_script
from static import CONFIG
from .. import train_main_fun

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

FEATURES_PATH = CURRENT_PATH + '/../../preprocessing/features'

EXTRACT_SCRIPT = CURRENT_PATH + '/../../preprocessing/test.sh'
EXCTRACTING_LOGS = CURRENT_PATH + '/../../logs/extracting.log'

TRAIN_SCRIPT = CURRENT_PATH + '/../../preprocessing/test.sh'
TRAINING_LOGS = CURRENT_PATH + '/../../logs/extracting.log'

class TrainFrame(QFrame):

    def __init__(self, ui):
        super(QFrame, self).__init__()
        self.ui = ui
        self.setup()

    def setup(self):
        self.setup_state()
        self.connect_actions()
    
    def setup_state(self):
        self.dataset_path = None
        self.features_path = FEATURES_PATH
        self.trained_models_path = None

        with open(CONFIG) as config:
            data = yaml.safe_load(config)
        try:
            self.dataset_path = data['dataset']['path']
            self.trained_models_path = data['trained-models']['path']
            self.max_epochs = data['training']['max-epochs']
        except:
            pass
        
        self.ui.datasetPathLabel.setText(self.dataset_path)
        self.ui.trainedModelsPathLabel.setText(self.trained_models_path)
        self.ui.maxEpochsSlider.setValue(self.max_epochs)
        self.ui.maxEpochsLabel.setText(str(self.max_epochs))

    def connect_actions(self):
        self.ui.datasetPathButton.clicked.connect(self.select_dataset_path)
        self.ui.extractFeaturesButton.clicked.connect(self.extract_features)
        self.ui.trainedModelsPathButton.clicked.connect(self.select_trained_models_path)
        self.ui.maxEpochsSlider.valueChanged.connect(self.set_current_max_epochs)
        self.ui.maxEpochsSlider.sliderReleased.connect(self.save_max_epochs)

    def select_dataset_path(self):
        self.dataset_path, _ = QFileDialog.getExistingDirectory()
        self.ui.datasetPathLabel.setText(os.path.basename(self.dataset_path))

    def select_trained_models_path(self):
        self.trained_models_path, _ = QFileDialog.getExistingDirectory()
        self.ui.trainedModelsPathLabel.setText(os.path.basename(self.trained_models_path))

    def extract_features(self):
        run_script(script=EXTRACT_SCRIPT, logs=EXCTRACTING_LOGS)
        self.ui.featuresPathLabel.setText('features saved to ' + FEATURES_PATH)
    
    def set_current_max_epochs(self):
        self.max_epochs = self.ui.maxEpochsSlider.value()
        self.ui.maxEpochsLabel.setText(str(self.max_epochs))

    def save_max_epochs(self):
        with open(CONFIG) as config: 
            data = yaml.safe_load(config)
        data['training']['max-epochs'] = self.max_epochs
        with open(CONFIG, 'w') as config:
            yaml.dump(data, config)
        
    def train(self):
        progress = TrainingProgressNotifier(self)
        self.training_thread = Thread(target=train_main_fun, args=[progress])
        self.training_thread.start()
    
    def get_notified(self, progress):
        self.current_epoch = progress.current_epoch
        self.current_sample = progress.current_sample
        self.current_loss = progress.current_loss
        self.last_epoch_accuracy = progress.last_epoch_accuracy
        self.ui.currentEpochLabel = self.current_epoch
        self.ui.currentSampleLabel = self.current_sample
        self.ui.currentLossLabel = self.current_loss
        self.ui.lastEpochAccuracyLabel = self.last_epoch_accuracy


    
class TrainingProgressNotifier:

    def __init__(self, parentFrame) -> None:
        self.parent = parentFrame
        self.current_epoch = 0
        self.current_sample = 0
        self.current_loss = 0
        self.last_epoch_accuracy = 0
    
    def notify(self):
        self.parent.get_notified(self)


