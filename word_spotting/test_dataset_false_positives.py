import os

# from word_spotting.dict.WordMapper import WordMapper
# from word_spotting.distance39 import distance_ratio39

from dict.WordMapper import WordMapper
from distance39 import distance_ratio39

WORD_MAPPING_FILE = '/home/michal/Documents/timit/timit/TIMITDIC.TXT'
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
RESULT39 = CURRENT_PATH + '/../result39.mlf'

phones_provider = WordMapper(WORD_MAPPING_FILE)

# potrzebuję listy plików zbioru testowego


def parse_word_filename(line):
    word_filename = line.strip().replace('.WAV.wav', '.WRD')
    return word_filename

def load_dictionary(word_filname):
    file = open(word_filname)
    words = []
    for line in file:
        line_elements = line.strip().split()
        words.append(line_elements[2])
    file.close()
    return words

def load_dictionary_phones(words):
    dict = {}
    for word in words:
        phones = phones_provider.get_phones(word)
        if phones == []: continue # ignorowanie nie występujących słów
        dict[word] = phones
    return dict


def load_sentence_phones(audio_filename):
    file = open(RESULT39)
    rec_part = '_'.join(audio_filename.split('/')[-2 :]).replace('.WAV.wav', '.rec')

    phones = []
    phone_mode = False
    for line in file: # szukam "/home/michal/Documents/CTC-speech-recognition/preprocessing/features/MJLN0_SX369.rec"
        if phone_mode == False:
            if line[0] != '"': continue
            if line.split('/')[-1].replace('"', '') != rec_part: continue
            phone_mode = True
        phones.append(line.strip())
        if line.strip() == '.': break

    file.close()
    return phones[1 : -2]


class WordRatio:
    def __init__(self, ratio):
        self.count = 1
        self.average_ratio = ratio

def run():
    words_ratios = {}
    all_words = phones_provider.load_all_available_words_with_phones()
    file = open(CURRENT_PATH + '/../preprocessing/test_audio_files.scp')
    t = 0
    for audio_filename in file: # np /home/michal/Documents/timit/timit/data/TEST/DR6/MJDH0/SI724.WAV.wav
        print(t)
        # if t < 163: 
        #     t = t + 1
        #     continue
        word_transcription_filename = parse_word_filename(audio_filename)
        sentence_words = load_dictionary(word_transcription_filename)
        sentence_phones = load_sentence_phones(audio_filename)

        words_to_be_recognized_in_this_sentence = {}
        for word in all_words:
            if word not in sentence_words: 
                words_to_be_recognized_in_this_sentence[word] = all_words[word]

        
        for word in words_to_be_recognized_in_this_sentence:
            word_ratio = distance_ratio39(model39_phones=sentence_phones, word61_phones=words_to_be_recognized_in_this_sentence[word])
            if word in words_ratios:
                old_count = words_ratios[word].count
                new_count = old_count + 1
                words_ratios[word].count = new_count
                words_ratios[word].average_ratio = (words_ratios[word].average_ratio * old_count + word_ratio) / new_count
            else:
                words_ratios[word] = WordRatio(word_ratio)

        t = t + 1
        if t == 200: break

    file.close()

    result_file = open(CURRENT_PATH + '/false_positives.txt', "w")
    for word in words_ratios:
        ratio_struct = words_ratios[word]
        result_file.write(word + ' ' + str(ratio_struct.average_ratio) + '\n')
    result_file.close()



if __name__ == '__main__':
    run()
