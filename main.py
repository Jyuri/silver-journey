import json
import math


#Opening files
with open("input.json", "r") as f:
	input_json = json.load(f)
	sequence = input_json["Sequence"]
	saltConc = input_json["Sodium Concentration"]
	primerConc = input_json["Primer Concentration"]
	f.close()
with open("base_values.json", "r") as f:
	base_values = json.load(f)
	f.close()

#Analyze Sequence Pairs
pairVals = []
for i in range(len(sequence) - 1):
	pairVal = sequence[i] + sequence[i+1]
	try:
		dHi = base_values[pairVal+'-dH']
		dSi = base_values[pairVal+'-dS']
		pairVals.append([pairVal, dHi, dSi])		
	except:
		print(pairVal + " is not recognized")
dH = 0
dS = 0
for i in pairVals:
	dH += i[1]
	dS += i[2]

#Conditions for adding and subtracting special cases
if sequence[0] == "T" or sequence[len(sequence)-1] == "A":
	dH += 0.4
if sequence[0] == "G" or sequence[0] == "C":
	dS += -5.9
else:
	if sequence[len(sequence)-1] == "G" or sequence[len(sequence)-1] == "C":
		dS += -5.9
	else:
		if sequence[0] == "A" or sequence[0] == "T":
			dS += -9.0
		elif sequence[len(sequence)-1] == "A" or sequence[len(sequence)-1] == "T":
			dS += -9.0

#Final Calculations
Ct = primerConc
Tm = ((dH * 1000) / (dS + 1.987 * math.log(Ct/4))) - 273.15
dTm = Tm + 12.5 * math.log(saltConc)

with open("sequenceValues.txt", "w") as f:
		f.write(f"Sequence:\n   {sequence}\n")
		f.write(f"Heat of Enthalpy: {dH}\n")
		f.write(f"Entropy: {dS}\n")
		f.write(f"Tm at 1M Na+: {Tm}\n")
		f.write(f"Tm at {saltConc}M Na+: {dTm}\n")
		f.close()