import sys
from pylab import *
import numpy as np

if (len(sys.argv))==1:
    n = 100
    M = 5
    nk = 500
    u0 = 5
    p = 0.25

elif (len(sys.argv))==6:
    try:
        n = int(sys.argv[1])
        M = int(sys.argv[2])
        nk = int(sys.argv[3])
        u0 = float(sys.argv[4])
        p = float(sys.argv[5])
    except Exception:
        print(f'ERROR! Wrong Usage!!\nCorrect usage: python3 {sys.argv[0]} n M nk u0 p')
        print('n = Spatial grid size\nM = Number of electrons injected per turn\nnk = Number of turns to simulate\nu0 = Threshold velocity\np = Probability that Ionization will occur')
        exit()
else:
    print(f'ERROR! Wrong Usage!!\nCorrect usage: python3 {sys.argv[0]} n M nk u0 p')
    print('n = Spatial grid size\nM = Number of electrons injected per turn\nnk = Number of turns to simulate\nu0 = Threshold velocity\np = Probability that Ionization will occur')
    exit()

Msig = 1 # Variance

def Tubelight(n,M,nk,u0,p,Msig):
    xx = np.zeros(n*M)
    u = np.zeros(n*M)
    dx = np.zeros(n*M)
    I = []
    X = []
    V = []
    for turn in range(nk):
        # Injecting Electrons
        m = int(randn()*Msig+M)
        # Add them to free slots
        ee = where(xx==0)[0]
        # Initialize their position to 1
        xx[ee[0:m]] = 1
        # Finding electrons present in the chamber
        ii = where(xx>0)[0]
        # Adding their positions and velocities to X and V
        X.extend(xx[ii].tolist())
        V.extend(u[ii].tolist())
        # Calculate the displacement during this turn
        dx[ii] = u[ii] + 0.5
        # Update Position and Velocity
        xx[ii] += dx[ii]
        u[ii]+=1
        # Determine particles which have hit the anode
        jj = where(xx>=n)[0]
        xx[jj]=0
        u[jj]=0
        dx[jj]=0
        # Electrons with velocity greater than threshold velocity
        kk = where(u>=u0)[0]
        ll = where(rand(len(kk))<=p)[0]
        kl = kk[ll]
        # Reset the velocity of these electrons to zero (inelastic collision)
        u[kl]=0
        # Determining the point of collision
        rho = rand(1)
        xx[kl] -= dx[kl]*rho
        # Emissions
        I.extend(xx[kl].tolist())
        # Finding all the existing electrons again
        #ii = where(xx>0)
    return X,V,I

def Plots(X,V,I):
    # Electron density
    figure()
    hist(X,bins=range(0,n+1),color='r',ec='black')
    title("Electron density")
    xlabel("$x$")
    ylabel("Number of electrons")
    show()
    # Light instensity
    figure()
    ints,bins,trash = hist(I,bins=range(0,n+1),color='yellow',ec='black')
    title("Light Intensity")
    xlabel("$x$")
    ylabel("I")
    show()
    # Electron phase-space
    figure()
    scatter(X,V,marker='x')
    title("Electron Phase Space")
    xlabel("$x$")
    ylabel("$v$")
    show()
    return ints,bins

X,V,I = Tubelight(n,M,nk,u0,p,Msig)
ints, bins = Plots(X,V,I)

# Tabulating Data
xpos = 0.5*(bins[0:-1]+bins[1:])
print("Intensity Data:")
print('xpos',end='    ')
print('count')
for k in range(len(xpos)):
    print(xpos[k],end='     ')
    print(ints[k])
