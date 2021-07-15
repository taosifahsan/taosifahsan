from scipy import integrate,signal
import matplotlib.pyplot as plt
import numpy as np

#real spectrum
#normalized
#singularity at 0 for F/E avoided
def raw_spectrum(E):
	#spectrum shape
	F=np.exp(-(E-1)**2/0.301**2)

	dE=E[1]-E[0]#space between two bins
	F=F/[sum(F)*dE]#normalization
	F=F*(E[0]<E)#avoiding the division by 0
	return F

#algorithm to calculate first m pulsepule-up terms via convolution
#time complexity o(nlogn*m), n=len(E)
#m in number of terms, a is triangularity
def pileupterms(F,E,m,a):
	dE=E[1]-E[0]
	#saving convolution update term
	#I=int^E_0 P(E')/E' dE'
	I=integrate.cumtrapz(F/E, E, initial=0)
	#X(E)=(1-a)*P(E)+a*I(\inf)-a*I(E)
	X=(1-a)*F+a*I[len(I)-1]-a*I
	#first m terms of PPU
	P=np.array([[0.0]*len(E)]*m)
	#seed
	#p_0(E)=P(E)
	P[0]=F
	#convolution
	#p_n(E)=int_0^E p(E')x(E-E')dE'
	for n in range(m-1):
		#fast fourier transform to reduce
		#time complexity of convolution to o(nlogn)
		P[n+1]=signal.fftconvolve(P[n], X)[:len(E):]*dE	
	return P

#poisson distribution
def poisson(ut,m):
	p=[0.0]*m
	p[0]=np.e**(-ut)
	for i in range(m-1):
		p[i+1]=p[i]*(ut)/(i+1)
	return p

#returns apparent spectrum due to pile up
def apparent_spectrum(F,E,m,a,ut):
	#extracting pileup coefficient terms
	P=pileupterms(F, E, m, a)
	#extracting poisson distribution
	pois=poisson(ut,m)
	#sums all ppu terms
	#P_a(E)=Sum_n P_n(E)*pois(ut,n)
	P_a=np.array([0.0]*len(E))
	for n in range(m):
		P_a+=P[n]*pois[n]
	return P_a

def extra_terms(F,E,m,a,ut):
	#extracting pileup coefficient terms
	P=pileupterms(F, E, m, a)
	#extracting poisson distribution
	pois=poisson(ut,m)
	#sums all ppu terms
	#P_a(E)=Sum_n P_n(E)*pois(ut,n)
	P_a=np.array([0.0]*len(E))
	for n in range(1,m):
		P_a+=P[n]*pois[n]
	return P_a


#moving average filter with weight
def mov_avg(y, w):
	y_smooth=y
	for i in range(len(y)-len(w)):
		y_smooth[i+int(len(w)/2)]=sum(y[i:i+len(w):]*w)/sum(w)
	return y_smooth

#plot above a limit/bar
def plot(y,bar,w):
	return np.maximum(mov_avg(np.array(y), w),bar)

N=1000#number of steps in integral
m=100#number of terms in poison series
start=10E-12#parameter to avoid dividing by 0
stop=10#end of energy array

#necessary parameters
ut=2.2#count-rate*PPR time
a=0.7#triangularity
w=[1]*1#weight of moving average filter
bar=10E-10#lowest bound of plot

E=np.linspace(start,stop*(1-1/N),N)#energy array
F=raw_spectrum(E)#creating the raw spectrum
plt.semilogy(E,plot(F,bar,w),label='Raw Spectrum')
P_a=apparent_spectrum(F,E,m,a,ut)
plt.semilogy(E,plot(P_a,bar,w),label='Piled-up, a = '+str(round(a,2))+', ut = '+str(round(ut,2)))

plt.grid(True, which="both", ls="-.")
plt.legend()
plt.show()




