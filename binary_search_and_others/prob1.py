import numpy as np 
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

##########
dts = [0.1,0.2]
y_0 = 3
t_0 = 0
t_f = 4
##########
def Euler_forward(dt):
	def y_next(yy,tt):
		y = yy - (np.cos(4*tt)+2*yy)*dt
		return y
	##########
	t_range = []
	t = t_0 
	while(t <= t_f):
		t_range.append(t)
		t += dt
	Y = []
	y = y_0
	for t in t_range:
		Y.append(y)
		y = y_next(y,t)
	return np.array(t_range), np.array(Y)
##########
def RK2(dt):
	def f(yy,tt):
		y = -(np.cos(4*tt)+2*yy)
		return y
	##########
	t_range = []
	t = t_0 
	while(t <= t_f):
		t_range.append(t)
		t += dt
	Y = []
	y = y_0
	for t in t_range:
		Y.append(y)
		k1 = f(y,t)*dt
		k2 = f(y+0.5*k1,t+0.5*dt)*dt
		y += k2
	return np.array(t_range), np.array(Y)
##########
def y_analytic(tt):
	return -0.1*(np.cos(4*tt)+2*np.sin(4*tt)-31*np.exp(-2*tt))
##########
plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False

for dt, color in zip(dts, ['green','orange']):
	t, y = Euler_forward(dt)
	res_avg = np.mean(np.abs(y-y_analytic(t)))
	plt.errorbar(x=t, y=y, fmt='o', color=color,
		label='frwd E: $\Delta t$='+str(dt)+'\navg residual='
		+str(np.round(res_avg,6)))

for dt, color in zip(dts, ['purple','blue']):
	t, y = RK2(dt)
	res_avg = np.mean(np.abs(y-y_analytic(t))/y.size)
	plt.errorbar(x=t, y=y, fmt='o', color=color,
		label='RK2: $\Delta t$='+str(dt)+'\navg residual='
		+str(np.round(res_avg,6)))

tt = np.linspace(t_0,t_f,num=1000)
plt.errorbar(x=tt, y=y_analytic(tt), fmt='', linewidth=1.5,
	color='black', label='analytic')

plt.legend(loc='best', fontsize=15)
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('foward Euler vs RK2 vs Analytic', fontsize=15)
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()