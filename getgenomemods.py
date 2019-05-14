# This program takes a column number for phylogenetic depth, a column number 
# for number of organisms, and a series of files.  It produces a flame graph,
# a colored version of a matrix where each row is a histogram of the relevant 
# column.
# 
# Adapted from Avida's source/utils/hist_map.cc
#
# Written in Python 2.5.1
# BLW
# 9-7-09

import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser
import matplotlib.pyplot as plt
import math
from collections import defaultdict
from copy import deepcopy
from random import uniform

fig, ax = plt.subplots()

# Set up options
usage = """usage: %prog [options] outfile analyzefile logfile infile1 [infile2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-g", "--graph", action = "store_true", dest = "showgraph", 
                  default = False, help = "show the graph")
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")
                  
                  
(options, args) = parser.parse_args()

if len(args) < 4:
	parser.error("incorrect number of arguments")

outfilename = args[0]
analyzefilename = args[1]
logfilename = args[2]

outfile = open(outfilename, "w")
analyzefile = open(analyzefilename, "w")
logfile = open(logfilename, "w")

logctr = 0

for i in range(3, len(args)):
	if options.verbose:
		print "==================================================\nProcessing: '" + args[i] + "'"
	
	# Python allows us to read .gz files as easily as unzipped files,
	# as long as we know they are .gz files
	if args[i][-3:] == ".gz":
		fd = gzip.open(args[i])
	else:
		fd = open(args[i])
	
	toSkip = False
	for line in fd:
		if len(line.strip()) == 0 or line[0] == '#':
			continue

		# if not toSkip:
		# 	lineArr = line.strip().split()
			
		# 	genome = lineArr[16]
		# 	print("Processing genome\n" + genome)
		# 	for i in range(0, int(lineArr[4])):
		# 		outfile.write(genome + "\n")
		# 		analyzefile.write("LOAD_SEQUENCE " + genome + "\n")
		# 		logfile.write(str(logctr) + "\n")
		# 		logctr += 1

		# 		genArr = list(genome)
		# 		for i in range(0, len(genArr)):
		# 			genMod = deepcopy(genArr)
		# 			genMod[i] = '0' # set position i to an insert instruction
		# 			outfile.write(("").join(genMod) + "\n")
		# 			analyzefile.write("LOAD_SEQUENCE " + ("").join(genMod) + "\n")
		# 			logctr += 1

		# 		logfile.write(str(logctr) + "\n")

		# 	toSkip = True

		lineArr = line.strip().split()

		if not float(lineArr[8]):
			continue
		
		if uniform(0, 1) < 0.2:
			genome = lineArr[16]
			print("Processing genome\n" + genome)
			for i in range(0, int(lineArr[4])):
				outfile.write(genome + "\n")
				analyzefile.write("LOAD_SEQUENCE " + genome + "\n")
				logfile.write(str(logctr) + "\n")
				logctr += 1

				genArr = list(genome)
				for i in range(0, len(genArr)):
					genMod = deepcopy(genArr)
					genMod[i] = '0' # set position i to an insert instruction
					outfile.write(("").join(genMod) + "\n")
					analyzefile.write("LOAD_SEQUENCE " + ("").join(genMod) + "\n")
					logctr += 1

				logfile.write(str(logctr) + "\n")

	logfile.write("-\n")

	fd.close()

	if options.verbose:
		print "=================================================="

outfile.close()
analyzefile.close()
logfile.close()




