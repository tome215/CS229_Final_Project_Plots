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

fig, ax = plt.subplots()

# Set up options
usage = """usage: %prog [options] outfile key_col count_col infile1 [infile2 ...]

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
col_str = args[1]
count_str = args[2]
col_id = int(col_str)
count_id = int(count_str)
if col_id > count_id:
	max_id = col_id
else:
	max_id = count_id
	
num_files = len(args) - 3

count_arrays = []
count_dicts = []

avgArr = []

for i in range(0, num_files):
	if options.verbose:
		print "Processing: '" + args[i + 3] + "'"
	
	# Python allows us to read .gz files as easily as unzipped files,
	# as long as we know they are .gz files
	if args[i + 3][-3:] == ".gz":
		fd = gzip.open(args[i + 3])
	else:
		fd = open(args[i + 3])
	
	site_count_dict = {}
	
	total_count = 0
	
	line_num = 0
	
	for line in fd:
		line = line.strip()
		if len(line) == 0 or line[0] == '#':
			continue
		line = line.split()
				
		##################################################
		# value = int(line[col_id - 1])
		# count = int(line[count_id - 1])
		value = float(line[col_id - 1])
		count = float(line[count_id - 1])
		##################################################
		
		if value < 0:
			print "Error in file '" + args[i + 3] + "': Only positive values allowed."
			print "   (line =", line_num + 1, "count =", count, "value = " + str(value) + "')"
			sys.exit(1)
			
		if count < 0:
			print "Error in file '" + args[i + 3] + "': Only positive abundance allowed"
			sys.exit(1)
			
		# create dictionary of values : non-zero counts
		if value in site_count_dict:
			site_count_dict[value] += int(count)
		else:
			site_count_dict[value] = int(count)

		# plt.scatter([i], [value], color=(1, 0, 0, math.tanh(count)))
		
		line_num += 1
		total_count += count

	total = 0.0
	count = 0

	for k in site_count_dict.keys():
		total += k*site_count_dict[k]
		count += site_count_dict[k]

	avg = total/count

	avgArr.append(avg)

	count_dicts.append(site_count_dict)
	
	if options.verbose:
		print "  Total count =", total_count
	
	fd.close()

print("Line creation in progress...")
plt.plot(avgArr)

fig.savefig(outfilename)
plt.show()




