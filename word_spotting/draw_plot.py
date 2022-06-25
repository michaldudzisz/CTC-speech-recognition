import matplotlib.pyplot as plt
from torch import double
plt.style.use('seaborn-whitegrid')
import numpy as np

def draw_one():
    file = open("words_per_sentence_sorted.txt", "r")
    lines = file.readlines()
    file.close() 

    count = 0
    nums = []
    for line in lines:
        nums.append(float(line.strip().split()[1]))

    x = range(0, 2369) #np.linspace(1, len(nums), 48)
    y = nums.sort()
    y = nums
    print(x)
    print(y)


    plt.plot(x, y, '.', color='blue')
    ax = plt.gca()
    ax.set_ylabel('ratio')
    ax.set_xlabel('indeks słowa')
    ax.set_ylim([0, 1])
    ax.set_xlim([0, 2400])
    ax.set_title('')
    plt.show()


def draw_two():
    file = open("false_positives.txt", "r")
    lines = file.readlines()
    file.close() 

    count = 0
    nums = []
    for line in lines:
        nums.append(float(line.strip().split()[1]))

    x = range(0, len(nums)) #np.linspace(1, len(nums), 48)
    y = nums.sort()
    y = nums
    print(x)
    print(y)


    plt.plot(x, y, '.', color='red')
    ax = plt.gca()
    ax.set_ylabel('ratio')
    ax.set_xlabel('indeks słowa')
    ax.set_ylim([0, 1])
    ax.set_xlim([0, len(nums)])
    ax.set_title('')
    plt.show()

if __name__ == '__main__':
    draw_one()
    draw_two()
