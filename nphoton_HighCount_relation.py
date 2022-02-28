import numpy as np 
import matplotlib.pyplot as plt
import numpy.random
#-------------------------------------------------------------------------------------------
# THESE ARE NECESSARY FUNCTIONS AND METHODS
#-------------------------------------------------------------------------------------------
slope = np.array([])
yintercept = np.array([])
# helps in doing a moving average
w=[1,3,5,8,10,8,5,3,1] # weigths of moving average
def mov_avg(y, w):
	y_smooth=y
	for i in range(len(y)-len(w)):
		y_smooth[i+int(len(w)/2)]=sum(y[i:i+len(w):]*w)/sum(w)
	return y_smooth

# cuts of graph below a lower limit
bar = 1e-6
def plot(y,bar,w):
	return np.maximum(mov_avg(np.array(y), w),bar)


# this returns a trapezoid gor given height, position, rise and flat top time
def trap(h,t_temp,ti, tr,tf):
	part1=(ti<t_temp)*(t_temp<=ti+tr)*(t_temp-ti)/tr*h
	part2=(ti+tr<t_temp)*(t_temp<ti+tr+tf)*h
	part3=(tr+tf+ti<=t_temp)*(t_temp<2*tr+tf+ti)*(2*tr+tf+ti-t_temp)/tr*h
	return part1+part2+part3


# necessary for the count rate vs maximum plot
pulse_rates = np.linspace(2,10,10)
triangularities = [200/212]#np.linspace(0.8, 1.0,11)
maximum_array = np.array([])

#-------------------------------------------------------------------------------------------
# THIS IS WHERE OUR INPUT GOES IN
#-------------------------------------------------------------------------------------------

# this is the input spectrum
accuracy=1000 # number of bins in input spectrum
E=np.linspace(0.01, 10,accuracy) # energy array of input spectrum
dE=E[1]-E[0] 
input_spectrum=np.exp(-(E-1)**2/0.2**2) # input spectrum
P=input_spectrum/sum(input_spectrum)

#-------------------------------------------------------------------------------------------
# PARAMETERS
#-------------------------------------------------------------------------------------------

#pulse_rate = 1 # this is pulse per unit time
pulse_number = 5000000 # this is total number of pulses
resolution = 10 # number of bins in unit time

fig = plt.figure(1)
ax=fig.add_subplot(111)
ax.set_xlabel('count rate times dead time, $\\mu t_d$', fontsize=20)
ax.set_ylabel('$E_{max}/\\langle spectrum \\rangle$', fontsize=20)
ax.grid(True, which="both", ls="-.")


