import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
from scipy import optimize

fName = sys.argv[1]
f = open(fName)
lines = f.readlines()
for i in range(len(lines)):
	lines[i] = lines[i].split()

I = [0]*len(lines)
V = [0]*len(lines)
for i in range(len(lines)):
	I[i] = float(lines[i][0])
	V[i] = float(lines[i][1])

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False

plt.errorbar(x=I, y=V, linewidth=3, color='red', fmt='o', label='data')

def test_func(I, R, V_0):
    return I*R + V_0

params, params_covariance = optimize.curve_fit(test_func, I, V)
xx = np.linspace(I[0],I[len(I)-1])
plt.errorbar(x=xx, y=test_func(xx, params[0], params[1]),
	linewidth=3, color='black', label='fit')

plt.legend(loc='best')
plt.ylabel('Voltage (V)')
plt.xlabel('Current (A)')

#plt.ylim(-5,20)

fit_params = np.round(params, 4)
fit_params_std = np.round(np.sqrt(params_covariance), 4)

plt.title(sys.argv[1]+': R='+str(fit_params[0])+', V$_0$='+str(fit_params[1])
	+', $\sigma_R$='+str(fit_params_std[0][0])+', $\sigma_{V_0}$='
	+str(fit_params_std[1][1]))
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))

residuals = np.array(V) - test_func(np.array(I), params[0], params[1])
plt.errorbar(x=I, y=residuals, linewidth=3, color='blue', fmt='v')

plt.ylabel('Voltage Residual (V)')
plt.xlabel('Current (A)')
#plt.ylim(-5,20)
plt.title(sys.argv[1]+': residuals')
plt.tight_layout(pad=0)
plt.grid(linestyle='--')

plt.show()
