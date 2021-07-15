import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib 

freq = 245 # Hz
file = '3in8in245Hz.txt'

time = []
signal = []

with open(file, 'r') as txt:
	lines = txt.readlines()
	for line in lines[100:-100]:
		split = line.split(' ')
		time.append(float(split[0]))
		signal.append(float(split[1]))
time = np.array(time)
signal = np.array(signal)
f_s = time.size/time[time.size-1]

t_3i, t_3f = int(f_s*0.1), int(f_s*2.2)
t_8i, t_8f = int(f_s*9.5), int(f_s*12)

X_3 = np.mean(signal[t_3i:t_3f]*np.sin(2*np.pi*freq*time[t_3i:t_3f]))
Y_3 = np.mean(signal[t_3i:t_3f]*np.cos(2*np.pi*freq*time[t_3i:t_3f]))
phi_3 = np.arctan(X_3/Y_3)

X_8 = np.mean(signal[t_8i:t_8f]*np.sin(2*np.pi*freq*time[t_8i:t_8f]))
Y_8 = np.mean(signal[t_8i:t_8f]*np.cos(2*np.pi*freq*time[t_8i:t_8f]))
phi_8 = np.arctan(X_8/Y_8)

print('$\phi_3$: '+str(phi_3))
print('$\phi_8$: '+str(phi_8))
# \Delta t = \Delta\phi/(2πf)
# v = (b-a)/dt = (8-3)/dt in/s = .../39.3701 m/s
dt = (phi_8-phi_3)/(2*np.pi*freq)
v = (8-3)/dt/39.3701
print('speed of sound: '+str(v))


