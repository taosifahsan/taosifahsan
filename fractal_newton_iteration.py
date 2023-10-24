# The code plots the newton-raphson iteration fractal for any given polynomial for any set of roots
# run by writing the following in terminal
# >python3 [codename.py] N_grid N_roots Num_steps

# N_grid*N_grid is the pixel number
# N_roots number of roots
# Num_steps gives the number of iterations in the fractal

# def roots(N, spread) method can be used to manually set roots to be whatever we desire in complex plain
# by writing the return [z1, z2, ...., zn] array. Currently, it automatically chooses default sets of 
# randomized roots

import matplotlib.pyplot as plt
import numpy as np
import sys

# coloring/classifies all initial points in terms of their arrived roots
def main_algorithm(x,y,a):

    #initial points for complex numbers
    [x,y]=np.meshgrid(x,y)
    z0 = x+y*1j 

    #get the root it arrives upon
    zr = findroot_poly(z0,a) 

    #color the initial points according to the root they reached
    color = set_color(zr, a) 
    return color

# finds root of a polynomial prod_i (z-a_i) = 0 starting with z=z0 guess
# this is the heart of the algorithm
# we here take advantage of numpy matrix formalities to make the 
# code run much faster
def findroot_poly(z0,a): 
    eps = 1e-10 #accetped erro
    error = 1e8 #initial error

    # reshaping the given root array
    Ma = np.transpose(np.tile(a,(z0.shape[0],z0.shape[1],1)))

    #initial guess for the root
    zr = z0

    while(error>eps):
       # reshaping the calculated roots array
       Mz = np.tile(zr,(len(a),1,1))

       # calculating the correction needed
       dz = 1/np.sum(1/(Mz-Ma+eps),axis=0)

       #correcting the root calculated so far
       zr -= dz

       # rough estimation of error
       error=abs(dz[0,0])

    return zr

# given the root, labels/colors it and thus classifies it
# we here take advantage of numpy matrix formalities to make the 
# code run much faster
def set_color(zr,a):  

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
def roots(N,spread):
    theta = np.linspace(0,2*np.pi*(1-1/N),N)
    r1 = 2*np.random.rand(1,N)-1
    r2 = 2**np.random.rand(1,N)-1
    A = 0.5+r1*spread+r2*spread*1j
    return A*np.exp(theta*1j)

# main()
N_grid = int(sys.argv[1]) #this gives the number of grids
N_roots = int(sys.argv[2]) #this gives the number of roots

x = np.linspace(-1,1,N_grid)#initial condition for real part
y = np.linspace(-1,1,N_grid)#initial condition for imaginary part
# array of roots of the polynomial
a = roots(N_roots,0.01)
# coloring all initial points in terms of their roots
color = main_algorithm(x,y,a)

#plot the fractal
plt.imshow(color, cmap='winter', interpolation='nearest',alpha=1)
plt.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False) 

plt.show()  
