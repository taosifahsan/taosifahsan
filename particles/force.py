import numpy as np 
import sys
import matplotlib.pyplot as plt


def force(N):
	r=np.linspace(1,N-1,N-1)
	y=1/np.sin(np.pi*r/N)/4/N

	return np.sqrt(sum(y))


n=int(sys.argv[1])

x=np.linspace(1,n,n)
y=[None]*len(x)
for i in range(len(x)):
	y[i]=force(int(x[i]))

plt.plot(x,y, 'ro', markersize=1)

plt.xlabel("N")
plt.ylabel("$\\sqrt{\\frac{\\sum_{r=1}^{N-1}\\cosec{(\\frac{\\pi r}{N})}}{4N}}$")

print(y[len(y)-1])
plt.grid(True, which="both", ls="-.")
plt.legend()
plt.show()



