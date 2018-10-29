# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from summarizer import getAvgClientStat
import glob

# resbase="/home/doruk/Desktop/asl/asl-fall18-project/res/test/"
resbase = "/home/doruk/Desktop/asl/asl-fall18-project/res/"

# vlist = [1,2,3,4,8,16,24,32,40,48,64] # CS Baseline-1, write only
# vlist = [1,2,4,8,16,32] # CS Baseline-1, read only
vlist = [1,2]
reps = [1,2,3]

settpt = []
setlat = []
gettpt = []
getlat = []
for vcli in vlist:
	for rep in reps:
		rep_settpt = []
		rep_setlat = []
		rep_gettpt = []
		rep_getlat = []
		# fmain = "nsvr=1/ncli=3/icli=1/tcli=2/vcli=" + str(vcli) + "/wrkld=" + "1:0" + "/mgshrd=NA/mgsize=NA/nmw=NA/tmw=NA/ttime=100/*rep" + str(rep) + "*.csv" # CS Baseline-1, write only
		# fmain = "nsvr=1/ncli=3/icli=1/tcli=2/vcli=" + str(vcli) + "/wrkld=" + "0:1" + "/mgshrd=NA/mgsize=NA/nmw=NA/tmw=NA/ttime=100/*rep" + str(rep) + "*.csv" # CS Baseline-1, read only
		fnamelist = glob.glob(resbase + fmain)
		for filename in fnamelist:
			avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
			fcli = filename.split("/")[-1]
			# print str(vcli), fcli, avgSetThru, avgSetLat
			rep_settpt.append(avgSetThru)
			rep_setlat.append(avgSetLat)
			rep_gettpt.append(avgGetThru)
			rep_getlat.append(avgGetLat)
		rep_settpt = np.asarray(rep_settpt)
		rep_setlat = np.asarray(rep_setlat)
		rep_gettpt = np.asarray(rep_gettpt)
		rep_getlat = np.asarray(rep_getlat)

		# tot_rep_settpt = np.sum(rep_settpt)
		# weighted = np.multiply(rep_settpt, rep_setlat)
		# avg_set_lat = np.divide(np.sum(weighted), tot_rep_settpt)
		# settpt.append(tot_rep_settpt)
		# setlat.append(avg_set_lat)

		tot_rep_gettpt = np.sum(rep_gettpt)
		weighted = np.multiply(rep_gettpt, rep_getlat)
		avg_get_lat = np.divide(np.sum(weighted), tot_rep_gettpt)
		gettpt.append(tot_rep_gettpt)
		getlat.append(avg_get_lat)

# Convert the lists into numpy arrays
# settpt = np.asarray(settpt)
# setlat = np.asarray(setlat)
# settpt = settpt.reshape(len(vlist),len(reps))
# setlat = setlat.reshape(len(vlist),len(reps))
gettpt = np.asarray(gettpt)
getlat = np.asarray(getlat)
gettpt = gettpt.reshape(len(vlist),len(reps))
getlat = getlat.reshape(len(vlist),len(reps))

tpt = gettpt
lat = getlat

if (1):
	tpt = tpt / 1000.0
	y = np.average(tpt, 1)
	yerr = np.std(tpt, 1)

	vlist = np.asarray(vlist)
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label='Avg. Throughput', marker='o', capsize=2, capthick=1)

	plt.ylabel("Throughput (1000 ops/sec)")
	plt.xlabel("Virtual clients per instance")
	plt.figtext(.5,.94,'Throughput versus virtual clients per client instance', fontsize=14, ha='center') # CS Baseline-1
	plt.figtext(.5,.90,'Baseline without middleware, one server', fontsize=9, ha='center') # CS Baseline-1
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,np.max(y)*1.2))
	plt.show()
	plt.clf()

if (1):
	lat = lat * 1000
	y = np.average(lat, 1)
	yerr = np.std(lat, 1)

	vlist = np.asarray(vlist)
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label='Avg. Latency', marker='o', capsize=2, capthick=1)

	plt.ylabel("Latency (msec)") # just here if need be: μ
	plt.xlabel("Virtual clients per instance")
	plt.figtext(.5,.94,'Latency versus virtual clients per client instance', fontsize=14, ha='center') # CS Baseline-1
	plt.figtext(.5,.90,'Baseline without middleware, one server', fontsize=9, ha='center') # CS Baseline-1
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,np.max(y)*1.2))
	plt.show()
	plt.clf()
