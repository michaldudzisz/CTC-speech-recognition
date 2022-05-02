from word_spotting.dict.WordMapper import WordMapper
import time

def test_should_map_word_to_phones():
    # given
    word = 'word'
    mapper = WordMapper('/home/michal/Documents/timit/timit/TIMITDIC.TXT')

    # expect
    time1 = time.time()
    assert mapper.get_phones(word) == ['w', 'er', 'd']
    time2 = time.time()

    print(f"WordMapper#get_phones took {time2 - time1}")

