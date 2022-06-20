import re
from matplotlib.pyplot import close


VALID_LETTER = re.compile('[a-zA-Z]')
ENDS_WITH_DIGIT = re.compile('(.*)[0-9]')

class WordMapper:

    def __init__(self, word_mapping_file_path):
        self.mapping_file = word_mapping_file_path
    
    def is_word_available(self, word):
        mapping_file = open(self.mapping_file, "r")
        while True:
            line = mapping_file.readline()
            if line == '': return False
            if VALID_LETTER.match(line[0]):
                words = line.split()
                if words[0] == word: return True
        
    def get_phones(self, word):
        print('getting phones for word: ' + word)
        phones = []
        mapping_file = open(self.mapping_file, "r")

        while True:
            line = mapping_file.readline()
            if line == '': return phones

            if VALID_LETTER.match(line[0]):
                words = line.split()
                if words[0] != word: continue
                phones = [words[1].replace('/', ''), *words[2 : -1], words[-1].replace('/', '')]
                # removing stress markers, maybe they are helpful, dunno
                phones = map(lambda phone: phone[0: -1] if ENDS_WITH_DIGIT.match(phone) else phone, phones)
                phones = list(phones)
                break
        
        mapping_file.close()
        return phones

    def load_all_available_words_with_phones(self):
        mapping_file = open(self.mapping_file, "r")
        all_words = {}
        while True:
            line = mapping_file.readline()
            if line == '': return all_words
            if VALID_LETTER.match(line[0]):
                words = line.split()
                all_words[words[0]] = self.get_phones(words[0])

