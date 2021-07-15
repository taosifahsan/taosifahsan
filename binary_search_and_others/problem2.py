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

X = [0]*len(lines)
Y = [0]*len(lines)
Yerr = [0]*len(lines)
for i in range(len(lines)):
	X[i] = float(lines[i][0])
	Y[i] = float(lines[i][1])
	Yerr[i] = np.sqrt(np.max((Y[i],1)))

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False

plt.errorbar(x=X, y=Y, yerr=Yerr, linewidth=3, color='red', fmt='o', label='data')

def test_func(X, A, x_0, s):
    return A*np.exp(-((X-x_0)**2)/(2*(s**2)))

fitErrors = np.sqrt(np.array(Y)+1.)
initialGuess = [np.max(np.array(Y)), np.average(X), 1.]

params, params_covariance = optimize.curve_fit(test_func, X, Y,
	p0=initialGuess, sigma=fitErrors)
xx = np.linspace(X[0],X[len(X)-1])
plt.errorbar(x=xx, y=test_func(xx, params[0], params[1], params[2]),
	linewidth=3, color='black', label='fit')

plt.legend(loc='best')
plt.ylabel('Y (#)')
plt.xlabel('X (#)')

#plt.ylim(-5,20)

fit_params = np.round(params, 4)
fit_params_std = np.round(np.sqrt(params_covariance), 4)

plt.title(sys.argv[1]+': A='+str(fit_params[0])+', x$_0$='+str(fit_params[1])
	+', s='+str(fit_params[2])
	+'\n$\sigma_A$='+str(fit_params_std[0][0])+', $\sigma_{x_0}$='
	+str(fit_params_std[1][1])+', $\sigma_s$='+str(fit_params_std[2][2]))
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))

residuals = np.array(Y) - test_func(np.array(X), params[0], params[1], params[2])
plt.errorbar(x=X, y=residuals, linewidth=3, color='blue', fmt='v')

plt.ylabel('Y Residual (#)')
plt.xlabel('X (#)')
#plt.ylim(-5,20)
plt.title(sys.argv[1]+': residuals')
plt.tight_layout(pad=0)
plt.grid(linestyle='--')

plt.show()
