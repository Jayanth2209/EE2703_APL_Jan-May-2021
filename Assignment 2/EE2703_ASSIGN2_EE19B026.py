from sys import argv, exit
import numpy as np
import cmath
import math
from tabulate import tabulate
import pandas as pd

CIRCUIT = '.circuit'
END = '.end'
ac = False

"""
To check whether the user has given required and only the required inputs
Otherwise, show them the expected usage
"""
if len(argv) < 2:
    print('ERROR: Please enter the name of Input Netlist file\nExpected Usage: python3 <Assignment_1_EE19B026.py> <Input Netlist file>')
    #print('Expected Usage: python3 <Assignment_1_EE19B026.py> <Input Netlist file>')
    exit()
elif len(argv) > 2:
    print('ERROR: Arguments exceeded\nExpected Usage: python3 <Assignment_1_EE19B026.py> <Input Netlist file>')
    exit()

arg1 = argv[1]
if ('.' in arg1)==True:
    file_name = arg1.split('.')
    if file_name[1]!= 'netlist':
    	print('ERROR: Please check the format of the Input file\nInput file has to be a .netlist file')
    	exit()
else:
    print('ERROR: Invalid Input file\nInput file has to be a .netlist file')
    exit()

"""
Reading from the Input Netlist file and obtaining required indices
"""
try:
    with open(argv[1]) as f:
        lines = f.readlines()
        #print(lines)
        global start
        global end
        start = -1; end = -2
        for line in lines:              # Extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)       # start index
                #print(start)
            elif END == line[:len(END)]:
                end = lines.index(line)         # end index
                #print(end)
                break
        if start >= end:                # Validating circuit block
            print('Invalid circuit definition')
            exit(0)

        """print('\nReverse Order:\n')
        for line in reversed([' '.join(reversed(line.split('#')[0].split())) for line in lines[start+1:end]]):
            print(line)"""                # Print the reversed order
        # Storing tokens
        lines_new = []
        for line in lines[start+1:end]:
            lines_new.append(line.split('#')[0].split())
        f.close()
    #print(lines_new)

except IOError:
    print('ERROR: Invalid Input file\nPlease enter a valid .netlist file located in the same directory/folder')
    exit()

temp = []
for line in lines:
    temp.append(line.split('#')[0].split())
#print(temp)
for i in range(len(temp)):
    if temp[i][0] == '.ac':
        lines_new.append(temp[i])
        ac = True
        f = float(temp[i][2])
#print(lines_new)
#print(ac)
#print(f)

lines2 = []
for i in range(len(lines_new)):
    if (lines_new[i][0] == '.ac'):
        pass
    else:
        lines2.append(lines_new[i])
#print(lines2)

nodes = []
for i in range(len(lines2)):		# Adding all unique nodes to the list 'nodes'
	if (lines2[i][1] not in nodes):
		nodes.append(lines2[i][1])
	if (lines_new[i][2] not in nodes):
		nodes.append(lines2[i][2])
#print(nodes)

node_dict = {}
e=1

for i in nodes:		# d is a dictionary with keys as all unique nodes and values as integers
	if i=='GND':
		node_dict['GND']=0	# value is always zero for key 'GND'
	else:
		node_dict[str(i)] = e # values for remaining nodes are ascending integers
		e=e+1
#print(node_dict)

class Components:		# Class of all components
	def __init__(self, name, n1, n2, value): # Attributes: name, fromnode, tonode, value;
		self.name = name
		self.n1 = n1
		self.n2 = n2
		self.value = value

