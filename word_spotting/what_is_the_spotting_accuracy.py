import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

treshold = 0.2

file = open(CURRENT_PATH + '/false_positives.txt')
false_positives = []
for line in file:
    line_elements = line.strip().split()
    false_positives.append(float(line_elements[1]))
file.close()

file = open(CURRENT_PATH + '/words_per_sentence_sorted.txt')
true_positives = []
for line in file:
    line_elements = line.strip().split()
    true_positives.append(float(line_elements[1]))
file.close()

max_acc = 0
treshold = 0

for current_treshold in [x / 100.0 for x in range(10, 90)]: #range(0.2, 0.8, 0.01):
    tmp_true_positives = list(filter(lambda x: x > current_treshold, true_positives))
    tmp_false_positives = list(filter(lambda x: x > current_treshold, false_positives))
    acc = len(tmp_true_positives) - len(tmp_false_positives)
    if acc > max_acc:
        max_acc = acc
        treshold = current_treshold

print('best acc: ' + str(max_acc))
print('treshold: ' + str(treshold))

# wynik:
# best acc: 1998
# treshold: 0.42
