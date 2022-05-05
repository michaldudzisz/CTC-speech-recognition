import os
import yaml
from PyQt5.QtWidgets import QFrame
from PyQt5 import Qt

from app.static import CONFIG
from word_spotting.dict.WordMapper import WordMapper

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
WORD_MAPPING_FILE = '/home/michal/Documents/timit/timit/TIMITDIC.TXT'

class DictionaryFrame(QFrame):

    def __init__(self, ui):
        super(QFrame, self).__init__()
        self.ui = ui
        self.phones_provider = WordMapper(WORD_MAPPING_FILE)
        self.setup()

    def setup(self):
        self.load_dict()
        self.connect_actions()
    
    def load_dict(self):
        words = []
        with open(CONFIG) as config:
            data = yaml.safe_load(config)
        try:
            words = data['word-spotting-dictionary']
        except:
            pass
        self.check_for_correctness(words)
        self.dictionary = words
        self.update_dictionary_list()

    def check_for_correctness(self, words):
        for word in words:
            if not self.phones_provider.is_word_available(word):
                raise Exception('Incorrect words stored in config file!')
            
    def update_dictionary_list(self):
        for word in self.dictionary:
            if self.ui.dictionaryList.findItems(word, Qt.Qt.MatchExactly) == []:
                self.ui.dictionaryList.addItem(word)
        self.ui.dictionaryList.sortItems()

    def connect_actions(self):
        self.ui.addWordButton.clicked.connect(self.add_word)
        self.ui.removeWordButton.clicked.connect(self.remove_word)

    def add_word(self):
        word = self.ui.wordEdit.text()
        word = word.lower()
        if not self.phones_provider.is_word_available(word):
            print('No such word in dictionary!')
            self.clear_word_edit()
            return
        self.dictionary.append(word)
        self.save_words_to_config()
        self.clear_word_edit()
        self.update_dictionary_list()
    
    def clear_word_edit(self):
        self.ui.wordEdit.setText('')
    
    def remove_word(self):
        current_row = self.ui.dictionaryList.currentRow()
        if current_row == None: return
        selected = self.ui.dictionaryList.takeItem(current_row)
        word_to_remove = selected.text()
        self.dictionary.remove(word_to_remove)
        self.save_words_to_config()
    
    def save_words_to_config(self):
        words_to_store = self.dictionary
        storage_dict = {'word-spotting-dictionary': words_to_store}
        self.save_to_config(storage_dict)

    def save_to_config(self, value):
        with open(CONFIG) as config: 
            data = yaml.safe_load(config)
        if data == None: data = {}
        data.update(value)
        with open(CONFIG, 'w') as config:
            yaml.dump(data, config)
