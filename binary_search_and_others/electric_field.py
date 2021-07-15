import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

r=10
a=1.5
n=300
number_v=300
err=0.00001
r_0=r/n

def step(x,x_0,s):
	return 1/(1+np.exp((x-x_0)/s))

def delta(x,x_0,s):
	return np.exp(-(x-x_0)**2/s**2)

def F(x,y,x_0,y_0,m_0):
	r=((x-x_0)**2+(y-y_0)**2)**0.5
	f_out=m_0/r**2
	f_in=m_0*(r/r_0**3)
	f=f_out*(r>=r_0)+f_in*(r<r_0)
	f_x=f*(x-x_0)/r
	f_y=f*(y-y_0)/r
	return f_x,f_y

def F_total(x,y,arr_x,arr_y,arr_m):
	F_x=[0]*len(x)
	F_y=[0]*len(y)

	for i in range(len(arr_m)):
		f_x,f_y=F(x,y,arr_x[i],arr_y[i], arr_m[i])
		F_x+=f_x
		F_y+=f_y

	return F_x,F_y

def V(x,y,x_0,y_0,m_0):
	r=((x-x_0)**2+(y-y_0)**2)**0.5
	inside=m_0*(3*r_0**2-r**2)/(2*r_0**3)
	outside=m_0/(r+err)
	v=inside*(r<r_0)+outside*(r>=r_0)
	return v

def V_total(x,y,arr_x,arr_y,arr_m):
	V_t=[0]*len(x)

	for i in range(len(arr_m)):
		V_t+=V(x,y,arr_x[i],arr_y[i], arr_m[i])
	return V_t

def density(x,y):
	r=np.sqrt(x**2+y**2)
	return step(r, 5, 1/20)*(2*np.random.rand(len(x))-1)

pos_x=[]
pos_y=[]

for i in range(n):
	for j in range(n):
		pos_x=np.append(pos_x, 2*i/n*r-r)
		pos_y=np.append(pos_y, 2*j/n*r-r)

pos_m=density(pos_x, pos_y)
x=np.linspace(-a*r,a*r,50)
y=np.linspace(-a*r,a*r,50)
x, y = np.meshgrid(x, y)


x_v=np.linspace(-a*r,a*r,number_v)
y_v=np.linspace(-a*r,a*r,number_v)
x_v, y_v = np.meshgrid(x_v, y_v)

fx,fy=F_total(x,y,pos_x, pos_y, pos_m)
V=V_total(x_v, y_v, pos_x, pos_y, pos_m)

f=np.sqrt(fx**2+fy**2)

arrow_color=np.log(f)/np.log(10)
scattersize=2*a*r/n

pos_m_n=np.append(pos_m, [0-max(abs(pos_m)),max(abs(pos_m))])
pos_x_n=np.append(pos_x, [0,0])
pos_y_n=np.append(pos_y, [0,0])

v_max=abs(V).max()

x_v_n=np.append(x_v, [a*r,a*r])
y_v_n=np.append(y_v, [a*r,a*r])
V_tot=np.append(V, [0-v_max,v_max])

plt.style.use('dark_background')
color_charge = [(1.0, 0.0, 0.0, 1.0),
				(0.0, 0.0, 0.0, 1.0),
				(0.0, 0.5, 1.0, 1.0)]  

color_potential = [	(1.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.5, 1.0, 1.0)] 

color_f=  [	(1.0, 0.0, 1.0, 0.0),
			(1.0, 0.0, 1.0, 0.5),
			(1.0, 0.0, 1.0, 1.0)] 

cmap_name = 'my_list'
cm_charge = LinearSegmentedColormap.from_list(cmap_name, color_charge, N=n)
cm_potential = LinearSegmentedColormap.from_list(cmap_name, color_potential, N=100)
cm_f= LinearSegmentedColormap.from_list(cmap_name, color_f, N=len(x_v))

fig = plt.figure()
fig_c=plt.figure()
ax1 = fig.add_subplot(111)
ax2	= fig_c.add_subplot(111)

strm=ax2.streamplot(x,y,fx,fy,color=arrow_color,linewidth=0.5,density=1,cmap=cm_f)
fig_c.colorbar(strm.lines)
pot=ax1.scatter(x_v_n,y_v_n,c=V_tot,s=scattersize,cmap=cm_potential)
fig.colorbar(pot)
sc=ax2.scatter(pos_x_n, pos_y_n, c=pos_m_n, s=scattersize,cmap=cm_charge)
fig_c.colorbar(sc)


ax1.set_aspect('equal', adjustable='box')
ax2.set_aspect('equal', adjustable='box')
plt.show()