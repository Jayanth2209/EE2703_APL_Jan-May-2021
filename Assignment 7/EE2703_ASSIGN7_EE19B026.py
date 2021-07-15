from sympy import *
import pylab as p
import scipy.signal as sp
import numpy as np

s = symbols('s')

PI = np.pi 
# Defining Time scale
t = np.arange(0,0.01,1e-8)
# Defining Input Voltage Vi
Vi = (np.sin(2e3*np.pi*t)+np.cos(2e6*np.pi*t))*np.heaviside(t,1)

# Defining a Low Pass Filter
def lowpass(R1,R2,C1,C2,G,Vi):
	s = symbols('s')
	A = Matrix([[0,0,1,-1/G],[-1/(1+s*R2*C2),1,0,0], [0,-G,G,1],[-1/R1-1/R2-s*C1,1/R2,0,s*C1]])
	b = Matrix([0,0,0,-Vi/R1])
	V = A.inv()*b
	return (A,b,V)

# Defining a High Pass Filter
def highpass(R1,R3,C1,C2,G,Vi):
	s = symbols('s')
	A=Matrix([[0,-1,0,1/G],[s*C2*R3/(s*C2*R3+1),0,-1,0],[0,G,-G,1],[-s*C2-1/R1-s*C1,0,s*C2,1/R1]])
	b=Matrix([0,0,0,-Vi*s*C1])
	V=A.inv()*b
	return (A,b,V)

def S2LTI(func):
	num,den = fraction(func)
	num = Poly(num,s)
	den = Poly(den,s)
	num_coeffs = num.all_coeffs()
	den_coeffs = den.all_coeffs()
	num_coeffs = [float(num) for num in num_coeffs]
	den_coeffs = [float(den) for den in den_coeffs]
	return sp.lti(num_coeffs,den_coeffs)

# Impulse Response of the Low-Pass Filter in Frequency Domain
A,b,V = lowpass(10000,10000,1e-9,1e-9,1.586,1) # Vi = 1 - Impusle function in frequency domain
HSLP = V[3]
w = p.logspace(0,8,801) # Omega
ss = 1j*w
hf = lambdify(s,HSLP,'numpy') #Substituting omega values in the function HSLP
v = hf(ss)
p.loglog(w,abs(v),'r',lw=2) #Plotting Impulse response in the frequency domain
p.title("Impulse response of the Low-Pass filter in Frequency Domain")
p.xlabel("Frequency(\u03C9) $\longrightarrow$")
p.ylabel("|H(j\u03C9)| - Low Pass")
p.grid(True)
p.show()

# Step Response of the Low-Pass Filter in Frequency Domain
A,b,V = lowpass(10000,10000,1e-9,1e-9,1.586,1/s) # Vi = 1/s - Step function in frequency domain
SSLP = V[3]
w = p.logspace(0,8,801) # Omega
ss = 1j*w
hf = lambdify(s,SSLP,'numpy') #Substituting omega values in the function SSLP
v = hf(ss)
p.loglog(w,abs(v),'r',lw=2) #Plotting Step response in the frequency domain
p.title("Step response of the Low-Pass filter in Frequency Domain")
p.xlabel("Frequency(\u03C9) $\longrightarrow$")
p.ylabel("|S(j\u03C9)| - Low Pass")
p.grid(True)
p.show()

# Step Response of the Low-Pass Filter in Time Domain
t,Vstep = sp.impulse(S2LTI(SSLP),None,t)
p.plot(t,Vstep,'b')
p.title("Step response of the Low-Pass filter in Time Domain")
p.xlabel("Time (t) $\longrightarrow$")
p.ylabel("s(t) $\longrightarrow$")
p.grid(True)
p.show()

# Determining the Output Voltage Vo(t)
t,Vo,svecLP = sp.lsim(S2LTI(HSLP),Vi,t)
p.plot(t,Vo,'b')
p.title('Output of the Low-Pass Filter V\u2080(t) for Input V\u2081(t) = sin(2000$\pi$t) + cos(2x10\u2076$\pi$t)')
p.xlabel('Time (t) $\longrightarrow$')
p.ylabel('V\u2090(t) $\longrightarrow$')
p.show()

