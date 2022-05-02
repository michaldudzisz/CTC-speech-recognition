import re
from matplotlib.pyplot import close


VALID_LETTER = re.compile('[a-zA-Z]')
ENDS_WITH_DIGIT = re.compile('(.*)[0-9]')

class WordMapper:

    def __init__(self, word_mapping_file_path):
        self.mapping_file = word_mapping_file_path

    def get_phones(self, word):
        phones = []
        mapping_file = open(self.mapping_file, "r")

        while True:
            line = mapping_file.readline()
            if line[0] == '': return

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

