import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate
np.warnings.filterwarnings('ignore')
# Defining the functions we will fit using Fourier series
def coscos(x):
	return np.cos(np.cos(x))

x_axis = np.linspace(-2*np.pi,4*np.pi, 10000)

def func(n):
    if n==0:
        return np.exp,'exp(x)'
    elif n==1:
        return coscos,'cos(cos(x))'

for n in range(0,2):
	#Plotting the functions against x
	plt.plot(x_axis,func(n)[0](x_axis),'r')
	plt.title(f'{func(n)[1]} vs x')
	plt.grid()
	plt.xlabel('x    $\longrightarrow$')
	plt.ylabel(f'{func(n)[1]}    $\longrightarrow$')
	plt.show()
	#Plotting the functions against x in semilog-Y scale(for exp(x))
	plt.semilogy(x_axis,func(n)[0](x_axis))
	plt.title(f'{func(n)[1]} vs x: Semilogy')
	plt.grid()
	plt.xlabel('x    $\longrightarrow$')
	plt.ylabel(f'{func(n)[1]}    $\longrightarrow$')
	plt.show()

# Periodic extension of exp(x)
plt.plot(x_axis,func(0)[0](x_axis%(2*np.pi)),'m')
plt.title(f'Periodic extenstion of {func(0)[1]} vs x')
plt.grid()
plt.xlabel('x    $\longrightarrow$')
plt.ylabel(f'Expected Fourier {func(0)[1]}    $\longrightarrow$')
plt.show()

# Defining functions f(x)coskx and f(x)sinkx for finding coefficients
def u(x,n,k):
	return np.cos(k*x)*func(n)[0](x)
def v(x,n,k):
	return np.sin(k*x)*func(n)[0](x)

