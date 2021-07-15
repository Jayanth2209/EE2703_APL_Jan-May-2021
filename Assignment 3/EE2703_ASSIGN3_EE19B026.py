from pylab import *
import scipy.special as sp
import scipy
import math
import sys

try:	   # To make sure no error is raised while opening the file
	lines = loadtxt('fitting.dat')			# Reading the lines of file.
except Exception:
	print("ERROR!\nPlease check that the data to be fitted is in a file named <fitting.dat>, and is in the same folder/directory as your code!")
	exit()

lines=list(lines)

sigma=logspace(-1,-3,9)  #standard deviation of noise

n = [[],[],[],[],[],[],[],[],[],[]]

def g(t,A,B):			#defining the function g(t;A,B)
	return (A*sp.jn(2,t)+B*t)

for row in lines:			#Parsing the file and extracting each column into list-n
	for i in range(10):
		if len(row) == 10 :
			n[i].append(float(row[i]))
n=array(n)

for i in range(9):				#Plotting Noisy Data againt time
	plot(n[0],n[i+1], label=f'\u03C3{i+1}={(sigma[i]):.3f}')

plot(n[0],g(n[0],1.05,-0.105),label='True Value',color='k')		#Plotting expected true value
title('Q4: Data to be fitted to theory')
xlabel('t (time)$\longrightarrow$')
ylabel('f(t) + Noise $\longrightarrow$')
legend(loc='upper right')
grid()
show()

#Plotting errorbar of noisy data against time
errorbar(n[0][::5],n[1][::5],sigma[0],fmt='ro',label='Errorbar')
plot(n[0],g(n[0],1.05,-0.105),label='f(t)',color='k')
legend()
title('Q5: Data points for \u03C3=0.10 along with the exact function')
xlabel('t (time)$\longrightarrow$')
grid()
show()

#Defining matrix M
t = array(n[0])
t=t[:, newaxis]
j2_t = sp.jn(2,n[0])
j2_t= j2_t[:, newaxis]
M=c_[j2_t,t]
p = [[1.05],[-0.105]]
#Verifying whether both these are equal
print('Verifying if M.p = g(t,A,B): at A = 1.05 and B = -0.105....')
print(f'Error of M.p with actual function: {average(g(n[0],1.05,-0.105)-dot(M,p))}\n')
#print(average(g(n[0],1.05,-0.105)-dot(M,p)))

A = arange(0, 2.1, 0.1)
B = arange(-0.2, 0.01, 0.01)
epsilon = zeros((len(A),len(B)),dtype=float)

#Generating Error Matrix
for i in range(len(A)):
	for j in range(len(B)):
		for k in range(len(n[0])):
			epsilon[i][j] += (1/101)*((n[1][k]-g(n[0][k],A[i],B[j]))**2)
min_error = amin(epsilon[i][j])
for i in range(len(A)):
	for j in range(len(B)):
		if (epsilon[i][j]==min_error):
			print(f'Minimum error is {epsilon[i][j]} for A = {A[i]} and B = {B[j]}\n')

#Plotting contour plot
c=contour(A,B,epsilon,20)
clabel(c,c.levels[:5],inline=True)
plot(1.05,-0.105,'ro', label='Exact Location')
title('Q8: Contour plot of \u03B5ij')
xlabel('A $\longrightarrow$')
ylabel('B $\longrightarrow$')
legend()
show()


h=[]
A_error = []
B_error = []
try: #Solving for best estimate
	for i in range(9):
		h.append(scipy.linalg.lstsq(M,n[i+1])[0])
except Exception:
	print("The equation M.p = data couldn't be sovled!")
	exit()

print("Solutions for different sigma:")
print(h)

for i in range(9):		#Calculating error in A and B
	A_error.append(abs((h[i][0]-1.05)))
	B_error.append(abs((h[i][1]+0.105)))

#Plotting Aerr and Berr againt noise standard deviation
plot(sigma,A_error,'--r',label = 'Aerr',marker="o")
plot(sigma,B_error,'--g',label = 'Berr',marker="o")
title('Q10: Variation of error with noise')
xlabel('Noise Standard Deviation $\longrightarrow$')
ylabel('Mean Squared Error $\longrightarrow$')
grid()
legend()
show()

#Plotting Aerr and Berr againt sigma in log scale for both axes
errorbar(sigma,A_error,A_error,fmt='ro',label='Aerr')
errorbar(sigma,B_error,B_error,fmt='go',label='Berr')
xscale('log')
yscale('log')
title('Q11: Variation of error with noise')
ylabel('Mean Squared Error $\longrightarrow$')
xlabel('\u03C3n $\longrightarrow$')
grid()
legend(loc='upper right')
show()