k = 0    #number of voltage sources
Vs = []  #list of voltage sources
Is = []  #list of current sources
### CREATING OBJECTS FOR EACH COMPONENT in the class 'Comp1' defined above
for i in range (len(lines2)):
    if i == 0:
        if len(lines2[i]) == 4:
            c = np.array([Components(lines2[i][0], node_dict[lines2[i][1]], node_dict[lines2[i][2]], float(lines2[i][3]))])
        elif len(lines2[i])==6:
            c = np.array([Components(lines2[i][0], node_dict[lines2[i][1]], node_dict[lines2[i][2]], cmath.rect(float(lines2[i][4])/2,float(lines2[i][5])))])
        elif len(lines2[i])==5:
            c = np.array([Components(lines2[i][0], node_dict[lines2[i][1]], node_dict[lines2[i][2]], float(lines2[i][4]))])
    else:
        if len(lines2[i]) == 4:
            a1,a2,a3,a4 = tuple(lines2[i])
            c = np.append(c,[Components(a1,node_dict[a2],node_dict[a3],float(a4))],axis = 0)
        elif len(lines2[i])==6:
            c = np.append(c,[Components(lines2[i][0], node_dict[lines2[i][1]], node_dict[lines2[i][2]], cmath.rect(float(lines2[i][4])/2,float(lines2[i][5])))],axis = 0)
        elif len(lines2[i])==5:
            c = np.append(c,[Components(lines2[i][0], node_dict[lines2[i][1]], node_dict[lines2[i][2]], float(lines2[i][4]))],axis = 0)

    if lines2[i][0][0]=='V':
        Vs.append(lines2[i][0])	#list of voltage sources
        k+=1						# Number of independent sources
    if lines2[i][0][0]=='I':
        Is.append(lines2[i][0])	#list of current sources
        k+=1

#print(Vs)
#print(Is)

n = len(node_dict)-1

if ac==True:		# Inializing M matrix for AC system
	m = np.zeros((n+k,n+k), dtype=complex)
	b = np.zeros((n+k,1), dtype=complex)
	w = 2*3.1415926535*f
else:				# Inializing M matrix for AC system
	m = np.zeros((n+k,n+k))
	b = np.zeros((n+k,1))
#print(m)
#print(b)

for i in range(len(c)):
    # X = 1/Impedance of each component (R,L and C)
    if (c[i].name[0]=='R'):
        X = 1/(c[i].value)
        # For Resistors, Impedance = Resistance
    elif (c[i].name[0]=='L' and ac == True):
        X = complex(0,-1/(w*(c[i].value)))
        # For Inductors, Impedance = j*w*L
    elif (c[i].name[0]=='C' and ac == True):
        X = complex(0,w*c[i].value)
        # For capacitors, Impedance = 1/(j*w*C)
    if c[i].name[0] == 'R' or c[i].name[0] == 'L' or c[i].name[0] == 'C':
        if c[i].n1 == 0:
            m[c[i].n2-1,c[i].n2-1] += X     # If node n1 is GND
        elif c[i].n2 == 0:
            m[c[i].n1-1,c[i].n1-1] += X     # If node n2 is GND
        else:
            m[c[i].n1-1,c[i].n1-1] += X
            m[c[i].n1-1,c[i].n2-1] += -X
            m[c[i].n2-1,c[i].n1-1] += -X
            m[c[i].n2-1,c[i].n2-1] += X

    #Changing the M and b matrices accordingly for independent VOLTAGE source
    if c[i].name[0]=='V':
        # If node n1 is GND
        if c[i].n1 == 0:
            m[n,c[i].n2-1] += 1
            b[n] += c[i].value
            m[c[i].n2-1,n] += -1
        # If node n2 is GND
        elif c[i].n2 == 0:
            m[n,c[i].n1-1] += -1
            b[n] += c[i].value
            m[c[i].n1-1,n] += 1
        else:
            m[n,c[i].n2-1] += 1
            m[n,c[i].n1-1] += -1
            b[n] += c[i].value
            m[c[i].n2-1,n] += -1
            m[c[i].n1-1,n] += 1
    #if c[i].name[0]=='V':
        n = n+1

        #Changing the M and b matrices accordingly for independent CURRENT source
    if c[i].name[0]=='I':
        # If node n1 is GND
        if c[i].n1 == 0:
            m[n,n] += -1
            b[n] += c[i].value
            m[c[i].n2-1,n] += 1
        # If node n2 is GND
        elif c[i].n2 == 0:
            m[n,n] += -1
            b[n] += c[i].value
            m[c[i].n1-1,n] += -1
        else:
            m[n,n] += -1
            b[n] += c[i].value
            m[c[i].n2-1,n] += 1
            m[c[i].n1-1,n] += -1
    #if c[i].name[0]=='I':
        n = n+1