for a in triangularities:
	maximum_array = np.array([])
	tr=a+1e-9#rise time
	tf=1-a-1e-9 #flat top time
	td=2*tr+tf # total time length of a pulse 

	#jr=int(tr*resolution) # number of bins in rising range of a pulse
	#jf=int(tf*resolution) # number of bins in flat top range of a pulse
	jd=int(td*resolution) # total number of bins in a pulse
	for pulse_rate in pulse_rates:
		#-------------------------------------------------------------------------------------------
		# CREATING THE VOLTAGE ARRAY, O(pulse_number*jd)
		#-------------------------------------------------------------------------------------------
		Time = int(pulse_number/pulse_rate)  #time to run the experiment
		t=np.linspace(0,Time,Time*resolution)  # time array 
		Total_time_bins=len(t) # time array has Time*resolution bins
		voltage=t*0.0 # empty voltage array
		
		# this returns an height from the input function
		Energy_random_raw = np.random.choice(E, size=pulse_number, replace=True, p=P)

		for i in range(pulse_number):
			# we smooth it out more
			Energy_random =np.random.uniform(Energy_random_raw[i]-dE/2,Energy_random_raw[i]+dE/2)

			ti=np.random.uniform(Time-td) #choses a random time
			#adds trapezoid
			ji=int(ti*resolution) # site of the time
			# the elements that needs to be updated
			t_temp=np.linspace(ti, ti+td, jd)
			#creating the trapezoid 
			y=trap(Energy_random, t_temp, ti, tr, tf)
			# update the necessary elements by adding the trapezoid to it
			for j in range(len(y)):
				voltage[ji+j]+=y[j]
				

		#-------------------------------------------------------------------------------------------
		#REGISTER PEAKS AS ENERGY OF PHOTONS,  O(Time*Resolution)
		#-------------------------------------------------------------------------------------------

		peak=np.array([])
		#orange=t*0
		i=0
		baseline=10**-9
		while(i<len(t)-1):
			#if voltage starts to rise start looking for peak
			if voltage[i+1] > voltage[i]+baseline:
				j=0
				#look until it starts to fall
				while voltage[i+j+1] > voltage[i+j]-baseline and i+j+1 < len(t)-1:
					j+=1
				#it fell so peak is found
				i+=j
				#register the peak
				peak=np.append(peak,voltage[i])		
				#orange[i]=voltage[i]
			i+=1

		#-------------------------------------------------------------------------------------------
		# CREATE THE SPECTRUM FORM THE PEAKS REGISTERED O(len(peak))
		#-------------------------------------------------------------------------------------------
		N=1000 # number of bins in out put spectrum, ideally set equal to accuracy variable
		spectrum=np.linspace(0,0,N) #register counts
		Energy_array=np.linspace(peak.min(), peak.max() ,N) #associated energy array
		for i in range(len(peak)):
			Energy_bin = int (peak[i]*(N/peak.max())-1) #bin associated with peak
			spectrum[Energy_bin]+=1 #increase count

		integral = np.sum(spectrum)*((peak.max()-peak.min())/N) 
		spectrum = spectrum/integral # normalize
		spectrum = plot(spectrum, bar, w) #smooth it
		#-------------------------------------------------------------------------------------------


		'''
		# This plots a graph where we can see individual peak registry behind the scene 
		# remove comments to make it work
		fig = plt.figure()
		ax1=fig.add_subplot(111)
		ax1.set_title("voltage vs time")
		ax1.set_xlabel('time')
		ax1.set_ylabel('voltage')
		ax1.plot(t,voltage)
		ax1.plot(t,orange)
			
		#-------------------------------------------------------------------------------------------
		# Plot the graphs
		#-------------------------------------------------------------------------------------------
		fig = plt.figure()
		ax2=fig.add_subplot(111)
		ax2.set_title('Total time = '+str(Time)+', Count Rate = '+str(pulse_rate)+'\n'+
			'Rise time = '+str(tr)+', Flat-top time = '+str(tf))
		ax2.set_ylabel('Count')
		ax2.set_xlabel('Energy')
		#ax2.plot(E,input_spectrum)
		ax2.plot(Energy_array, spectrum)
		ax2.grid(True, which="both", ls="-.")

		plt.show()
		'''
		#-------------------------------------------------------------------------------------------
		# necessary for the count rate vs maximum plot
		# remove comment if necessary
		i_r=np.where(spectrum==spectrum.max())
		maximum_array=np.append(maximum_array, Energy_array[i_r])
	maximum_array=maximum_array[:len(pulse_rates)]
	fit = np.polyfit(pulse_rates, maximum_array, 1)
	color=next(ax._get_lines.prop_cycler)['color']
	ax.plot(pulse_rates,maximum_array, '.',color=color)
	ax.plot(pulse_rates,pulse_rates*fit[0]+fit[1], '-',color=color)#+str(a))
	slope=np.append(slope, fit[0])
	yintercept=np.append(yintercept, fit[1])
ax.legend(fontsize=20)
print(slope)
print(yintercept)
'''
fig2 = plt.figure(2)
ax1=fig2.add_subplot(121)
ax1.set_ylabel('slope', fontsize=20)
ax1.set_xlabel('triangularity, a', fontsize=20)
ax1.plot(triangularities, slope)
ax1.grid(True, which="both", ls="-.")

ax2=fig2.add_subplot(122)
ax2.set_ylabel('y-intercept', fontsize=20)
ax2.set_xlabel('triangularity, a', fontsize=20)
ax2.plot(triangularities, yintercept)
ax2.grid(True, which="both", ls="-.")
'''
plt.show()

	





	