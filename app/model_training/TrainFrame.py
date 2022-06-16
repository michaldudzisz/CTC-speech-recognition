import os
import yaml
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog

from app.static import CONFIG
from app.utils.scripting import run_script
from train_ctc import TrainingThread

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

FEATURES_PATH = CURRENT_PATH + '/../../preprocessing/features'

EXTRACT_SCRIPT = CURRENT_PATH + '/../../preprocessing/extract_features.sh'
EXCTRACTING_LOGS = CURRENT_PATH + '/../../logs/extracting.log'

TRAINING_LOGS = CURRENT_PATH + '/../../logs/training.log'

class TrainFrame(QFrame):

    def __init__(self, ui):
        super(QFrame, self).__init__()
        self.ui = ui
        self.test_box_elements = [
            self.ui.label_21,
            self.ui.label_22,
            self.ui.label_23,
            self.ui.label_26,
            self.ui.useLanguageModelCheckbox,
            self.ui.BWSpin,
            self.ui.alphaSpin,
            self.ui.betaSpin
        ]
        self.setup()

    def setup(self):
        self.setup_state()
        self.connect_actions()
    
    def setup_state(self):
        self.dataset_path = None
        self.features_path = FEATURES_PATH
        self.trained_models_path = None
        self.max_epochs = 10

        with open(CONFIG) as config:
            data = yaml.safe_load(config)
        try:
            self.dataset_path = data['dataset']['path']
            self.trained_models_path = data['trained-models']['path']
            self.max_epochs = data['training']['max-epochs']
            self.num_hidden_layers = data['num-hidden-layers']
            self.hidden_layers_size = data['hidden-layers-size']
            self.test_use_language_model = data['test-use-language-model']
            self.test_beam_width = data['test-beam-width']
            self.test_alpha = data['test-alpha']
            self.test_beta = data['test-beta']
            self.beam_decoding_enabled = data['test-beam-decoding-endabled']
        except:
            pass
        
        self.ui.datasetPathLabel.setText(self.dataset_path)
        self.ui.trainedModelsPathLabel.setText(self.trained_models_path)
        self.ui.maxEpochsSlider.setValue(self.max_epochs)
        self.ui.maxEpochsLabel.setText(str(self.max_epochs))
        self.ui.hiddenLayersSpin.setValue(self.num_hidden_layers)
        self.ui.hiddenLayerSizeSpin.setValue(self.hidden_layers_size)
        self.ui.useLanguageModelCheckbox.setChecked(self.test_use_language_model)
        self.ui.BWSpin.setValue(self.test_beam_width)
        self.ui.alphaSpin.setValue(self.test_alpha)
        self.ui.betaSpin.setValue(self.test_beta)
        self.ui.greedyRadio.setChecked(not self.beam_decoding_enabled)
        self.ui.beamRadio.setChecked(self.beam_decoding_enabled)

        for element in self.test_box_elements:
            element.setEnabled(self.beam_decoding_enabled)

    def connect_actions(self):
        self.ui.datasetPathButton.clicked.connect(self.select_dataset_path)
        self.ui.extractFeaturesButton.clicked.connect(self.extract_features)
        self.ui.trainedModelsPathButton.clicked.connect(self.select_trained_models_path)
        self.ui.maxEpochsSlider.valueChanged.connect(self.set_current_max_epochs)
        self.ui.maxEpochsSlider.sliderReleased.connect(self.save_max_epochs)
        self.ui.trainButton.clicked.connect(self.train)
        self.ui.stopTrainingButton.clicked.connect(self.stop_training)
        self.ui.hiddenLayersSpin.valueChanged.connect(self.set_hidden_layers)
        self.ui.hiddenLayerSizeSpin.valueChanged.connect(self.set_hidden_layers_size)
        self.ui.useLanguageModelCheckbox.stateChanged.connect(self.set_test_use_language_model)
        self.ui.BWSpin.valueChanged.connect(self.set_test_beam_width)
        self.ui.alphaSpin.valueChanged.connect(self.set_test_alpha)
        self.ui.betaSpin.valueChanged.connect(self.set_test_beta)
        self.ui.greedyRadio.toggled.connect(self.test_greedy_toggled)

    def select_dataset_path(self):
        self.dataset_path = QFileDialog.getExistingDirectory()
        self.ui.datasetPathLabel.setText(os.path.basename(self.dataset_path))
        self.save_to_config({'dataset': {'path': self.dataset_path}})

    def select_trained_models_path(self):
        self.trained_models_path = QFileDialog.getExistingDirectory()
        self.ui.trainedModelsPathLabel.setText(os.path.basename(self.trained_models_path))
        self.save_to_config({'trained-models': {'path': self.trained_models_path}})

    def extract_features(self):
        run_script(script=EXTRACT_SCRIPT, arg=self.dataset_path, logs=EXCTRACTING_LOGS)
        self.ui.featuresPathLabel.setText('features extracted successfully')
    
    def set_current_max_epochs(self):
        self.max_epochs = self.ui.maxEpochsSlider.value()
        self.ui.maxEpochsLabel.setText(str(self.max_epochs))

    def save_max_epochs(self):
        self.save_to_config({'training': {'max-epochs': self.max_epochs}})

    def set_hidden_layers(self):
        self.num_hidden_layers = self.ui.hiddenLayersSpin.value()
        self.save_to_config({'num-hidden-layers' : self.num_hidden_layers})

    def set_hidden_layers_size(self):
        self.hidden_layers_size = self.ui.hiddenLayerSizeSpin.value()
        self.save_to_config({'hidden-layers-size' : self.hidden_layers_size})
    
    def set_test_use_language_model(self):
        self.test_use_language_model = self.ui.useLanguageModelCheckbox.isChecked()
        self.save_to_config({'test-use-language-model' : self.test_use_language_model})
    
    def set_test_beam_width(self):
        self.test_beam_width = self.ui.BWSpin.value()
        self.save_to_config({'test-beam-width' : self.test_beam_width})

    def set_test_alpha(self):
        self.test_alpha = self.ui.alphaSpin.value()
        self.save_to_config({'test-alpha' : self.test_alpha})

    def set_test_beta(self):
        self.test_beta = self.ui.betaSpin.value()
        self.save_to_config({'test-beta' : self.test_beta})

    def test_greedy_toggled(self):
        self.beam_decoding_enabled = self.ui.beamRadio.isChecked()
        self.save_to_config({'test-beam-decoding-endabled' : self.beam_decoding_enabled})
        for element in self.test_box_elements:
            element.setEnabled(self.beam_decoding_enabled)
        
    def train(self):
        progress = TrainingProgressNotifier(self)
        self.training_thread = TrainingThread(progress_notifier=progress)
        self.training_thread.start()
    
    def get_notified(self, progress):
        self.current_epoch = progress.current_epoch
        self.current_sample = progress.current_sample
        self.current_loss = progress.current_loss
        self.last_epoch_accuracy = progress.last_epoch_accuracy
        self.ui.currentEpochLabel.setText(str(self.current_epoch))
        self.ui.currentSampleLabel.setText(str(self.current_sample))
        self.ui.currentLossLabel.setText("{:.2f}".format(self.current_loss))
        self.ui.lastEpochAccuracyLabel.setText(str(self.last_epoch_accuracy))
    
    def stop_training(self):
        if not hasattr(self, 'training_thread'): return
        self.training_thread.stop()
        self.training_thread.join()
    
    def save_to_config(self, value):
        with open(CONFIG) as config: 
            data = yaml.safe_load(config)
        data.update(value)
        with open(CONFIG, 'w') as config:
            yaml.dump(data, config)



class TrainingProgressNotifier:

    def __init__(self, parentFrame) -> None:
        self.parent = parentFrame
        self.current_epoch = 0
        self.current_sample = 0
        self.current_loss = 0
        self.last_epoch_accuracy = 0
    
    def notify(self):
        self.parent.get_notified(self)


