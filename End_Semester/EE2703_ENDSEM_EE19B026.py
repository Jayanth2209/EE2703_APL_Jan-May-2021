from pylab import *

a = 10  # Radius of the loop is 10 cm
N = 100 # Number of sections in the loop

# QUESTION 2: Breaking the Volume into a 3 by 3 by 1000 Mesh:
x = arange(-1,2,1)
y = arange(-1,2,1)
z = arange(1,1001,1)    # (1cm, 1000cm)
X,Y,Z = meshgrid(x,y,z) # 3 X 3 X 1000 Mesh

r = zeros([3,3,1000,3]) # Points in the Volume
r[:,:,:,0] = X
r[:,:,:,1] = Y
r[:,:,:,2] = Z

# Inititalising Vector Potential A:
Ax = zeros([3,3,1000])
Ay = zeros([3,3,1000])

phi = linspace(0,2*pi,N+1)[:-1] # Angle in Polar coordinates across the loop
r_ = c_[a*cos(phi),a*sin(phi),zeros(N)] # Point on the Loop - (X,Y)

# CURRENT IN THE LOOP:
I = 4*pi*c_[-sin(phi)*cos(phi),cos(phi)**2,zeros(N)]
#I = 4*pi*c_[-sin(phi)*abs(cos(phi)),cos(phi)*abs(cos(phi)),zeros(N)]   # Asymmetric Current Distribution

# QUESTION 3: Plotting the Current elements in X-Y Plane:
figure()
quiver(r_[:,0],r_[:,1],I[:,0],I[:,1],scale=500,color='navy')
xlim([-12,12])
ylim([-12,12])
grid(True)
title('Current in the Wire elements in X-Y Plane')
ylabel('y $\longrightarrow$')
xlabel('x $\longrightarrow$')
legend('Current')
show()

# QUESTION 4: Obtaining the vector dl:
dl = (2*pi*a/N)*c_[-sin(phi),cos(phi),zeros(N)]
dl_x = dl[:,0]
dl_y = dl[:,1]

# QUESTION 5 & 6: Defining the calc() function which returns R and terms in summation of A:
def calc(l):
    R = norm(r-r_[l],axis=-1)
    dAx = cos(phi[l])*exp(-0.1j*R)*dl_x[l]/R
    dAy = cos(phi[l])*exp(-0.1j*R)*dl_y[l]/R
    #dAx = abs(cos(phi[l]))*exp(-0.1j*R)*dl_x[l]/R # For Asymmetric Distribution
    #dAy = abs(cos(phi[l]))*exp(-0.1j*R)*dl_y[l]/R
    #dAx = cos(phi[l])*dl_x[l]/R  # Static in Time 
    #dAy = cos(phi[l])*dl_y[l]/R
    #dAx = abs(cos(phi[l]))*dl_x[l]/R  # Static in Time for Asymmetric Distribution
    #dAy = abs(cos(phi[l]))*dl_y[l]/R
    #dAx = dl_x[l]/R    # Static in Space and Time
    #dAy = dl_y[l]/R
    return R,dAx,dAy

# QUESTION 7: Computing A: 
for l in range(N):
    R,dAx,dAy = calc(l)
    Ax = Ax + dAx
    Ay = Ay + dAy

# QUESTION 8: Computing Magnetic Field B along z-axis:
Bz = (Ay[1,2,:]-Ay[1,0,:] + Ax[0,1,:]-Ax[2,1,:])/4

# QUESTION 9: Log-Log Plot of Magnetic Field B along z-axis:
figure()
loglog()
grid(True)
plot(z,abs(Bz),color='darkblue')
ylabel(r"Magnetic Field - $|B_{z}|$ $\longrightarrow$")
xlabel('$z$ $\longrightarrow$')
title(r"Magnetic Field $B_{z}$ vs $z$ in Log-Log Scale")
legend([r'log|$B_{z}$|'])
show()
# Magnetic Field Bz vs z:
figure()
grid(True)
plot(z,abs(Bz),color='navy')
ylabel(r"Magnetic Field - $B_{z}$ $\longrightarrow$")
xlabel('z $\longrightarrow$')
title(r"Magnetic Field $B_{z}$ vs $z$")
legend([r'|$B_{z}$|'])
show()

# QUESTION 10: Fitting the Field to Bz = cz^b:
b,log_c = lstsq(c_[log(z),ones(1000)],log(abs(Bz)),rcond=None)[0]
print(f"Value of the Decay Factor(b) = {b}\nValue of c = {exp(log_c)}")

# Plotting the Fit alongside the actual plot: 
figure()
loglog()
grid(True)
plot(z,abs(Bz),label=r'Actual value: $log|B_{z}|$',color='darkblue')
plot(z,(exp(log_c)*(z**b)),label='Obtained Best Fit',color='gold')
ylabel(r"Magnetic Field - $|B_{z}|$ $\longrightarrow$")
xlabel('z $\longrightarrow$')
title(r"Magnetic Field $|B_{z}|$ vs $z$ in Log-Log scale alongside Obtained Best Fit")
legend()
show()



