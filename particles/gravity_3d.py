import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

class particles:

	def __init__(state, x=[],y=[], z=[], vx=[],vy=[], vz=[],m=[],rad=[]):

		state.x=x
		state.y=y
		state.z=z
		state.vx=vx
		state.vy=vy
		state.vz=vz
		state.m=m
		state.rad=rad

	def add(state,x,y,z,vx,vy,vz,m):
		state.x.append(x)
		state.y.append(y)
		state.z.append(z)
		state.vx.append(vx)
		state.vy.append(vy)
		state.vz.append(vz)
		state.m.append(m)
		state.rad.append(rad)

	def add_array(state,x,y,z,vx,vy,vz,m):
		state.x=state.x+x
		state.y=state.y+y
		state.z=state.z+z
		state.vx=state.vx+vx
		state.vy=state.vy+vy
		state.vz=state.vz+vz
		state.m=state.m+m
		state.rad=state.rad+rad

	def acceleration(state):

		x=state.x
		y=state.y
		z=state.z
		m=state.m
		rad=state.rad

		N=len(x)

		ax=[0]*N
		ay=[0]*N
		az=[0]*N


		for i in range(N):
			for j in range(N):
				if j==i:
					continue

				rx,ry,rz=x[j]-x[i],y[j]-y[i],z[j]-z[i]
				r=(rx**2+ry**2+rz**2)**0.5

				inside=(r<=rad[j]+rad[i])
				outside=1-inside

				term_x_in=m[j]*rx/(rad[j]+rad[i])**3
				term_x_out=m[j]*rx/r**3

				term_y_in=m[j]*ry/(rad[j]+rad[i])**3
				term_y_out=m[j]*ry/r**3

				term_z_in=m[j]*rz/(rad[j]+rad[i])**3
				term_z_out=m[j]*rz/r**3


				ax[i]+=inside*term_x_in+outside*term_x_out
				ay[i]+=inside*term_y_in+outside*term_y_out
				az[i]+=inside*term_z_in+outside*term_z_out

		return ax,ay,az

	def step(state,dt):

		N=len(state.x)
		ax,ay,az=state.acceleration()

		for i in range(N):
			state.vx[i]+=ax[i]*dt
			state.vy[i]+=ay[i]*dt
			state.vz[i]+=az[i]*dt
			state.x[i]+=vx[i]*dt
			state.y[i]+=vy[i]*dt
			state.z[i]+=vz[i]*dt

	def momentum(state):
		N=len(state.vx)
		px=0
		py=0
		pz=0
		for i in range(N):
			px+=state.m[i]*state.vx[i]
			py+=state.m[i]*state.vy[i]
			pz+=state.m[i]*state.vz[i]

		return px,py,pz

plt.style.use('dark_background')

R=15
V=10
M=10

N=int(sys.argv[1])
dt=float(sys.argv[2])
Radius=float(sys.argv[3])

G=10

'''
theta=np.random.rand(N-1)*2*np.pi
phi=np.random.rand(N-1)*2*np.pi
Radius=np.random.rand(N-1)*R

x=Radius*np.cos(theta)*np.cos(phi)
y=Radius*np.cos(theta)*np.sin(phi)
z=Radius*np.sin(theta)

rad=(np.random.rand(N)+1)*0.2


x=np.append(x,0)
y=np.append(y,0)
z=np.append(z,0)

vx=[0]*N
vy=[0]*N
vz=[0]*N
m=np.random.rand(N-1)*M



center_mass=100*M
m=np.append(m,center_mass)
tot_mass=np.sum(m)


for i in range(N-1):
	r=(x[i]**2+y[i]**2+z[i]**2)*0.5
	v=(G*center_mass/r+G*tot_mass*r/R**2)**(0.5)
	x_h=x[i]/r
	y_h=y[i]/r
	z_h=z[i]/r

	vx[i]= v*(x_h*z_h)/(x[i]**2+y[i]**2)**0.5/r
	vy[i]= v*(y_h*z_h)/(x[i]**2+y[i]**2)**0.5/r
	vz[i]= -v*(x[i]**2+y[i]**2)**0.5/r
'''

x=np.random.rand(N)*R
y=np.random.rand(N)*R
z=np.random.rand(N)*R

vx=(np.random.rand(N-1)-0.5)*V
vy=(np.random.rand(N-1)-0.5)*V
vz=(np.random.rand(N-1)-0.5)*V

m=np.random.rand(N-1)*M
m=np.append(m,10*M)
tot_mass=np.sum(m)

vx=np.append(vx,0)
vy=np.append(vy,0)
vz=np.append(vz,0)

rad=(np.random.rand(N))*Radius


curr_state=particles(x,y,z,vx,vy,vz,m,rad)

fig=plt.figure("Gravity")
ax = fig.add_subplot(111, projection='3d',
					xlim=(-2*R, 2*R),
					ylim=(-2*R, 2*R),
					zlim=(-2*R, 2*R))

line, = ax.plot([], [], [],'o', color= (0,0,1,0.5),markersize=7)

p_vec_text = ax.text(-5, -20,-30, '', color=(1,1,1,0.5))

def init():
    line.set_data(curr_state.x, curr_state.y)
    line.set_3d_properties(curr_state.z)
    p_vec_text.set_text(' ')
    return line, p_vec_text

def animate(i):
	px,py,pz=curr_state.momentum()
	line.set_data(curr_state.x,curr_state.y)
	line.set_3d_properties(curr_state.z)

	p_vec_text.set_text('$\\langle\\vec{v}\\rangle$=(%.1f' %(px/tot_mass)+', %.1f'%(py/tot_mass)+', %.1f)'%(pz/tot_mass))
	curr_state.step(dt)
	return line, p_vec_text

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=1, blit=True, init_func=init)

ax.grid(False)
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
plt.show()




