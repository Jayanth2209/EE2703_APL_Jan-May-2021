from sys import argv, exit

CIRCUIT = '.circuit'
END = '.end'

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

        print('\nReverse Order:\n')
        for line in reversed([' '.join(reversed(line.split('#')[0].split())) for line in lines[start+1:end]]):
            print(line)                 # Print the reversed order
        # Storing tokens
        lines_new = []
        for line in lines[start+1:end]:
            lines_new.append(line.split('#')[0].split())
        f.close()
    #print(lines_new)

except IOError:
    print('ERROR: Invalid Input file\nPlease enter a valid .netlist file located in the same directory/folder')
    exit()

# Using stored tokens for Circuit Analysis
print('\nCircuit Analysis:\n')
for i in range(len(lines_new)):
	if lines_new[i][0][0] == 'V':
		print(f'Independent Voltage source: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nValue = {lines_new[i][3]}V\n')
	elif lines_new[i][0][0] == 'I':
		print(f'Independent Current source: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nValue = {lines_new[i][3]}A\n')
	elif lines_new[i][0][0] == 'R':
		print(f'Resistor: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nValue = {lines_new[i][3]} Ohm\n')
	elif lines_new[i][0][0] == 'L':
		print(f'Inductor: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nValue = {lines_new[i][3]} H\n')
	elif lines_new[i][0][0] == 'C':
		print(f'Capacitor: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nValue = {lines_new[i][3]} F\n')
	elif lines_new[i][0][0] == 'E':
		print(f'Voltage Controlled Voltage source: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nDependent Voltage: Voltage difference between Node {lines_new[i][3]} and Node {lines_new[i][4]}\nValue = {lines_new[i][5]}\n')
	elif lines_new[i][0][0] == 'G':
		print(f'Voltage Controlled Current source: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nDependent Voltage: Voltage difference between Node {lines_new[i][3]} and Node {lines_new[i][4]}\nValue = {lines_new[i][5]}\n')
	elif lines_new[i][0][0] == 'H':
		print(f'Current Controlled Voltage source: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nControlling Current: Current through Voltage source {lines_new[i][3]}\nValue = {lines_new[i][4]}\n')
	elif lines_new[i][0][0] == 'F':
		print(f'Current Controlled Current source: {lines_new[i][0]}\nBetween Node {lines_new[i][1]} and Node {lines_new[i][2]}\nControlling Current: Current through Voltage source {lines_new[i][3]}\nValue = {lines_new[i][4]}\n')
