import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np

genomes = []
with open("modsout.txt", "r") as genomeData:
	for line in genomeData:
		genomes.append(line.strip())

tasks = []
with open("tasks_sex_std.dat", "r") as taskData:
	for line in taskData:
		tasks.append(line.strip().split()[1:])

start = None
end = None
startsEnds = []
curStartsEnds = []
with open("modslog.txt", "r") as modsData:
	for line in modsData:
		if line.strip() == "-":
			startsEnds.append(curStartsEnds)
			curStartsEnds = []
			continue

		if start == None:
			start = int(line.strip())
			continue

		if end == None:
			end = int(line.strip())
			curStartsEnds.append((start, end))
			start = None
			end = None
			continue

PMAvgArr = []
FMAvgArr = []
for seArr in startsEnds:
	PMSum = 0.0
	numPM = 0
	PMArr = []

	FMSum = 0.0
	numFM = 0
	FMArr = []
	for se in seArr:
		activeG = genomes[se[0]:se[1]]
		activeGMain = activeG[0]
		activeGComp = activeG[1:]

		activeT = tasks[se[0]:se[1]]
		activeTMain = activeT[0]
		activeTComp = list(map(lambda j: (j-1, set(filter(lambda i: int(activeT[j][i]) != 0, range(0, len(activeT[j]))))), range(1, len(activeT))))

		# for atc in activeTComp:
		# 	print(atc)

		executable = set(filter(lambda i: int(activeTMain[i]) != 0, range(0, len(activeTMain))))
		nT = len(list(executable))
		L = len(activeGMain)
		PM_numer = 0.0
		for exe in executable:
			necessaries = list(filter(lambda t: exe not in t[1], activeTComp))
			necessaries = [n[0] for n in necessaries]
			
			for n1 in necessaries:
				for n2 in necessaries:
					if n1 > n2:
						PM_numer += (abs(float(n1 - n2))/(len(necessaries)*(len(necessaries) - 1)))

		PM = 1 - 2*(PM_numer/(L*nT)) if nT else 0.0
		if PM != 0.0:
			numPM += 1
			PMArr.append(PM)
		PMSum += PM

		FM_numer = 0.0
		if nT >= 2:
			for exe1 in executable:
				for exe2 in executable:
					if exe1 != exe2:
						nec1 = list(filter(lambda t: exe1 not in t[1], activeTComp))
						nec1 = [n[0] for n in nec1]
						nec2 = list(filter(lambda t: exe2 not in t[1], activeTComp))
						nec2 = [n[0] for n in nec2]

						for n in nec1:
							if n not in nec2:
								FM_numer += 1.0

			FM = FM_numer/(L*nT*(nT - 1))
			numFM += 1
			FMArr.append(FM)
			FMSum += FM

	# PMArr = [pma/numPM for pma in PMArr]
	PMAvgArr.append((sum(PMArr)/numPM, max(PMArr), min(PMArr)))
	print("PM Info: " + str((sum(PMArr)/numPM, max(PMArr), min(PMArr))))

	FMAvgArr.append((sum(FMArr)/numFM, max(FMArr), min(FMArr)))
	print("FM Info: " + str((sum(FMArr)/numFM, max(FMArr), min(FMArr))))

toPlotMain = [pmaa[0] for pmaa in PMAvgArr]
toPlotUpper = [pmaa[1] for pmaa in PMAvgArr]
toPlotLower = [pmaa[2] for pmaa in PMAvgArr]

plt.plot([i*5000 for i in range(1, 20)], toPlotMain, color=(1, 0, 0, 1))
plt.plot([i*5000 for i in range(1, 20)], toPlotUpper, color=(1, 0, 0, 0.25))
plt.plot([i*5000 for i in range(1, 20)], toPlotLower, color=(1, 0, 0, 0.25))
plt.show()

toPlotMain = [fmaa[0] for fmaa in FMAvgArr]
toPlotUpper = [fmaa[1] for fmaa in FMAvgArr]
toPlotLower = [fmaa[2] for fmaa in FMAvgArr]

plt.plot([i*5000 for i in range(1, 20)], toPlotMain, color=(0, 0, 1, 1))
plt.plot([i*5000 for i in range(1, 20)], toPlotUpper, color=(0, 0, 1, 0.25))
plt.plot([i*5000 for i in range(1, 20)], toPlotLower, color=(0, 0, 1, 0.25))
plt.show()
























