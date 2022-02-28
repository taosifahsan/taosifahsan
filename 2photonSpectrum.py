import matplotlib.pyplot as plt
import numpy as np
from numpy import random
from scipy import integrate
import math
import sys
import csv

def mov_avg(y, w):
	y_smooth=y
	for i in range(len(y)-len(w)):
		y_smooth[i+int(len(w)/2)]=sum(y[i:i+len(w):]*w)/sum(w)
	return y_smooth

def plot(y,bar,w):
	return np.maximum(mov_avg(np.array(y), w),bar)

def pileup(p,E,utf,a):
	return (1-utf)*p+utf*p_2(p,E,a)

def p_2(p,E,a):
	return (1-a)*p_A(p,E)+a*p_B(p,E)

def p_A(p,E):
	y=E*0
	dE = E[2]-E[1]
	for i in range(1,len(E)):
		for j in range(i):
			y[i]+=p[i-j]*p[j]*dE
	return y

def p_B(p,E):
	y=E*0
	for i in range(0,len(E)-1):
		#add this region
		A=0
		for j in range(i+1):
			A += p[i+1]*p[j]/E[j]*dE
		#substract this region
		B=0
		for j in range(i//2+1,i):
			B += p[j]*p[i-j]/E[i-j]*dE
		y[i+1] = y[i] + 2*(A - B)*dE
	return y



E = np.linspace(1, 1000,1000)
dE = E[1]-E[0]
utf = 0.1 
a = 1
bar = 1e-6

F = (E<400)
p = F/(sum(F)*dE)
Fn = pileup(p,E,utf,a)
pn = Fn/(sum(Fn)*dE)

font = {'fontname':'Times'}
plt.semilogy(E,plot(p,bar,[1]),linewidth=1)
plt.semilogy(E,plot(pn,bar,[1]),linewidth=1)
plt.xlabel('Energy (ev)', **font)
plt.ylabel('count rate per energy bin (count/s/eV)', **font)

plt.title('count_rate=+'+str(utf))
plt.legend()
plt.grid()
plt.show()
