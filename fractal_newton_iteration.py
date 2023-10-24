import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# coloring/classifies all initial points in terms of their arrived roots
def classify(x,y,a):
    #initial points for complex numbers
    [x,y]=np.meshgrid(x,y)
    z0 = x+y*1j 
    #get the root it arrives upon
    zr = find_root_of_polynomials(z0,a) 
    #color the initial points according to the root they reached
    color = label_color(zr, a) 
    return color

# finds root of a polynomial prod_i (z-a_i) = 0 starting with z=z0 guess
# this is the heart of the algorithm
# we here take advantage of numpy matrix formalities to make the 
# code run much faster
def find_root_of_polynomials(z0,a):    
    divide_zero_smooth = 1e-16;
    # reshaping the given root array
    Ma = np.transpose(np.tile(a,(z0.shape[0],z0.shape[1],1)))
    #initial guess for the root
    zr = z0  
    # stop the count if accuracy or number of step reached
    eps = 1e-8 #accetped error
    error = 1e8 #initial error
    i = 0 # number of steps check
    Num_steps = int(sys.argv[3]) #maximum number of steps
    while(error > eps and i < Num_steps):
       # reshaping the calculated roots array
       Mz = np.tile(zr,(len(a),1,1))
       r = (Mz-Ma)+divide_zero_smooth*(Mz-Ma==0)
       # calculating the correction needed
       dz = 1/np.sum(1/r,axis=0)
       #correcting the root calculated so far
       zr -= dz
       # rough estimation of error
       error=abs(dz[0,0])
       i +=1
    return zr

# given the root, labels/colors it and thus classifies it
# we here take advantage of numpy matrix formalities to make the 
# code run much faster
def label_color(zr,a):  
    # here we find the argmin of the root we arrived at - the root that 
    # was given, thus giving us an idea which root it was
    # the argmin is the position of the given root in the given root array
    # the indice in the array is the color
    Ma = np.transpose(np.tile(a,(zr.shape[0],zr.shape[1],1)))
    Mz = np.tile(zr,(len(a),1,1))
    color = np.argmin(np.abs(Mz-Ma),axis=0)
    return color

# this function can be used to create an array of given roots
# of the polynomial
# N is the number of roots
# spread is a measure of randomness in the root distribution
def set_roots(N,spread):
    theta = np.linspace(0,2*np.pi*(1-1/N),N)
    r1 = 2*np.random.rand(1,N)-1
    r2 = 2**np.random.rand(1,N)-1
    A = 0.5+r1*spread+r2*spread*1j
    return A*np.exp(theta*1j)

# set design aspect, color schemes, color maps here
def set_color_map():
    cdict=      [(0.2, 0.2, 1.0, 0.0),
                (0.5, 0.5, 1.0, 0.5),
                (0.8, 0.8, 1.0, 1.0)] 
    return LinearSegmentedColormap.from_list('my_list', cdict, N=int(sys.argv[2]))

# plot the result here
def plot_fractal(color):
    plt.style.use("dark_background")
    plt.imshow(color, cmap=set_color_map(), interpolation='nearest',alpha=1)
    plt.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False) 
    plt.show()  

# main()
N_grid = int(sys.argv[1]) #this gives the number of grids
N_roots = int(sys.argv[2]) #this gives the number of roots
x = np.linspace(-1,1,N_grid)#initial condition for real part
y = np.linspace(-1,1,N_grid)#initial condition for imaginary part
plot_fractal(classify(x,y,set_roots(N_roots,0.1))) #plot the fractals
