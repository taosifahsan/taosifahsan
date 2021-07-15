from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.animation as animation
from matplotlib import gridspec

class particles:

	def __init__(state, x=[],y=[],z=[],vx=[],vy=[],vz=[],box=[]):

		state.x=x
		state.y=y
		state.z=z
		state.vx=vx
		state.vy=vy
		state.vz=vz
		state.box=box

	def add(state,x,y,vx,vy,m):
		state.x.append(x)
		state.y.append(y)
		state.vx.append(vx)
		state.vy.append(vy)
		state.vz.append(vz)
		state.box.append(box)

	def step(state,g,dt):

		x_min=box[0]
		x_max=box[1]
		y_min=box[2]
		y_max=box[3]
		z_min=box[4]
		z_max=box[5]

		for i in range(len(state.x)):

			inside_x=(x_min<state.x[i]+state.vx[i]*dt)&(state.x[i]+state.vx[i]*dt<x_max)
			inside_y=(y_min<state.y[i]+state.vy[i]*dt)&(state.y[i]+state.vy[i]*dt<y_max)
			inside_z=(z_min<state.z[i]+state.vz[i]*dt)&(state.z[i]+state.vz[i]*dt<z_max)
			outside_x=1-inside_x
			outside_y=1-inside_y
			outside_z=1-inside_z

			state.vx[i]=(2*inside_x-1)*state.vx[i]
			state.vy[i]=(2*inside_y-1)*state.vy[i]
			state.vz[i]=(state.vz[i]-g*dt)*inside_z+(-1)*state.vz[i]*outside_z
			

			state.x[i]+=state.vx[i]*dt
			state.y[i]+=state.vy[i]*dt
			state.z[i]+=state.vz[i]*dt

	def v_ms(state):
		sum=0
		for i in range(len(state.vx)):
			sum+=state.vx[i]**2+state.vy[i]**2+state.vz[i]**2
		return sum/len(state.vx)

	def height(state,dz):
		z=state.z
		n=len(z)
		zmax=state.box[5]
		zmin=state.box[4]

		N=int(zmax/dz-zmin/dz)+1
		distr=[0]*N
		for i in range(len(z)):
			distr[int((z[i]-zmin)/dz)]+=1/n

		return distr


box=[-5,5,-5,5,-5,5]
N=int(sys.argv[1])
dt=float(sys.argv[2])
v_x=10
v_y=10
v_z=12
g=9.81

k=np.random.rand(N)
v=np.sqrt(2*g*9)*np.linspace(0,1,N)#*k**2*np.exp(-k**2)
v=10*np.exp(-v**2)
dz=(box[5]-box[4])*0.1

fact2=1.0

curr_state=particles()
curr_state.box=box
theta_v=np.random.rand(N)*np.pi
phi_v=np.random.rand(N)*2*np.pi
#curr_state.vx=(2*np.random.rand(N)-1)*v_x
#curr_state.vy=(2*np.random.rand(N)-1)*v_y
#curr_state.vz=(2*np.random.rand(N)-1)*v_z

curr_state.vx=v*np.cos(phi_v)*np.sin(theta_v)
curr_state.vy=v*np.sin(phi_v)*np.sin(theta_v)
curr_state.vz=v*np.cos(theta_v)

beta=curr_state.v_ms()/(3*g)

curr_state.x=np.random.rand(N)*(box[1]-box[0])*0+box[0]
curr_state.y=np.random.rand(N)*(box[3]-box[2])*0+box[2]
#curr_state.z=np.random.exponential(beta,N)+box[4]
curr_state.z=np.random.rand(N)*(box[5]-box[4])*0+box[4]

for i in range(N):
	if curr_state.z[i]>=box[5]:
		curr_state.z[i]=box[5]*0.99

plt.style.use('dark_background')

fact=1.01
box=[box[0]*fact,box[1]*fact,box[2]*fact,box[3]*fact,box[4]*fact,box[5]*fact]

z_x=np.linspace(box[0],box[1],2)
z_y=np.linspace(box[2],box[3],2)
z_x, z_y = np.meshgrid(z_x, z_y)
z_low=z_x*0+box[4]
z_high=z_x*0+box[5]

x_y=np.linspace(box[2],box[3],2)
x_z=np.linspace(box[4],box[5],2)
x_y, x_z  = np.meshgrid(x_y, x_z)
x_low=z_x*0+box[0]
x_high=z_x*0+box[1]

