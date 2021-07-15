import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

class particles:
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

				rx,ry,rz=x[i]-x[j],y[i]-y[j],z[i]-z[j]

				r=(rx**2+ry**2+rz**2)**0.5
				G=1
				M=1
				rad=((m[i]/M)**(1/3)+(m[j]/M)**(1/3))*0.15

				outside=(r>rad)
				inside=1-outside
				n=-2
				f=r**n*outside+inside*r*rad**(n-1)

				ax[i]+=-G*m[j]*rx/r*f
				ay[i]+=-G*m[j]*ry/r*f
				az[i]+=-G*m[j]*rz/r*f

		return ax,ay,az

	def step(state,dt):

		ax,ay,az=state.acceleration()

		state.vx=state.vx+ax*dt
		state.vy=state.vy+ay*dt
		state.vz=state.vz+az*dt
		state.x=state.x+state.vx*dt
		state.y=state.y+state.vy*dt
		state.z=state.z+state.vz*dt

	def momentum(state):
		return np.sum(m*vx),np.sum(m*vy),np.sum(m*vz)

	def energy(state):
		return 0.5*np.sum(m*(vx**2+vy**2+vz**2))

	def center_mass(state):
		return np.sum(m*x)/np.sum(m),np.sum(m*y)/np.sum(m),np.sum(m*z)/np.sum(m)

def ring_force_fact(N):
	if N==1:
		return 0

	r=np.linspace(1,N-1,N-1)
	y=1/np.sin(np.pi*r/N)/4/N

	return np.sqrt(sum(y))

plt.style.use('dark_background')

N=int(sys.argv[1])
dt=float(sys.argv[2])
R=2
Rad=1
V=1
M=1000
G=1
center_mass=0
a=ring_force_fact(N)

m=M-np.linspace(1,M,N)
ring_mass=np.sum(m)
#m=np.append(m,center_mass)
#m[len(m)-1]*=center_mass_fact
tot_mass=np.sum(m)

theta=np.linspace(np.pi/2*0,np.pi,N)#np.random.rand(N)*np.pi
phi=np.linspace(0,np.pi*2,N)
r=np.linspace(Rad/N,Rad,N)#*np.random.rand(N)
v=np.sqrt(G*ring_mass/r*a**2+G*center_mass/r)#np.random.rand(N)*V
theta_v=np.random.rand(N)*np.pi
phi_v=np.random.rand(N)*np.pi*2


x=r*np.cos(phi)*np.sin(theta)
y=r*np.sin(phi)*np.sin(theta)
z=r*np.cos(theta)

#x[len(x)-1]=0
#y[len(y)-1]=0
#z[len(z)-1]=0

vx=-v*y/r*0#*np.cos(phi_v)*np.sin(theta_v)
vy= v*x/r*0#np.sin(phi_v)*np.sin(theta_v)
vz=0*v*np.cos(theta_v)
'''
x=np.append(x,0)
y=np.append(y,0)
z=np.append(z,0)
vx=np.append(vx,0)
vy=np.append(vy,0)
vz=np.append(vz,0)

N=len(m)
#vx[len(vx)-1]=0
#vy[len(vy)-1]=0
#vz[len(vz)-1]=0

#v_x=np.sum(m*vx)/tot_mass
#v_y=np.sum(m*vy)/tot_mass
#v_z=np.sum(m*vz)/tot_mass

#r_x=np.sum(m*x)/tot_mass
#r_y=np.sum(m*y)/tot_mass
#r_z=np.sum(m*z)/tot_mass

#vx-=v_x
#vy-=v_y
#vz-=v_z

#x-=r_x
#y-=r_y
#z-=r_z
'''
curr_state=particles(x,y,z,vx,vy,vz,m)
line=[None]*N

fig=plt.figure("Gravity")
ax = fig.add_subplot(111,projection='3d', xlim=(-1.5*R, 1.5*R),ylim=(-1.5*R, 1.5*R),zlim=(-1.5*R,1.5*R))

for i in range(len(line)):
	line[i], = ax.plot([], [], [],'o',markersize=int((m[i]*500/M)**(1/3))+1)

line = np.append(line,ax.text(-1.4*R, -1.4*R, -1.4*R, '', fontsize=6.5, color=(0,1,0,0.3)))
line = np.append(line,ax.text(-1.4*R, -1.4*R, -1.2*R, '', fontsize=6.5, color=(0,1,0,0.3)))
line = np.append(line,ax.text(-1.4*R, -1.4*R, -1.0*R, '', fontsize=6.5, color=(0,1,0,0.3)))
E_0=2000


def animate(i):
	px,py,pz=curr_state.momentum()
	rx,ry,rz=curr_state.center_mass()

	E=curr_state.energy()
	curr_state.step(dt)
	for j in range(len(line)-3):
		line[j].set_data(curr_state.x[j],curr_state.y[j])
		line[j].set_3d_properties(curr_state.z[j])
		E=(curr_state.vx[j]**2+curr_state.vy[j]**2+curr_state.vz[j]**2)*abs(m[j])*0.5
		line[j].set_color((E/(E_0+E),0,E_0/(E_0+E),0.5))
		#line[j].set_color((0,0,0,np.cos(E/E_0)**2))
	if(i%2==0):
		line[len(line)-3].set_text('K.E.=%.2f'%E)
	acc=10e-7
	line[len(line)-2].set_text('$\\vec{v}_{cm}$=(%.1f'%(px/tot_mass+acc)+', %.1f'%(py/tot_mass+acc)+', %.1f)'%(pz/tot_mass+acc))
	line[len(line)-1].set_text('$\\vec{r}_{cm}$=(%.1f'%(rx+acc)+', %.1f'%(ry+acc)+', %.1f)'%(rz+acc))

	return line

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=1, blit=True)
ax.grid(False)
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
plt.show()


