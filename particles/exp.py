import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

class loop:
	def __init__(state,x,y,z,vx,vy,vz,m):
		state.x=x
		state.y=y
		state.z=z
		state.vx=vx
		state.vy=vy
		state.vz=vz
		state.m=m


	def add(state,x,y,z,vx,vy,vz):
		state.x.append(x)
		state.y.append(y)
		state.z.append(z)
		state.vx.append(vx)
		state.vy.append(vy)
		state.vz.append(vz)
		state.m.append(m)

	def acceleration(state):

		x=state.x
		y=state.y
		z=state.z
		m=state.m

		ax=state.m*0
		ay=state.m*0
		az=state.m*0

		for i in range(len(x)):
			for j in range(len(y)):
				if j==i:
					continue

				rx,ry,rz=x[j]-x[i],y[j]-y[i],z[j]-z[i]

				r=(rx**2+ry**2+rz**2)**0.5
				n=-0
				G=1
				ax[i]+=G*m[j]*rx*r**(n-1)
				ay[i]+=G*m[j]*ry*r**(n-1)
				az[i]+=G*m[j]*rz*r**(n-1)

		return ax,ay,az

	def step(state,dt):

		ax,ay,az=state.acceleration()

		for i in range(len(state.x)):
			state.vx[i]+=ax[i]*dt
			state.vy[i]+=ay[i]*dt
			state.vz[i]+=az[i]*dt
			state.x[i]+=vx[i]*dt
			state.y[i]+=vy[i]*dt
			state.z[i]+=vz[i]*dt

	def momentum(state):
		return np.sum(m*vx),np.sum(m*vy),np.sum(m*vz)

	def energy(state):
		return 0.5*np.sum(m*(vx**2+vy**2+vz**2))


plt.style.use('dark_background')

N=50
dt=0.01
R=1
V=1
M=1

theta=np.random.rand(N)*np.pi
phi=np.random.rand(N)*np.pi*2
r=R*np.random.rand(N)

theta_v=np.random.rand(N)*np.pi
phi_v=np.random.rand(N)*np.pi*2
v=V*np.random.rand(N)


x=r*np.cos(phi)*np.cos(theta)
y=r*np.sin(phi)*np.cos(theta)
z=r*np.sin(theta)

vx=v*np.cos(phi_v)*np.cos(theta_v)
vy=v*np.sin(phi_v)*np.cos(theta_v)
vz=v*np.sin(theta_v)

m=M*np.random.rand(N)

tot_mass=np.sum(m)
v_x=np.sum(m*vx)/tot_mass
v_y=np.sum(m*vy)/tot_mass
v_z=np.sum(m*vz)/tot_mass

vx-=v_x
vy-=v_y
vz-=v_z

curr_state=loop(x,y,z,vx,vy,vz,m)
line=[None]*N

fig=plt.figure()
ax = fig.add_subplot(111,projection='3d', xlim=(-1.5*R, 1.5*R),ylim=(-1.5*R, 1.5*R),zlim=(-1.5*R,1.5*R))
ax.set_aspect('auto')


for i in range(len(line)):
	line[i], = ax.plot([], [], [],'o',markersize=5)

line = np.append(line,ax.text(-1.2*R, -1.4*R, -1.4*R, '', color=(0,1,0,0.3)))
line = np.append(line,ax.text(-1.2*R, -1.4*R, -1*R, '', color=(0,1,0,0.3)))

def animate(i):
	px,py,pz=curr_state.momentum()
	E=curr_state.energy()
	curr_state.step(dt)
	for j in range(len(line)-2):
		line[j].set_data(curr_state.x[j],curr_state.y[j])
		line[j].set_3d_properties(curr_state.z[j])

		E=(curr_state.vx[j]**2+curr_state.vy[j]**2+curr_state.vz[j]**2)*abs(m[j])*0.5
		E_0=1
		line[j].set_color((1-np.exp(-E/E_0),0,np.exp(-E/E_0),0.75))
	if(i%2==0):
		line[len(line)-2].set_text('E=%.2f'%E)
	acc=10e-7
	line[len(line)-1].set_text('$\\vec{p}$=(%.1f'%(px+acc)+', %.1f'%(px+acc)+', %.1f)'%(px+acc))

	return line

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=4, blit=True)
ax.grid(False)
ax.xaxis.set_pane_color((0.0, 0.0, 1.0, 0.1))
ax.yaxis.set_pane_color((0.0, 0.0, 1.0, 0.1))
ax.zaxis.set_pane_color((0.0, 0.0, 1.0, 0.1))
plt.show()


