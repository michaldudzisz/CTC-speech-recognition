import sys

if __name__ == '__main__':
    filename = sys.argv[0]
    file = open(filename, 'r')
    
    while True:
        line = file.readline()
        if line == '': break
        words = line.split()
        print("moje line: " + line)
        if words[0].isnumeric():
            if words[2] == 'h#':
                words.insert(2, 'sil')
                line = ' '.join(words)
        print(line)
    
    file.close()
