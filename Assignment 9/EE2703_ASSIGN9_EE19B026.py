from pylab import *
from mpl_toolkits.mplot3d import Axes3D

# Spectrum of sin(√2t):
t=linspace(-pi,pi,65);t=t[:-1]  # Sampling frequency
dt=t[1]-t[0];fmax=1/dt
y=sin(sqrt(2)*t)
y[0]=0                          # The sample corresponding to -tmax should be set zero
y=fftshift(y)                   # Start with y[0]
Y=fftshift(fft(y))/64.0
w=linspace(-pi*fmax,pi*fmax,65);w=w[:-1]
figure()
subplot(2,1,1)
plot(w,abs(Y),'b',lw=2)
xlim([-10,10])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $sin(\sqrt{2}t)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-10,10])
ylabel('\u2220$Y$',size=16)
xlabel('$\u03C9$',size=16)
grid(True)
show()

# Plotting sin(√2t) in Time Domain:
t1=linspace(-pi,pi,65);t1=t1[:-1]
t2=linspace(-3*pi,-pi,65);t2=t2[:-1]
t3=linspace(pi,3*pi,65);t3=t3[:-1]
figure()
plot(t1,sin(sqrt(2)*t1),'b',lw=2)
plot(t2,sin(sqrt(2)*t2),'r',lw=2)
plot(t3,sin(sqrt(2)*t3),'r',lw=2)
ylabel("y",size=16)
xlabel("t",size=16)
title(r"$sin(\sqrt{2}t)$")
grid(True)
show()

# Periodic repetition of sin(√2t) from -pi to +pi:
t1=linspace(-pi,pi,65);t1=t1[:-1]
t2=linspace(-3*pi,-pi,65);t2=t2[:-1]
t3=linspace(pi,3*pi,65);t3=t3[:-1]
y=sin(sqrt(2)*t1)
figure()
plot(t1,y,'bo',lw=2)
plot(t2,y,'ro',lw=2)
plot(t3,y,'ro',lw=2)
ylabel(r"$y$",size=16)
xlabel(r"$t$",size=16)
title(r"$sin(\sqrt{2}t)$ with $t$ wrapping every 2$\pi$ ")
grid(True)
show()

# Spectrum of a digital ramp:
t=linspace(-pi,pi,65);t=t[:-1]
dt=t[1]-t[0];fmax=1/dt
y=t
y[0]=0 # The sample corresponding to -tmax should be set zero
y=fftshift(y) # Start with y(0)
Y=fftshift(fft(y))/64.0
w=linspace(-pi*fmax,pi*fmax,65);w=w[:-1]
figure()
semilogx(abs(w),20*log10(abs(Y)),lw=2)
xlim([1,10])
ylim([-20,0])
xticks([1,2,5,10],["1","2","5","10"],size=16)
ylabel("|Y| (dB)",size=16)
title("Spectrum of a Digital Ramp")
xlabel("$\u03C9$",size=16)
grid(True)
show()

# sin(√2t) with Hamming window in Time domain:
t1=linspace(-pi,pi,65);t1=t1[:-1]
t2=linspace(-3*pi,-pi,65);t2=t2[:-1]
t3=linspace(pi,3*pi,65);t3=t3[:-1]
n=arange(64)
wnd=fftshift(0.54+0.46*cos(2*pi*n/63))
y=sin(sqrt(2)*t1)*wnd
figure()
plot(t1,y,'bo',lw=2)
plot(t2,y,'ro',lw=2)
plot(t3,y,'ro',lw=2)
ylabel(r"$y$",size=16)
xlabel(r"$t$",size=16)
title(r"$\sin(\sqrt{2}t)\times w(t)$ with $t$ wrapping every 2$\pi$ ")
grid(True)
show()


