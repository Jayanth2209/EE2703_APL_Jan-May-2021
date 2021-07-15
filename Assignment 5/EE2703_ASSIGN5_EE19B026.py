import sys
import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

#Default Values
if (len(sys.argv))==1:
	Nx=25   #size along x
	Ny=25	#size along y
	radius=8	#radius of central lead
	Niter=1500	#number of iterations to perform

#Taking values from command line arguements
elif (len(sys.argv))==5:
	try:
		Nx = int(sys.argv[1])	  #size along x
		Ny = int(sys.argv[2])   #size along y
		radius = float(sys.argv[3])   #radius of central lead
		Niter = int(sys.argv[4])	    #number of iterations to perform
	except Exception:
		print(f'ERROR! Wrong Usage!!\nCorrect usage: python3 {sys.argv[0]} Nx Ny radius Niter'/n)
		print('Nx= size along X\nNy= size along Y\nradius = Radius of central lead\nNiter= Number of iterations to perform')
		exit()

else:
	print(f'ERROR! Wrong Usage!!\nCorrect usage: python3 {sys.argv[0]} Nx Ny radius Niter')
	print('Nx= size along X\nNy= size along Y\nradius = Radius of central lead\nNiter= Number of iterations to perform')
	exit()

#Allocating the potential array and initializing it:
phi= np.zeros([Ny,Nx])

#To find central circular region:
x= np.arange(-(Nx-1)/2,(Nx-1)/2+1,1)
y= np.arange((Ny-1)/2,-(Ny-1)/2-1,-1)
Y,X = np.meshgrid(y,x)
#coordinates inside the circle
ii= np.where(X*X +Y*Y <= radius*radius )
phi[ii]=1.0  #Allocating phi for electrode region

#Plotting the contour plot of potential:
plt.contour(np.arange(0,Nx,1),np.arange(0,Ny,1),phi)
plt.title('Contour Plot of potential around electrode and individual 1V-points')
plt.plot(ii[1],ii[0],'o',color='r')
plt.xlim(0,Nx)
plt.ylim(0,Ny)
plt.grid()
plt.xlabel('$\longleftarrow$  Ground  $\longrightarrow$')
plt.show()

#Allocating an error vector:
errors = []

for i in range(Niter):
	#Saving copy of phi
	oldphi = phi.copy()

	#Updating phi array
	phi[1:-1,1:-1] = (phi[2:,1:-1]+phi[:-2,1:-1]+phi[1:-1,2:]+phi[1:-1,:-2])/4

	#Asserting boundaries
	phi[1:-1,0] = phi[1:-1,1]  #left
	phi[1:-1,-1] = phi[1:-1,-2] #right
	phi[0,:] = phi[1,:] #top
	phi[ii]=1.0

	#Appending the maximum error in this iteration
	errors.append((abs(phi-oldphi)).max())

#Plotting errors
plt.plot(np.arange(0,Niter,1),errors[::1])
plt.title('Errors in each Iteration')
plt.xlabel('Iteration number $\longrightarrow$')
plt.ylabel('Error $\longrightarrow$')
plt.grid()
plt.show()

plt.semilogy(np.arange(0,Niter,1),errors[::1], label='All points')
plt.semilogy(np.arange(0,Niter,50),errors[::50],'o',label='50th points')
plt.title('Errors in each Iteration: Semilogy')
plt.xlabel('Iteration number $\longrightarrow$')
plt.ylabel('log(Error) $\longrightarrow$')
plt.legend()
plt.grid()
plt.show()

plt.loglog(np.arange(0,Niter,1),errors[::1])
plt.title('Errors in each Iteration: Loglog Plot')
plt.xlabel('log(Iteration number) $\longrightarrow$')
plt.ylabel('log(Error) $\longrightarrow$')
plt.grid()
plt.show()

#Removing the points where the error goes to zero (log(0) is not finite)
errors_new=[]
Niter_new=0
for error in errors:
	if error != 0:
		errors_new.append(error)
		Niter_new+=1

#Finding best fit for entire vector of errors:
try:
	B1,logA1 = np.polyfit(np.arange(0,Niter_new,1), np.log(errors_new), 1)
except Exception:
	print("ERROR! Couldn't solve the equation for Fit1: Fit for the entire vector of errors")
#Finding best fit for error entries after 500th iteration:
try:
	B2,logA2 = np.polyfit(np.arange(500,Niter_new,1), np.log(errors_new[500:]), 1)
except Exception:
	print("ERROR! Couldn't solve the equation for Fit2: Fit for error entries after 500th iteration")

#Plotting fit1, fit2 and errors
plt.semilogy(np.arange(0,Niter,1),np.abs(errors),'k--',label='Errors')
plt.plot(np.arange(0,Niter,1), np.exp(B1*np.arange(0,Niter,1)+logA1), 'y',label='Fit1')
plt.plot(np.arange(500,Niter,1), np.exp(B2*np.arange(500,Niter,1)+logA2),'r', label='Fit2')
plt.title('Best fits (Fit1, Fit2) and actual Errors in each iteration: Semilogy')
plt.xlabel('Iteration number $\longrightarrow$')
plt.ylabel('log(Error) $\longrightarrow$')
plt.grid()
plt.legend()
plt.show()

#If Nx,Ny are not equal:
if Nx!=Ny:
	Nx=min(Nx,Ny)
	Ny=min(Nx,Ny)
	phi=phi[:min(Nx,Ny),:min(Nx,Ny)]
	x= np.arange(-(Nx-1)/2,(Nx-1)/2+1,1)
	y= np.arange((Ny-1)/2,-(Ny-1)/2-1,-1)
	X,Y = np.meshgrid(x,y)

#Plotting 3-D plot of the potential:
figure = plt.figure(4)
ax = p3.Axes3D(figure)
plt.title('3-D Plot of the Potential')
surf = ax.plot_surface(Y, X, phi.T,rstride=1, cstride=1, cmap='jet',linewidth=0, antialiased=False)
plt.xlabel('$\longleftarrow$ Ground $\longrightarrow$')
plt.ylabel('y $\longrightarrow$')
plt.show()

#Contour plot of potential:
c = plt.contour(np.arange(0,Nx,1),np.arange(0,Ny,1),phi[::-1,:],levels=np.arange(0,1,0.125))
plt.clabel(c,np.arange(0,1,0.25),inline=True)
plt.plot(ii[0],ii[1],'o',color='r',label='Central lead: 1V region')
plt.title('Contour plot of potential')
plt.xlim(0,Nx)
plt.ylim(0,Ny)
plt.legend()
plt.show()
#Plotting 1V electrode points
plt.plot(ii[0],ii[1],'o',color='r',label='Central lead: 1V Region')

#Defining the directions of Current density:
Jy=np.zeros([Ny,Nx])
Jx=np.zeros([Ny,Nx])
Jy[1:-1,1:-1]= (phi[0:-2,1:-1]-phi[2:,1:-1])/2
Jx[1:-1,1:-1]= (phi[1:-1,0:-2]-phi[1:-1,2:])/2

#Vector plot of Current densities:
plt.quiver(np.arange(0,Nx,1),np.arange(0,Ny,1),Jx[::-1,:],-Jy[::-1,:],scale=5,label='Current Density')
plt.title('Vector Plot of Current flow')
plt.legend(loc='upper right')
plt.show()