y_x=np.linspace(box[0],box[1],2)
y_z=np.linspace(box[4],box[5],2)
y_x, y_z  = np.meshgrid(y_x, y_z)
y_low=y_x*0+box[2]
y_high=y_x*0+box[3]

fig = plt.figure("Bound")

ax = fig.add_subplot(121, projection='3d',
					xlim=(box[0]*fact2, box[1]*fact2),
					ylim=(box[2]*fact2, box[3]*fact2),
					zlim=(box[4]*fact2, box[5]*fact2))

graph=fig.add_subplot(122,xlim=(box[0],box[1]))#,ylim=(0,N*dz*1.2))



surface_color=(0.1,0.1,0.1,0.5)
ax.plot_surface(z_x,z_y,z_low, color=surface_color)
ax.plot_surface(z_x,z_y,z_high, color=surface_color)
ax.plot_surface(x_low,x_y,x_z, color=surface_color)
ax.plot_surface(x_high,x_y,x_z, color=surface_color)
ax.plot_surface(y_x,y_low,y_z, color=surface_color)
ax.plot_surface(y_x,y_high,y_z, color=surface_color)

line_color=(1,1,1,1)
w=2
ax.plot([box[0],box[1]],[box[2],box[2]],[box[4],box[4]],color=line_color,lw=w)
ax.plot([box[0],box[1]],[box[2],box[2]],[box[5],box[5]],color=line_color,lw=w)
ax.plot([box[0],box[1]],[box[3],box[3]],[box[4],box[4]],color=line_color,lw=w)
ax.plot([box[0],box[1]],[box[3],box[3]],[box[5],box[5]],color=line_color,lw=w)
ax.plot([box[0],box[0]],[box[3],box[2]],[box[4],box[4]],color=line_color,lw=w)
ax.plot([box[1],box[1]],[box[3],box[2]],[box[4],box[4]],color=line_color,lw=w)
ax.plot([box[0],box[0]],[box[3],box[2]],[box[5],box[5]],color=line_color,lw=w)
ax.plot([box[1],box[1]],[box[3],box[2]],[box[5],box[5]],color=line_color,lw=w)
ax.plot([box[0],box[0]],[box[3],box[3]],[box[4],box[5]],color=line_color,lw=w)
ax.plot([box[1],box[1]],[box[3],box[3]],[box[4],box[5]],color=line_color,lw=w)
ax.plot([box[0],box[0]],[box[2],box[2]],[box[4],box[5]],color=line_color,lw=w)
ax.plot([box[1],box[1]],[box[2],box[2]],[box[4],box[5]],color=line_color,lw=w)

temp=graph.text(box[5]*0.5,0.8, ' ', color=(1,1,1))

particle_animation, = ax.plot([], [], [], 'o', markersize=int(10/np.log(N)), zdir='z',
				color=(1,0,0,0.3))
box=[box[0]/fact,box[1]/fact,box[2]/fact,box[3]/fact,box[4]/fact,box[5]/fact]


zmax=curr_state.box[5]
zmin=curr_state.box[4]
h_x=np.linspace(zmin,zmax,int(zmax/dz-zmin/dz)+1)

h_y=curr_state.height(dz)
graph_animation,=graph.semilogy([],[],'b.')
#graph.grid(True, which="both", ls="--")

graph.set_ylim(10e-4,1.2)
graph.set_xlabel('z')
graph.set_ylabel('Number of particle')


def init():
	h_y=curr_state.height(dz)
	particle_animation.set_data(curr_state.x,curr_state.y)
	particle_animation.set_3d_properties(curr_state.z)
	graph_animation.set_data(h_x,h_y)
	temp.set_text(' ')
	return particle_animation, temp, graph_animation,

def animate(i):
	h_y=curr_state.height(dz)
	particle_animation.set_data(curr_state.x,curr_state.y)
	particle_animation.set_3d_properties(curr_state.z)
	graph_animation.set_data(h_x,h_y)
	temp.set_text('T=%.1f'%curr_state.v_ms())
	curr_state.step(g, dt)
	return particle_animation, temp, graph_animation,

ani = animation.FuncAnimation(fig, animate, frames=6000,
			 interval=1, blit=True, init_func=init)

graph.set_aspect('auto')
ax.axis('off')

plt.show()




