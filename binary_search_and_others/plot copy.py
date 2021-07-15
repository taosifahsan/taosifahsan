import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib 
import csv

title = 'walkNog.csv'

time = []
a_x = []
a_y = []
a_z = []
a_total = []
with open(title, 'r') as file:
	read = csv.reader(file, delimiter=',')
	flag = True
	for row in read:
		if flag == True:
			flag = False
			continue
		time.append(float(row[0]))
		a_x.append(float(row[1]))
		a_y.append(float(row[2]))
		a_z.append(float(row[3]))
		a_total.append(float(row[4]))

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False
plt.errorbar(x=time, y=a_x, linewidth=0.5, fmt='', color='red', label='x')
plt.errorbar(x=time, y=a_y, linewidth=0.5, fmt='', color='blue', label='y')
plt.errorbar(x=time, y=a_z, linewidth=0.5, fmt='', color='green', label='z')
plt.errorbar(x=time, y=a_total, linewidth=0.5, fmt='', color='black', label='total')
plt.legend(loc='best')
plt.xlabel('time (s)')
plt.ylabel('acceleration (m/s$^2$)')
plt.title(title)
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()