import numpy as np 
import sounddevice as sd 
import matplotlib.pyplot as plt 
import matplotlib 

tone_freq = '330'
a = '3'
b = '8'

fs = 44100 
tau = 14 #s
rec_a = sd.rec(int(fs*tau), samplerate=fs, channels=1)
sd.wait()
print('#####\nnow\n#####')
rec_b = sd.rec(int(fs*tau), samplerate=fs, channels=1)
sd.wait()
tt = np.linspace(0,tau,num=fs*tau)

with open(a+'in'+b+'in'+tone_freq+'Hz.txt', 'w') as txt:
	txt.write('time(s) 3in 8in\n')
	for i in range(tt.size):
		line = str(tt[i])+' '+str(rec_a[i][0])+' '+str(rec_b[i][0])+'\n'
		txt.write(line)

plt.rc('font', family='serif', serif = "cmr10", size=20)
plt.rcParams['mathtext.fontset']='cm'
plt.figure(figsize=(10,6))
matplotlib.rcParams['axes.unicode_minus'] = False
plt.errorbar(x=tt[int(6*fs):-int(2*fs)], y=rec_a[int(6*fs):-int(2*fs)],
	linewidth=0.15, fmt='', color='red', label='y='+a+'in')
plt.errorbar(x=tt[int(6*fs):-int(2*fs)], y=rec_b[int(6*fs):-int(2*fs)],
	linewidth=0.15, fmt='', color='blue', label='y='+b+'in')
plt.legend(loc='best', fontsize=20)
plt.xlabel('time (s)')
plt.ylabel('signal')
plt.title('frequency = '+tone_freq+'Hz')
plt.tight_layout(pad=0)
plt.grid(linestyle='--')
plt.show()