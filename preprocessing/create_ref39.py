

REF61 = "/home/michal/Documents/CTC-speech-recognition/preprocessing/ref61.mlf"
REF39 = "/home/michal/Documents/CTC-speech-recognition/preprocessing/ref39.mlf"
MAPPING = "/home/michal/Documents/CTC-speech-recognition/timit2_39.led"


def load_dict():
    mapping_file = open(MAPPING)
    lines = mapping_file.readlines()
    mapping = {}
    for line in lines:
        words = line.split()
        try:
            mapping[words[2]] = words[1]
        except:
            pass
    return mapping


def create_ref39():
    mapping = load_dict()
    ref61 = open(REF61, 'r')
    ref39 = open(REF39, 'w')
    
    while True:
        line = ref61.readline()
        if line == '': break
        words = line.split()
        if words[0].isnumeric() and words[2] in mapping:
            words[2] = mapping[words[2]]
            line = ' '.join(words)
        line = line.replace('\n', '')
        ref39.write(line + '\n')
    
    ref61.close()
    ref39.close()

if __name__ == '__main__':
    create_ref39()