#print(n)
#print(m)
#print(b)
#print(k)
try:
	x = np.linalg.solve(m, b)	#Solving Mx=b for x matrix
except np.linalg.LinAlgError:	#Checking that the determinent of M is non zero, so that we don't get an inconsistent solution.
	print('Singular Matrix! Verify the circuit/netlist file')
	exit()
nodes.remove('GND')
#print(x)

#Printing out the results
choice = input("NOTE: For tabulated results, <tabulate> library using the command <pip3 install tabulate> must be installed, before running the code\nIf you want tabulated result, Enter Y\nIf you want untabulated results, Enter N: ")
print('\n')

if choice == 'N':
    nodevols1 = []
    currentvol1 = []
    for i in range(len(nodes)):
        if cmath.polar(x[i][0])[0] < 1e-5 and cmath.polar(x[i][0])[1] > 1e-5:
            nodevols1.append([str(nodes[i]), ('0', str(round(cmath.polar(x[i][0])[1], 5)))])
        elif cmath.polar(x[i][0])[0] > 1e-5 and cmath.polar(x[i][0])[1] < 1e-5:
            nodevols1.append([str(nodes[i]), (str(round(cmath.polar(x[i][0])[0], 5)), '0')])
        elif cmath.polar(x[i][0])[0] < 1e-5 and cmath.polar(x[i][0])[1] < 1e-5:
            nodevols1.append([str(nodes[i]), str('0', '0')])
        else:
            nodevols1.append([str(nodes[i]), (str(round(cmath.polar(x[i][0])[0], 5)), str(round(cmath.polar(x[i][0])[1], 5)))])
    #print(nodevols1)
    for i in range(len(nodevols1)):
        if ac == True:
            print(f'Voltage at {nodevols1[i][0]} is {nodevols1[i][1][0]}sin(wt + {nodevols1[i][1][1]}) V\n')
        else:
            print(f'Voltage at {nodevols1[i][0]} is {float(nodevols1[i][1][0])*round(math.cos(float(nodevols1[i][1][1])))} V\n')
    for i in range(len(Vs)):
        if cmath.polar(x[n-k+i][0])[0] < 1e-5 and cmath.polar(x[n-k+i][0])[1] > 1e-5:
            currentvol1.append([str(Vs[i]), ('0', str(round(cmath.polar(x[n-k+i][0])[1], 5)))])
        elif cmath.polar(x[n-k+i][0])[0] > 1e-5 and cmath.polar(x[n-k+i][0])[1] < 1e-5:
            currentvol1.append([str(Vs[i]), (str(round(cmath.polar(x[n-k+i][0])[0], 5)),'0')])
        elif cmath.polar(x[n-k+i][0])[0] < 1e-5 and cmath.polar(x[n-k+i][0])[1] < 1e-5:
            currentvol1.append([str(Vs[i]), ('0', '0')])
        else:
            currentvol1.append([str(Vs[i]), (str(round(cmath.polar(x[n-k+i][0])[0], 5)), str(round(cmath.polar(x[n-k+i][0])[1], 5)))])
    #print(currentvol1)
    for i in range(len(currentvol1)):
        if ac==True:
            print(f'Current through Voltage source {currentvol1[i][0]} is {currentvol1[i][1][0]}sin(wt + {currentvol1[i][1][1]}) A\n')
        else:
            print(f'Current through Voltage source {currentvol1[i][0]} is {float(currentvol1[i][1][0])*round(math.cos(float(currentvol1[i][1][1])))} A\n')
    #print(tabulate(currentvol, headers=['Voltage Source', 'Current through it']))
    if ac==True:
        print(f'Frequency of the system is {f} Hz (or) {w} rad/s')
        print('Voltages and currents are in the form Asin(wt + phase): A = Amplitude, w = frequency in rad/s')

