import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib 
import csv

time = []
B_total = []
with open('treadmill3.csv', 'r') as file:
	read = csv.reader(file, delimiter=',')
	flag = True
	for row in read:
		if flag == True:
			flag = False
			continue
		time.append(float(row[0]))
		B_total.append(float(row[4]))

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False
plt.errorbar(x=time, y=B_total, linewidth=0.5, fmt='', color='green')
plt.xlabel('time (s)')
plt.ylabel('magnetic field ($\mu$T)')
plt.title('AC current')
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()