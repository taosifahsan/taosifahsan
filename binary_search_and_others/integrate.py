import numpy as np 
import csv
from scipy import integrate
import matplotlib.pyplot as plt 
import matplotlib 

title = 'moveBackg.csv'

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
a_x = np.array(a_x)
a_y = np.array(a_y)
a_z = np.array(a_z)
time = np.array(time)
f_s = time.size / time[time.size-1]
a_x -= np.mean(a_x[:int(f_s*4)])
a_y -= np.mean(a_y[:int(f_s*4)])
a_z -= np.mean(a_z[:int(f_s*4)])#-9.81

v_x = integrate.cumtrapz(a_x, time, initial=0)
v_y = integrate.cumtrapz(a_y, time, initial=0)
v_z = integrate.cumtrapz(a_z, time, initial=0)
v_total = integrate.cumtrapz(a_total, time, initial=0)

s_x = integrate.cumtrapz(v_x, time, initial=0)
s_y = integrate.cumtrapz(v_y, time, initial=0)
s_z = integrate.cumtrapz(v_z, time, initial=0)
s_total = integrate.cumtrapz(v_total, time, initial=0)

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False
plt.errorbar(x=time, y=v_x, linewidth=2, fmt='', color='red', label='x')
plt.errorbar(x=time, y=v_y, linewidth=2, fmt='', color='blue', label='y')
plt.errorbar(x=time, y=v_z, linewidth=2, fmt='', color='green', label='z')
#plt.errorbar(x=time, y=v_total, linewidth=2, fmt='', color='black', label='total')
plt.legend(loc='best')
plt.xlabel('time (s)')
plt.ylabel('velocity (m/s)')
#plt.ylabel('angular position (rad)')
plt.title(title)
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False
plt.errorbar(x=time, y=s_x, linewidth=2, fmt='', color='red', label='x')
plt.errorbar(x=time, y=s_y, linewidth=2, fmt='', color='blue', label='y')
plt.errorbar(x=time, y=s_z, linewidth=2, fmt='', color='green', label='z')
#plt.errorbar(x=time, y=s_total, linewidth=2, fmt='', color='black', label='total')
plt.legend(loc='best')
plt.xlabel('time (s)')
plt.ylabel('position (m)')
plt.title(title)
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()
