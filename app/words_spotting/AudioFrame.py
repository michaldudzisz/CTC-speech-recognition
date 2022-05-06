import os
import yaml
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from shutil import copy

from app.static import CONFIG
from app.utils.scripting import run_script
from peek_at_ctc import main_test_fun
from word_spotting.dict.WordMapper import WordMapper
from word_spotting.distance39 import distance_ratio39

WORD_MAPPING_FILE = '/home/michal/Documents/timit/timit/TIMITDIC.TXT'

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
AUDIO_TMP = CURRENT_PATH + '/tmp/audio.wav'
SPOTTING_SCP = CURRENT_PATH + '/tmp/spotting.scp' # for HCopy
SPOTTING_FEATURE_SCP = CURRENT_PATH + '/tmp/spotting_feature.scp' # for HComp and testint net
EXTRACT_FILE_SCRIPT = CURRENT_PATH + '/extract_audio_file.sh'
NET_OUTPUT_RAW = CURRENT_PATH + '/tmp/result61.mlf'
STAT_PATH = CURRENT_PATH + '/tmp/stat'
MERGING_PHONES_SCRIPT = CURRENT_PATH + '/merge_61_to_39.sh'
NET_OUTPUT_MERGED = CURRENT_PATH + '/tmp/result39.mlf'


class AudioFrame(QFrame):

    def __init__(self, ui):
        super(QFrame, self).__init__()
        self.ui = ui
        self.phones_provider = WordMapper(WORD_MAPPING_FILE)
        self.setup()

    def setup(self):
        self.setup_state()
        self.connect_actions()
    
    def setup_state(self):
        self.model_path = ''
        self.audio_file = ''
        with open(CONFIG) as config:
            data = yaml.safe_load(config)
        try:
            self.model_path = data['word-spotting-model']
            self.audio_file = data['word-spotting-audio']
        except:
            pass
        self.update_selected_model_label()
        self.update_audio_file_label()

    def connect_actions(self):
        self.ui.spottingModelButton.clicked.connect(self.select_model_path)
        self.ui.audioFileButton.clicked.connect(self.load_audio_file)
        self.ui.processButton.clicked.connect(self.process)

    def select_model_path(self):
        self.model_path, _ = QFileDialog.getOpenFileName(filter='*.pkl')
        self.update_selected_model_label()
        self.save_to_config({'word-spotting-model': self.model_path})

    def load_audio_file(self):
        self.audio_file, _ = QFileDialog.getOpenFileName(filter='*.wav')
        self.save_to_config({'word-spotting-audio': self.audio_file})
        self.extraction_label_processing()
        self.update_audio_file_label()
        self.extract_audio_features()
        self.extraction_label_finished()
    
    def extract_audio_features(self):
        self.copy_audio_to_tmp()
        self.create_for_hcopy()
        self.create_for_hcomp()
        run_script(script=EXTRACT_FILE_SCRIPT)

    def copy_audio_to_tmp(self):
        copy(src=self.audio_file, dst=AUDIO_TMP)
        self.audio_file = AUDIO_TMP
    
    def create_for_hcopy(self):
        filename_wav = self.audio_file
        self.audio_file_mfcc = self.audio_file[0 : -4] + '.mfcc'
        filename_mfcc = self.audio_file_mfcc
        file = open(SPOTTING_SCP, 'w')
        file.write(filename_wav + ' ' + filename_mfcc + '\n')
        file.close

    def create_for_hcomp(self):
        file = open(SPOTTING_FEATURE_SCP, 'w')
        file.write(self.audio_file_mfcc + '\n')
        file.close

    def update_selected_model_label(self):
        self.ui.spottingModelLabel.setText(os.path.basename(self.model_path) if self.model_path != '' else 'No model selected')

    def update_audio_file_label(self):
        self.ui.audioFileLabel.setText(os.path.basename(self.audio_file) if self.audio_file != '' else "No file selected")

    def extraction_label_processing(self):
        self.ui.extractionLabel.setText('Extracting features...')

    def extraction_label_finished(self):
        self.ui.extractionLabel.setText('Features succesfully extracted!')

    def process(self):
        main_test_fun(
            feat_list=SPOTTING_FEATURE_SCP,
            model_path=self.model_path,
            output_path=NET_OUTPUT_RAW,
            stat_path=STAT_PATH
        )
        self.postprocess_net_result()
    
    def postprocess_net_result(self):
        self.map_result_to_39_phones()
        words = self.load_words()
        self.dictionary = self.load_dictionary_phones(words)
        self.model_phones = self.load_model_phones()
        ratios = self.compute_ratios()
        self.dispaly_ratios(ratios)
    
    def map_result_to_39_phones(self):
        run_script(MERGING_PHONES_SCRIPT)
    
    def compute_ratios(self):
        model_phones = self.model_phones
        ratios = {}
        for entry in self.dictionary.items():
            word, phones = entry
            ratios[word] = distance_ratio39(model_phones, phones)
        return ratios

    def dispaly_ratios(self, ratios):
        print(ratios)
        self.ui.rankingList.clear()
        sorted_ratios = sorted(ratios.items(), key=lambda item: -item[1])
        for ratio_tuple in sorted_ratios:
            word, ratio = ratio_tuple
            label = "{:.2f}".format(ratio) + f" {word}"
            self.ui.rankingList.addItem(label)

    def load_words(self):
        words = []
        with open(CONFIG) as config:
            data = yaml.safe_load(config)
        try:
            words = data['word-spotting-dictionary']
        except:
            pass
        return words
    
    def load_dictionary_phones(self, words):
        dict = {}
        for word in words:
            phones = self.phones_provider.get_phones(word)
            if phones == []: raise Exception('Invalid word stored in configuration file! Word: ' + word)
            dict[word] = phones
        return dict

    def load_model_phones(self):
        file = open(NET_OUTPUT_MERGED)
        lines = file.readlines()
        phone_lines = lines[2:-1]
        phones = []
        for phone_line in phone_lines:
            phones.append(phone_line.replace('\n', ''))
        return phones

    def save_to_config(self, value):
        with open(CONFIG) as config: 
            data = yaml.safe_load(config)
        data.update(value)
        with open(CONFIG, 'w') as config:
            yaml.dump(data, config)

