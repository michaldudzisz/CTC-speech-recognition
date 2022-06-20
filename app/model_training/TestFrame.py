import os
import yaml
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
import time

from app.static import CONFIG
from app.utils.scripting import run_script
from peek_at_ctc import main_test_fun

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ACC_SCRIPT = CURRENT_PATH + '/../../get_acc.sh'

class TestFrame(QFrame):

    def __init__(self, ui):
        super(QFrame, self).__init__()
        self.ui = ui
        self.setup()

    def setup(self):
        self.setup_state()
        self.connect_actions()
    
    def setup_state(self):
        self.model_path = ''
        with open(CONFIG) as config:
            data = yaml.safe_load(config)
        try:
            self.model_path = data['test']['model']['path']
        except:
            pass
        self.update_selected_model_label()


    def connect_actions(self):
        self.ui.testedModelPathButton.clicked.connect(self.select_model_path)
        self.ui.testButton.clicked.connect(self.test)

    def select_model_path(self):
        self.model_path, _ = QFileDialog.getOpenFileName(filter='*.pkl')
        self.update_selected_model_label()
        self.save_to_config({'test': {'model': {'path': self.model_path}}})

    def update_selected_model_label(self):
        self.ui.testedModelLabel.setText(os.path.basename(self.model_path) if self.model_path != '' else 'No model selected')

    def test(self):
        if self.model_path == None or self.model_path == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Model not specified")
            msg.setInformativeText('Please set path to a tested model.')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        if not self.get_testing_params(): return

        start = time.time()
        main_test_fun(
            feat_list='/home/michal/Documents/CTC-speech-recognition/preprocessing/test_features_files.scp', 
            decoderp= 'Beam_LM' if self.beam_decoding_enabled  else 'Greedy',
            alphap= self.test_alpha if self.test_use_language_model else 0.0,
            betap=self.test_beta,
            model_path=self.model_path,
            beam_widthp=self.test_beam_width
        )
        run_script(ACC_SCRIPT)
        end = time.time()
        print('time elapsed: ' + str(end - start))
    
    def get_testing_params(self):
        with open(CONFIG) as config:
            data = yaml.safe_load(config)
            try:
                self.test_use_language_model = data['test-use-language-model']
                self.test_beam_width = data['test-beam-width']
                self.test_alpha = data['test-alpha']
                self.test_beta = data['test-beta']
                self.beam_decoding_enabled = data['test-beam-decoding-endabled']
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Model not specified")
                msg.setInformativeText('Please set path to a tested model.')
                msg.setWindowTitle("Error")
                msg.exec_()
                return False
            
        return True

        
    def save_to_config(self, value):
        with open(CONFIG) as config: 
            data = yaml.safe_load(config)
        data.update(value)
        with open(CONFIG, 'w') as config:
            yaml.dump(data, config)
