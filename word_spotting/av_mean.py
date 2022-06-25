import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
poprawne = '/words_per_sentence_sorted.txt'
fp = '/false_positives.txt'

file = open(CURRENT_PATH + fp, "r")
lines = file.readlines()
file.close() 

nums = []
for line in lines:
    nums.append(float(line.strip().split()[1]))

av = sum(nums) / len(nums)
md = nums[int(len(nums) / 2)]

print("av: " + str(av))
print("md: " + str(md))

