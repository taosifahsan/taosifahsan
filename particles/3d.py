from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.animation as animation

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

box=[-5,5,-5,5,-5,5]
N=int(sys.argv[1])
dt=float(sys.argv[2])
v_x=5
v_y=5
v_z=10
g=9.81

fact2=1.0

curr_state=particles()
curr_state.box=box
curr_state.vx=(2*np.random.rand(N)-1)*v_x
curr_state.vy=(2*np.random.rand(N)-1)*v_y
curr_state.vz=(2*np.random.rand(N)-1)*v_z

beta=curr_state.v_ms()/(3*g)

curr_state.x=np.random.rand(N)*(box[1]-box[0])+box[0]
curr_state.y=np.random.rand(N)*(box[3]-box[2])+box[2]
curr_state.z=np.random.exponential(beta,N)+box[4]

for i in range(N):
	if curr_state.z[i]>=box[5]:
		curr_state.z[i]=box[5]*0.99

plt.style.use('dark_background')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', aspect='auto', autoscale_on=True, 
					xlim=(box[0]*fact2, box[1]*fact2), ylim=(box[2]*fact2, box[3]*fact2), zlim=(box[4]*fact2, box[5]*fact2))


line, = ax.plot([], [], [],'o', markersize=1, zdir='z',color=(1,0,0,0.5))

def init():
    line.set_data(curr_state.x,curr_state.y)
    line.set_3d_properties(curr_state.z)
    return line, 

def animate(i):
	line.set_data(curr_state.x,curr_state.y)
	line.set_3d_properties(curr_state.z)
	curr_state.step(g, dt)
	return line, 

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=1, blit=True, init_func=init)
plt.axis('off')
plt.show()