# Function for Plotting Spectra with/without Hamming Window:
def HammingWin(index,k,N,xlimit,heading,Hamming=True,EST=False):
    t = linspace(-k*pi,k*pi,N+1);t=t[:-1]
    dt=t[1]-t[0];fmax=1/dt
    if Hamming == True:
        n=arange(N)
        wnd=fftshift(0.54+0.46*cos(2*pi*n/(N-1)))
        y=func(index,t,N)*wnd
    elif Hamming == False:
        y=func(index,t,N)
    y[0]=0
    y=fftshift(y)
    Y=fftshift(fft(y))/N
    w=linspace(-pi*fmax,pi*fmax,N+1);w=w[:-1]
    figure()
    subplot(2,1,1)
    plot(w,abs(Y),'b',w,abs(Y),'bo',lw=2)
    xlim([-xlimit,xlimit])
    ylabel(r"$|Y|$",size=16)
    title(heading)
    grid(True)
    subplot(2,1,2)
    plot(w,angle(Y),'ro',lw=2)
    xlim([-xlimit,xlimit])
    ylim([-4,4])
    ylabel(r"Phase of $Y$",size=16)
    xlabel(r"$\omega$",size=16)
    grid(True)
    show()
    if EST==True:
        p=1.6
        phase = angle(Y[::-1][argmax(abs(Y[::-1]))])
        w0 = sum(abs(Y**p*w))/sum(abs(Y)**p)
        print(f'Estimated value of frequency, with noise : {w0}')
        print(f'Estimated value of phase, with noise : {phase}')

def func(index,t,N):
    if index == 0:
        return sin(sqrt(2)*t)
    elif index == 1:
        return (cos(0.86*t))**3
    elif index == 2:
        return cos(omega*t+delta)
    elif index == 3:
        return cos(omega*t+delta) + 0.1*randn(N)
    elif index == 4:
        return cos(16*(1.5+t/(2*pi))*t)

HammingWin(0,1,64,8,heading=r"Spectrum of $\sin(\sqrt{2}t)\times w(t)$ with 64 Points")
HammingWin(0,4,256,4,heading=r"Spectrum of $\sin(\sqrt{2}t)\times w(t)$ with 256 Points")
HammingWin(1,4,256,5,heading=r"Spectrum of $\cos^3(0.86t)$ without Hamming Window",Hamming=False)
HammingWin(1,4,256,5,heading=r"Spectrum of $\cos^3(0.86t)$ with Hamming Window")

# QUESTION 3: Estimating Omega and Delta:
omega=0.8
delta=pi
HammingWin(2,1,128,4,heading=r"Spectrum of cos($\omega$t+$\delta$) with Hamming Window",EST=True)

# QUESTION 4: Estimation with added Noise:
HammingWin(3,1,128,4,heading=r"Spectrum of Noisy cos($\omega$t+$\delta$) with Hamming Window",EST=True)

# QUESTION 5: DFT of Chirped Signal:
HammingWin(4,1,1024,50,heading=r"Spectrum of Chirped Signal without Hamming window",Hamming=False)
HammingWin(4,1,1024,50,heading=r"Spectrum of Chirped Signal with Hamming window")

# QUESTION 6: Surface Plot - Chirped Signal:
## Without Hamming Window:
t=linspace(-1*pi,1*pi,1025);t=t[:-1]
dt=t[1]-t[0];fmax=1/dt
y=cos(16*(1.5+t/(2*pi))*t)
y_=np.zeros((16,64),dtype=complex)
for i in range(16):
	y_[i]=fftshift(fft(fftshift(y[64*i:64*(i+1)])))
w=linspace(-pi*fmax,pi*fmax,1025);w=w[:-1]
n=arange(64)
t1 = np.array(range(16))
t1,n = meshgrid (t1,n)
ax=Axes3D(figure())
surf = ax.plot_surface(t1,n,abs(y_).T,rstride =1,cstride=1,cmap='inferno')
ylabel('\u03C9')
xlabel('t')
title("Surface Plot: Variation of frequency with time - Chirped Signal without Hamming Window")
ax.set_zlabel('|Y|')
show()

## With Hamming Window:
t=linspace(-1*pi,1*pi,1025);t=t[:-1]
dt=t[1]-t[0];fmax=1/dt
n0=arange(1024)
wnd=fftshift(0.54+0.46*cos(2*pi*n0/(1023)))
y=cos(16*(1.5+t/(2*pi))*t)*wnd
y_=np.zeros((16,64),dtype=complex)
for i in range(16):
	y_[i]=fftshift(fft(fftshift(y[64*i:64*(i+1)])))
w=linspace(-pi*fmax,pi*fmax,1025);w=w[:-1]
n=arange(64)
t1 = np.array(range(16))
t1,n = meshgrid (t1,n)
ax=Axes3D(figure())
surf = ax.plot_surface(t1,n,abs(y_).T,rstride =1,cstride=1,cmap='inferno')
ylabel('\u03C9')
xlabel('t')
title("Surface Plot: Variation of frequency with time - Chirped Signal with Hamming Window")
ax.set_zlabel('|Y|')
show()