for n in range(0,2):
	# Getting a0:
	coeff = [integrate.quad(func(n)[0],0,2*np.pi)[0] / (2*np.pi)]
	# Getting ak and bk:
	for k in range(1,26):
		coeff.append(integrate.quad(u,0,2*np.pi,args=(n,k))[0] / np.pi)
		#print(integrate.quad(u,0,2*np.pi,args=(n,k)))
		coeff.append(integrate.quad(v,0,2*np.pi,args=(n,k))[0] / np.pi)
	#Plotting the magnitude of fourier coefficients vs n:
	plt.plot(0,coeff[0],'bo',label='a\N{SUBSCRIPT ZERO}')
	plt.plot(np.arange(1,26,1),np.abs(coeff[1::2]),'ro',label='a')
	plt.plot(np.arange(1,26,1),np.abs(coeff[2::2]),'yo',label='b')
	plt.title(f'{func(n)[1]}: Magnitude of Fourier coefficients vs n')
	plt.xlabel('n    $\longrightarrow$')
	plt.ylabel('Magnitude of Fourier Coefficients   $\longrightarrow$')
	plt.grid()
	plt.legend()
	plt.show()
	#Plotting the coefficients on log scale against 'n'
	plt.semilogy(0,np.abs(coeff[0]),'bo')
	plt.semilogy(np.arange(1,26,1),np.abs(coeff[1::2]),'ro')
	plt.semilogy(np.arange(1,26,1),np.abs(coeff[2::2]),'yo')
	plt.title(f'{func(n)[1]}: Semilogy - Fourier Coefficients vs n')
	plt.xlabel('n    $\longrightarrow$')
	plt.ylabel('log(Fourier coefficients)   $\longrightarrow$')
	plt.grid()
	plt.show()
	#Plotting the coefficients on log scale against 'n', also in log scale
	plt.loglog(0,np.abs(coeff[0]),'bo')
	plt.loglog(np.arange(1,26,1),np.abs(coeff[1::2]),'ro')
	plt.loglog(np.arange(1,26,1),np.abs(coeff[2::2]),'yo')
	plt.title(f'{func(n)[1]}: Loglog Plot')
	plt.xlabel('log(n)    $\longrightarrow$')
	plt.ylabel('log(Fourier coefficients)   $\longrightarrow$')
	plt.grid()
	plt.show()

    # To find the coefficients using Least Squares approach:
	x_vector = np.linspace(0,2*np.pi,401)[:-1] # entries from 0 to 2pi
	# List b contains function values at each x in x_vector
	b = func(n)[0](x_vector)
	#print(b)
	#Forming the A matrix
	A = np.transpose(np.array([1]*400))

	for k in range(1,26):
		A=np.c_[A,np.cos(k*x_vector)]
		A=np.c_[A,np.sin(k*x_vector)]
	#print(A)
	#Solving for matrix c in Ac = b:
	try:
		sol = np.linalg.lstsq(A,b)[0]
	except Exception:
		print("The equation Ac = b couldn't be sovled!")
		exit()

	#print(sol)
	#Plotting the magnitude of coefficients obtained from Least squares approach
	plt.plot(0,sol[0],'bo',label='a\N{SUBSCRIPT ZERO}')
	plt.plot(np.arange(1,26,1),np.abs(sol[1::2]),'ro',label='a')
	plt.plot(np.arange(1,26,1),np.abs(sol[2::2]),'yo',label='b')
	plt.title(f'{func(n)[1]}: Magnitude of coefficients vs n (Least Squares approach)')
	plt.xlabel('n    $\longrightarrow$')
	plt.ylabel('Magnitude of coefficients   $\longrightarrow$')
	plt.grid()
	plt.legend()
	plt.show()
	#Plotting the coefficients obtained from Least squares approach in log scale against n
	plt.semilogy(0,np.abs(coeff[0]),'ro')
	plt.semilogy(np.arange(1,26,1),np.abs(coeff[1::2]),'ro')
	plt.semilogy(np.arange(1,26,1),np.abs(coeff[2::2]),'ro',label='Direct Integration')
	plt.semilogy(0,np.abs(sol[0]),'go')
	plt.semilogy(np.arange(1,26,1),np.abs(sol[1::2]),'go')
	plt.semilogy(np.arange(1,26,1),np.abs(sol[2::2]),'go',label='Least Squares approach')
	plt.title(f'Semilogy: {func(n)[1]} - Coefficients obtained by both methods vs n')
	plt.xlabel('n    $\longrightarrow$')
	plt.ylabel('log(Coefficients)   $\longrightarrow$')
	plt.legend()
	plt.grid()
	plt.show()
	#Plotting the loglog plot of coefficients obtained from Least squares approach against n
	plt.loglog(0,np.abs(coeff[0]),'ro')
	plt.loglog(np.arange(1,26,1),np.abs(coeff[1::2]),'ro')
	plt.loglog(np.arange(1,26,1),np.abs(coeff[2::2]),'ro',label='Direct Integration')
	plt.loglog(0,np.abs(sol[0]),'go')
	plt.loglog(np.arange(1,26,1),np.abs(sol[1::2]),'go')
	plt.loglog(np.arange(1,26,1),np.abs(sol[2::2]),'go',label='Least Squares approach')
	plt.title(f'{func(n)[1]}: log(Coefficients) vs log(n) - Direct Integration and Least Squares approach')
	plt.xlabel('log(n)    $\longrightarrow$')
	plt.ylabel('log(Coefficients)   $\longrightarrow$')
	plt.grid()
	plt.legend()
	plt.show()

	#Calculating the maximum difference in calculating coefficients from both methods
	print(f'For {func(n)[1]}: Largest deviation = {np.amax(np.abs(sol-coeff))}')
	#Plotting absolute difference of coefficients obtained from both methods
	plt.plot(0,np.abs(coeff[0]-sol[0]),'bo',label='a\N{SUBSCRIPT ZERO}')
	plt.plot(np.arange(1,26,1),np.abs(coeff[1::2]-sol[1::2]),'ro',label='a')
	plt.plot(np.arange(1,26,1),np.abs(coeff[2::2]-sol[2::2]),'yo',label='b')
	plt.xlabel('n    $\longrightarrow$')
	plt.ylabel('Deviation    $\longrightarrow$')
	plt.title(f'{func(n)[1]}: Absolute Difference between coefficients obtained by Direct Integration and Least Squares approach vs n')
	plt.grid()
	plt.legend(loc='best')
	plt.show()
	# Computing Ac:
	Ac = np.dot(A,sol)
	#Plotting Function values generated by least-squares as a function of x
	plt.plot(x_vector,Ac,'go',label='Function values from Least Squares approach')
	plt.plot(x_axis,func(n)[0](x_axis),'r',label=f'{func(n)[1]}')
	plt.title(f'{func(n)[1]} alongside Function values obtained through Least Squares approach')
	plt.xlabel('x   $\longrightarrow$')
	plt.ylabel(f'{func(n)[1]}    $\longrightarrow$')
	plt.grid()
	plt.legend(loc='best')
	plt.show()
	#Plotting Function values generated by least-squares approach in log scale with true function against x
	plt.semilogy(x_vector,Ac,'go',label='Function values from Least Squares approach')
	plt.semilogy(x_axis,func(n)[0](x_axis),'r',label=f'{func(n)[1]}')
	plt.title(f'Semilogy: {func(n)[1]} alongside Function values obtained through Least Squares approach')
	plt.xlabel('x   $\longrightarrow$')
	plt.ylabel(f'{func(n)[1]} - log scale    $\longrightarrow$')
	plt.grid()
	plt.legend(loc='best')
	plt.show()
