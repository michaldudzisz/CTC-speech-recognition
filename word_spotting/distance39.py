import os
from typing import Sequence
from typing import Tuple
from Levenshtein import distance

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
MAPPING_FILE = CURRENT_PATH + "/../map_list"
PHONES_MERGING_FILE = CURRENT_PATH + "/../timit2_39.led"
BOUNDING_FACTOR = 2


def distance_ratio39(model39_phones, word61_phones) -> float:

    if len(word61_phones) >= len(model39_phones): return 0

    word39_phones = map_61_to_39_phones(word61_phones)
    distance = get_minimal_distance(model39_phones, word39_phones)
    ratio = 1 -  (distance / + len(word39_phones))
    return ratio


def get_minimal_distance(model_phones, word_phones) -> int:
    model_chars = map_to_chars(model_phones)
    word_chars = map_to_chars(word_phones)
    lower_bound, upper_bound = calculate_window_bounds(len(model_chars), len(word_chars))

    # print('model_phones: ' + str(model_phones))
    # print('word_phones: ' + str(word_phones))

    minimal_distance = float('inf')
    for seq_len in range(upper_bound, lower_bound - 1, -1):
        for starting_pos in range(0, len(model_chars) - len(word_chars) + 1):
            current_model_seq = model_chars[starting_pos : starting_pos + seq_len - 1]
            current_distance = distance(str().join(current_model_seq), str().join(word_chars))
            if minimal_distance > current_distance: minimal_distance = current_distance

    if minimal_distance == float('inf'): raise Exception('Ooops! Minimal distance not calculated!')
    return minimal_distance


def map_to_chars(phone_seq) -> Sequence[int]:
    mapping = load_mapping()
    chars = list(map(lambda phone: mapping[phone], phone_seq))
    return chars


def load_mapping() -> dict:
    lines = read_file_lines()
    mappings = list(map(lambda line: line.split(), lines))
    char_dict = {}
    for mapping in mappings: char_dict[mapping[0]] = mapping[1]
    return char_dict


def read_file_lines() -> Sequence[str]:
    file = open(MAPPING_FILE)
    lines = file.readlines()
    file.close()
    return lines


def calculate_window_bounds(model_len, word_len) -> Tuple[int, int]:
    lower_bound = min(int(word_len / BOUNDING_FACTOR - 1), 1)
    upper_bound = min(word_len * BOUNDING_FACTOR + 1, model_len)
    return lower_bound, upper_bound

def map_61_to_39_phones(phones61):
    mapping = load_dict()
    phones39 = []
    for phone61 in phones61:
        if phone61 in mapping:
            phones39.append(mapping[phone61])
        else:
            phones39.append(phone61)
    return phones39

def load_dict():
    mapping_file = open(PHONES_MERGING_FILE)
    lines = mapping_file.readlines()
    mapping = {}
    for line in lines:
        words = line.split()
        try:
            mapping[words[2]] = words[1]
        except:
            pass
    return mapping

