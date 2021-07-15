import numpy as np
import scipy.signal as sp
from pylab import *
from matplotlib import pyplot as plt

# Question 1:
# Laplace Transform of x(t): X(s) - Damping = 0.5
X = sp.lti(poly1d([1,0.5]),polymul(poly1d([1,1,2.50]),poly1d([1,0,2.25])))
# Inverse laplace Transform of X(s)
t,x = sp.impulse(X,None,linspace(0,50,500))
# Plotting the time response for the spring satisfying x'' + 2.25x = f(t)
plot(t,x,'b')
title("Time Response of a Spring - for Damping constant(\u03B6) = 0.5")
ylabel('x(t) $\longrightarrow$')
xlabel('t $\longrightarrow$')
show()

# Question 2:
# Laplace Transform of x2(t): X2(s) - Damping = 0.05
X2 = sp.lti(poly1d([1,0.05]),polymul(poly1d([1,0.1,2.2525]),poly1d([1,0,2.25])))
# Inverse Laplace Transform of X2(s)
t2,x2 = sp.impulse(X2,None,linspace(0,50,500))
# Plotting
plot(t2,x2,'r')
title("Time Response of a Spring - for Damping constant(\u03B6) = 0.05")
ylabel('x(t) $\longrightarrow$')
xlabel('t $\longrightarrow$')
show()

# Plotting the above graphs in the same plots
plot(t,x,'b',label='\u03B6 = 0.5')
plot(t2,x2,'r',label='\u03B6 = 0.05')
title("Time Responses for Damping constant(\u03B6) = 0.5 and 0.05")
ylabel('x(t) $\longrightarrow$')
xlabel('t $\longrightarrow$')
legend()
show()

# Question 3:
t = linspace(0,50,500)
u = np.cos(1.5*t)*np.exp(-0.05*t)
# Obtaining the Transfer Function H(s) = X(s)/F(s)
H = sp.lti(1,poly1d([1,0,2.25]))
# Defining frequency range
freq = np.arange(1.4,1.65,0.05)
# Defining f(t)
def f(w,t):
    return np.cos(w*t)*np.exp(-0.05*t)*np.heaviside(t,1)
for w in freq:
    u = f(w,t)
    # Obtaining the output x(t)
    t,x3,svec = sp.lsim(H,u,t)
    # For Subplots
    if w == 1.40:
        plt.subplot(5,1,1)
        plt.title(f'Resulting Response for \u03C9 = {w}')
        plt.plot(t,x3)
    if w == 1.45:
        plt.subplot(5,1,2)
        plt.title(f'Resulting Response for \u03C9 = {w}')
        plt.plot(t,x3)
    if w == 1.50:
        plt.subplot(5,1,3)
        plt.title(f'Resulting Response for \u03C9 = {w}')
        plt.plot(t,x3)
    if w == 1.55:
        plt.subplot(5,1,4)
        plt.title(f'Resulting Response for \u03C9 = {w}')
        plt.plot(t,x3)
    if w == 1.60:
        plt.subplot(5,1,5)
        plt.title(f'Resulting Response for \u03C9 = {w}')
        plt.plot(t,x3)
plt.tight_layout()
plt.show()

# For plotting individual plots
for w in freq:
    u = f(w,t)
    t,x3,svec = sp.lsim(H,u,t)
    plot(t,x3)
    title(f'Resulting Response for \u03C9 = {w}')
    ylabel('x(t) $\longrightarrow$')
    xlabel('t $\longrightarrow$')
    show()

# Question 4: Coupled Spring Problem
# For x(t):
X = sp.lti([1,0,3,0,2,0],[1,0,4,0,3,0,0])
# Inverse Laplace Transform
t,x = sp.impulse(X,None,np.linspace(0,20,200))
# For y(t):
Y = sp.lti([2,0],[1,0,3,0,0])
# Inverse Laplace Transform
t,y = sp.impulse(Y,None,np.linspace(0,20,200))
# Plotting
plot(t,x,'b',label = 'x(t)')
plot(t,y,'r',label = 'y(t)')
title('Coupled Spring Problem: x(t) and y(t)')
ylabel('Function $\longrightarrow$')
xlabel('t $\longrightarrow$')
show()

# Question 5:
R = 100
L = 1e-6
C = 1e-6
# Transfer Function:
H2 = sp.lti(1,poly1d([L*C,R*C,1]))
# Obtaining Phase and Magnitude
w,S,phi = H2.bode()
# Plotting Bode Magnitude Plot and Phase Plot
plt.subplot(2,1,1)
plt.semilogx(w,S,'b')
plt.ylabel('|H(j\u03C9)| $\longrightarrow$')
plt.xlabel('\u03C9 $\longrightarrow$')
plt.title('Bode Magnitude and Phase plots of given L-C-R circuit Transfer function')
plt.subplot(2,1,2)
plt.semilogx(w,phi,'b')
plt.ylabel('\u2220(H(j\u03C9)) $\longrightarrow$')
plt.xlabel('\u03C9 $\longrightarrow$')
plt.show()

# Question 6:
# Time Ranges
t1 = np.arange(0,0.01,1e-8) #msec timescale
t2 = linspace(0,30e-6)
# Input Signal
vi = (np.cos(1000*t1) - np.cos(t1*1e6))*heaviside(t1,1)
vi1 = (np.cos(1000*t2) - np.cos(t2*1e6))*heaviside(t2,1)
# Computing Output: vo(t)
t1,vo,svec1 = sp.lsim(H2,vi,t1)
t2,vo1,svec2 = sp.lsim(H2,vi1,t2)
# Plotting
plot(t1,vo,'r')
title('Output Voltage v\u2080(t) vs Time (msec timescale)')
ylabel('v\u2080(t) $\longrightarrow$')
xlabel('t (time) $\longrightarrow$')
show()
plot(t2,vo1,'b')
title('Output Voltage v\u2080(t) vs Time (till 30\u03BCs)')
ylabel('v\u2080(t) $\longrightarrow$')
xlabel('t (time) $\longrightarrow$')
show()
