import matplotlib.pyplot as plt
import csv
import sys
title = sys.argv[1]
time = []
a_x = []
a_y = []
a_z = []
a_total = []

with open(title,'r') as file:
    read=csv.reader(file, delimiter=',')
    x=True
    for row in read:
        if (x==True):
            x=False
            continue
        time.append(float(row[0]))
        a_x.append(float(row[1]))
        a_y.append(float(row[2]))
        a_z.append(float(row[3]))
        a_total.append(float(row[4]))


plt.errorbar(x=time, y=a_x, linewidth=0.5, fmt='', color='red', label='x')
plt.errorbar(x=time, y=a_y, linewidth=0.5, fmt='', color='blue', label='y')
plt.errorbar(x=time, y=a_z, linewidth=0.5, fmt='', color='green', label='z')
plt.errorbar(x=time, y=a_total, linewidth=1, fmt='', color='black', label='total')

plt.show()