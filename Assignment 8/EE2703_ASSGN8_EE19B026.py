from pylab import *

# FFT of sin(5x):
x=linspace(0,2*pi,128)
y=sin(5*x) 	# Defining the function
Y=fft(y)    # Finding the Fourier Transform
figure()
subplot(2,1,1)
plot(abs(Y),'r',lw=2)   # Magnitude spectrum
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $\sin(5t)$")
grid(True)
subplot(2,1,2)
plot(unwrap(angle(Y)),'b',lw=2)   # Phase spectrum
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$k$",size=16)
grid(True)
show()

# CORRECTED FFT of sin(5x)
x=linspace(0,2*pi,129);x=x[:-1]
y=sin(5*x)  # Defining the function
Y=fftshift(fft(y))/128.0  # Corrected DFT
w=linspace(-64,63,128)
figure()
subplot(2,1,1)
plot(w,abs(Y),'b',lw=2)   # Magnitude spectrum
xlim([-10,10])
ylabel(r"$|Y|$",size=16)
title(r"Corrected Spectrum of $\sin(5t)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2) # Phase spectrum
ii=where(abs(Y)>1e-3)
plot(w[ii],angle(Y[ii]),'go',lw=2)  # Phase for points with magnitude > 0.001
xlim([-10,10])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
show()

# DFT of (1+0.1cos(t))cos(10t) using 128 points
t=linspace(0,2*pi,129);t=t[:-1]
y=(1+0.1*cos(t))*cos(10*t) # Defining the function
Y=fftshift(fft(y))/128.0   # Finding DFT
w=linspace(-64,63,128)
figure()
subplot(2,1,1)
plot(w,abs(Y),'b',lw=2)  # Magnitude spectrum
xlim([-15,15])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $(1+0.1cos(t))cos(10t)$ with 128points")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)  # Phase spectrum
ii=where(abs(Y)>1e-3)
plot(w[ii],angle(Y[ii]),'go',lw=2)  # Phase spectrum for points with magnitude > 0.001
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
show()

# A function to plot the Spectra
def plotSpectrum(index,N,r,w,xlimit,heading,allphase=True,gauss=False,actgauss=False):
    t = linspace(-r,r,N+1);t=t[:-1]
    if actgauss == False:
        y = func(index,t) # Defining the function
    if gauss == False and actgauss == False:
        Y = fftshift(fft(y))/N   # Finding DFT
    elif gauss == True or actgauss == True:
        y = func(index,t)
        Y = fftshift(abs(fft(y)))/N  # Finding DFT
        Y = Y*sqrt(2*pi)/max(Y)
    w = linspace(-w,w,N+1);w=w[:-1]
    if actgauss == True:
        Y_ = sqrt(2*pi)*exp(-w*w/2)
        print(f'Maximum error in the Computed Spectrum of Gaussian function = {max(abs(abs(Y)-abs(Y_)))}')
    figure()
    subplot(2,1,1)
    if actgauss == False:
        plot(w,abs(Y),'b',lw=2)  # Magnitude spectrum
    elif actgauss == True:
        plot(w,abs(Y_),'b',lw=2)  # Magnitude spectrum
    xlim([-xlimit,xlimit])
    ylabel(r"$|Y|$",size=16)
    title(heading)
    grid(True)
    subplot(2,1,2)
    if allphase == True:
        if actgauss == False:
            plot(w,angle(Y),'ro',lw=2)  # Phase spectrum
            ii = where(abs(Y)>1e-3)
        elif actgauss == True:
            plot(w,angle(Y_),'ro',lw=2)  # Phase spectrum
            ii = where(abs(Y_)>1e-3)
    elif allphase == False:
        ii = where(abs(Y)>1e-3)
    plot(w[ii],angle(Y[ii]),'go',lw=2)  # Phase spectrum for points with magnitude > 0.001
    xlim([-xlimit,xlimit])
    ylabel("Phase of $Y$",size=16)
    xlabel(r"$\omega$",size=16)
    grid(True)
    show()

# The following function returns the required function based on the index passed:
def func(index,t):
    if index == 0:
        return (1+0.1*cos(t))*cos(10*t)
    elif index == 1:
        return sin(t)*sin(t)*sin(t)
    elif index == 2:
        return cos(t)*cos(t)*cos(t)
    elif index == 3:
        return cos(20*t + 5*cos(t))
    elif index == 4:
        return exp(-t*t/2)

plotSpectrum(0,512,4*pi,64,xlimit=15,heading=r"Spectrum of $(1+0.1cos(t))cos(10t)$ with 512points")
plotSpectrum(1,512,4*pi,64,xlimit=15,heading=r"Spectrum of $sin^3(t)$")
plotSpectrum(2,512,4*pi,64,xlimit=15,heading=r"Spectrum of $cos^3(t)$")
plotSpectrum(3,2048,8*pi,128,xlimit=45,heading=r"Spectrum of $cos(20t+5cos(t))$",allphase=False)
plotSpectrum(4,2**9,4*pi,2**5,xlimit=5,heading=r"Spectrum of $e^{-t^2/2}$",gauss=True)
plotSpectrum(4,2**9,8*pi,2**5,xlimit=5,heading=r"Spectrum of $e^{-t^2/2}$",gauss=True)
plotSpectrum(4,2**9,8*pi,2**5,xlimit=5,heading=r"Actual Spectrum of $e^{-t^2/2}$",actgauss=True)
