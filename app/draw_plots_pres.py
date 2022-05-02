import matplotlib.pyplot as plt
from torch import double
plt.style.use('seaborn-whitegrid')
import numpy as np

def draw_one():
    file = open("demofile2.txt", "r")
    lines = file.readlines()
    file.close() 

    count = 0
    nums = []
    for line in lines:
        nums.append(float(line.strip()))

    x = np.linspace(1, 48, 48)
    y = nums[1:]
    print(x)
    print(y)


    plt.plot(x, y, 'o', color='red')
    ax = plt.gca()
    ax.set_ylabel('dokładność')
    ax.set_xlabel('przetworzone nagrania x400')
    ax.set_ylim([0, 100])
    ax.set_xlim([0, 50])
    ax.set_title('Dokładność w czasie treningu')
    plt.show()


def draw_two():
    file = open("demofile3.txt", "r")
    lines = file.readlines()
    file.close() 

    count = 0
    nums = []
    for line in lines:
        nums.append(float(line.strip()))

    x = np.linspace(1, 105, 105)
    y = nums
    print(x)
    print(y)


    plt.plot(x, y, 'o', color='red')
    ax = plt.gca()
    ax.set_ylabel('dokładność [%]')
    ax.set_xlabel('przetworzone nagrania [x200]')
    ax.set_ylim([0, 100])
    ax.set_xlim([0, 107])
    ax.set_title('Dokładność w czasie treningu')
    plt.show()

if __name__ == '__main__':
    draw_two()