# Impulse Response of High-Pass Filter in Frequency Domain 
A,b,V = highpass(1e4,1e4,1e-9,1e-9,1.586,1) # Vi = 1 - Impusle function in frequency domain
HSHP = V[3]
w = p.logspace(0,8,801) # Omega
ss=1j*w
hf = lambdify(s,HSHP,'numpy') #Substituting omega values in the function HSHP
v=hf(ss)
p.loglog(w,abs(v),'r',lw=2) #Plotting Impulse response in the frequency domain
p.title("Impulse response of the High-Pass filter in Frequency Domain")
p.xlabel("Frequency(\u03C9) $\longrightarrow$")
p.ylabel("|H(j\u03C9)| - High Pass")
p.grid(True)
p.show()

# Step Response of the High-Pass Filter in Frequency Domain
A,b,V = highpass(10000,10000,1e-9,1e-9,1.586,1/s) # Vi = 1/s - Step function in frequency domain
SSHP = V[3]
w = p.logspace(0,8,801) # Omega
ss = 1j*w
hf = lambdify(s,SSHP,'numpy') #Substituting omega values in the function SSLP
v = hf(ss)
p.loglog(w,abs(v),'r',lw=2) #Plotting Step response in the frequency domain
p.title("Step response of the High-Pass filter in Frequency Domain")
p.xlabel("Frequency(\u03C9) $\longrightarrow$")
p.ylabel("|S(j\u03C9)| - High Pass")
p.grid(True)
p.show()

# Step Response of the High-Pass Filter in Time Domain
t,Vstep = sp.impulse(S2LTI(SSHP),None,t)
p.plot(t,Vstep,'b')
p.title("Step response of the High-Pass filter in Time Domain")
p.xlabel("Time (t) $\longrightarrow$")
p.ylabel("s(t) $\longrightarrow$")
p.grid(True)
p.show()

# Determining the Output Voltage Vo(t)
t2 = np.arange(0,5e-6,5e-8)
Vi = (np.sin(2e3*np.pi*t2)+np.cos(2e6*np.pi*t2))*np.heaviside(t2,1)
t2,Vo,svecHP = sp.lsim(S2LTI(HSHP),Vi,t2)
p.plot(t2,Vo,'b')
p.title('Output of the High-Pass Filter V\u2080(t) for Input V\u2081(t) = sin(2000$\pi$t) + cos(2x10\u2076$\pi$t)')
p.xlabel('Time (t) $\longrightarrow$')
p.ylabel('V\u2090(t) $\longrightarrow$')
p.show()

# Question 4  
Vi_LFdamp = (np.sin(2e3*PI*t))*np.exp(-500*t)*np.heaviside(t,1)
#t3 = np.arange(0,1e-3,5e-8)
Vi_HFdamp = (np.sin(2e6*PI*t))*np.exp(-500*t)*np.heaviside(t,1)

# Output for Damped Sinusoid of Low frequency
t,Vo,svecHP = sp.lsim(S2LTI(HSHP),Vi_LFdamp,t)
p.plot(t,Vo,'b')
p.title('Output of the High-Pass Filter V\u2080(t) for Damped Low Frequency Sinusoid Input')
p.xlabel('Time (t) $\longrightarrow$')
p.ylabel('V\u2090(t) $\longrightarrow$')
p.grid(True)
p.show()

# Output for Damped Sinusoid of High frequency
t,Vo,svecHP = sp.lsim(S2LTI(HSHP),Vi_HFdamp,t)
p.plot(t,Vo,'b')
p.title('Output of the High-Pass Filter V\u2080(t) for Damped High Frequency Sinusoid Input')
p.xlabel('Time (t) $\longrightarrow$')
p.ylabel('V\u2090(t) $\longrightarrow$')
p.grid(True)
p.show()

