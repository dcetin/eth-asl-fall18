# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from summarizer import getAvgClientStat

resbase = "/home/doruk/Desktop/asl/asl-fall18-project/res/test/"

vlist = [1,2,4]
reps = [1,2,3]
clis = [1,2]

setThru = []
setLat = []
getThru = []
getLat = []
for vcli in vlist:
	for rep in reps:
		for cli in clis:
			fmain = "nsvr=2/ncli=1/icli=2/tcli=1/vcli=" + str(vcli) + "/wrkld=" + "1:0" + "/mgshrd=NA/mgsize=NA/nmw=NA/tmw=NA/ttime=10/"
			fcli = "cli" + str(cli) + "rep" + str(rep) + "-1-0-0.csv"
			fname = fmain + fcli
			avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(resbase, fname, 1, 1)
			# print fcli, avgSetThru, avgSetLat
			setThru.append(avgSetThru)
			setLat.append(avgSetLat)
			getThru.append(avgGetThru)
			getLat.append(avgGetLat)

# Convert the lists into numpy arrays
setThru = np.asarray(setThru)
setLat = np.asarray(setLat)
setThru = setThru.reshape(len(vlist),len(reps),len(clis))
setLat = setLat.reshape(len(vlist),len(reps),len(clis))
getThru = np.asarray(getThru)
getLat = np.asarray(getLat)
getThru = getThru.reshape(len(vlist),len(reps),len(clis))
getLat = getLat.reshape(len(vlist),len(reps),len(clis))

# For each type of workload
thru = setThru
lat = setLat

if (0):
	aggThru = np.sum(thru, 2)
	y = np.average(aggThru, 1)
	yerr = np.std(aggThru, 1)

	vlist = np.asarray(vlist)
	vlist = np.asarray([1,2,4])
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label='Avg. Throughput', marker='o', capsize=2, capthick=1)

	plt.ylabel("Throughput (ops/sec)")
	plt.xlabel("Virtual clients per instance")
	plt.figtext(.5,.94,'Throughput versus virtual clients per client instance', fontsize=14, ha='center')
	plt.figtext(.5,.90,'Baseline without middleware, two servers',fontsize=9,ha='center')
	plt.legend(loc='upper right')
	plt.xticks(vlist)
	plt.show()
	plt.clear()

if (0):
	aggLat = np.divide(np.sum(np.multiply(thru, lat), 2), np.sum(thru, 2))
	aggLat = aggLat * 1000 * 1000
	y = np.average(aggLat, 1)
	yerr = np.std(aggLat, 1)

	vlist = np.asarray(vlist)
	vlist = np.asarray([1,2,4])
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label='Avg. Latency', marker='o', capsize=2, capthick=1)

	plt.ylabel("Latency (μsec)")
	plt.xlabel("Virtual clients per instance")
	plt.figtext(.5,.94,'Latency versus virtual clients per client instance', fontsize=14, ha='center')
	plt.figtext(.5,.90,'Baseline without middleware, two servers',fontsize=9,ha='center')
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.show()
	plt.clear()