elif choice == 'Y':
    nodevols = []
    currentvol = []
    for i in range(len(nodes)):
        if cmath.polar(x[i][0])[0] < 1e-5 and cmath.polar(x[i][0])[1] > 1e-5:
            nodevols.append([str(nodes[i]), ('0', str(round(cmath.polar(x[i][0])[1], 5)))])
        elif cmath.polar(x[i][0])[0] > 1e-5 and cmath.polar(x[i][0])[1] < 1e-5:
            nodevols.append([str(nodes[i]), (str(round(cmath.polar(x[i][0])[0], 5)), '0')])
        elif cmath.polar(x[i][0])[0] < 1e-5 and cmath.polar(x[i][0])[1] < 1e-5:
            nodevols.append([str(nodes[i]), str('0', '0')])
        else:
            nodevols.append([str(nodes[i]), (str(round(cmath.polar(x[i][0])[0], 5)), str(round(cmath.polar(x[i][0])[1], 5)))])
    if ac == True:
        for i in range(len(nodevols)):
            nodevols[i].append(str(f'{round(float(nodevols[i][1][0])*(math.cos(float(nodevols[i][1][1]))), 5)} + j{round(float(nodevols[i][1][0])*(math.sin(float(nodevols[i][1][1]))), 5)}'))
    else:
        for i in range(len(nodevols)):
            nodevols[i].append(str(float(nodevols[i][1][0])*round(math.cos(float(nodevols[i][1][1])))))
    #print(nodevols)
    print(tabulate(nodevols, headers=['Node', 'Voltage (Polar form) (V)', 'Voltage (V)']))
    print('\n')
    print('Format: Voltage (Polar form): (Amplitude, Phase), in units of Volts\n')
    for i in range(len(Vs)):
        if cmath.polar(x[n-k+i][0])[0] < 1e-5 and cmath.polar(x[n-k+i][0])[1] > 1e-5:
            currentvol.append([str(Vs[i]), ('0', str(round(cmath.polar(x[n-k+i][0])[1], 5)))])
        elif cmath.polar(x[n-k+i][0])[0] > 1e-5 and cmath.polar(x[n-k+i][0])[1] < 1e-5:
            currentvol.append([str(Vs[i]), (str(round(cmath.polar(x[n-k+i][0])[0], 5)),'0')])
        elif cmath.polar(x[n-k+i][0])[0] < 1e-5 and cmath.polar(x[n-k+i][0])[1] < 1e-5:
            currentvol.append([str(Vs[i]), ('0', '0')])
        else:
            currentvol.append([str(Vs[i]), (str(round(cmath.polar(x[n-k+i][0])[0], 5)), str(round(cmath.polar(x[n-k+i][0])[1], 5)))])
    if ac == True:
        for i in range(len(currentvol)):
            currentvol[i].append(str(f'{round(float(currentvol[i][1][0])*(math.cos(float(currentvol[i][1][1]))), 5)} + j{round(float(currentvol[i][1][0])*(math.sin(float(currentvol[i][1][1]))), 5)}'))
    else:
        for i in range(len(currentvol)):
            currentvol[i].append(str(float(currentvol[i][1][0])*round(math.cos(float(currentvol[i][1][1])))))
    #print(currentvol)
    print(tabulate(currentvol, headers=['Voltage Source', 'Current through it (Polar form) (A)', 'Current (A)']))
    print('\n')
    print('Format: Current (Polar form): (Amplitude, Phase), in units of Amperes\n')
    if ac==True:
        print(f'Frequency of the system is {f} Hz\nOmega (w) = {w} rad/s')
