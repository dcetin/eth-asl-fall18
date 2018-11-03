# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from summarizer import getAvgClientStat
from summarizer import getMiddlewareStatHist
import glob
import sys

# resbase="/home/doruk/Desktop/asl/asl-fall18-project/res/test/"
resbase = "/home/doruk/Desktop/asl/asl-fall18-project/res/"

# CHOOSE THE EXPERIMENT TYPE
experiment = sys.argv[1] # e.g. "1-wo"
out_format = sys.argv[2] # e.g. "show" or "save"

if experiment == "1-wo":
	vlist = [1,2,4,8,16,20,24,32,48,64] # CS Baseline-1, write only
	load = "1:0"
if experiment == "1-ro":
	vlist = [1,2,4,8,16,32] # CS Baseline-1, read only
	load = "0:1"
if experiment == "2-wo":
	vlist = [1,2,3,4,8,16,32] # CS Baseline-2, write only
	load = "1:0"
if experiment == "2-ro":
	vlist = [1,2,3,4,6,8,16,32] # CS Baseline-2, read only
	load = "0:1"
if experiment == "2-ro":
	vlist = [1,2,3,4,6,8,16,32] # CS Baseline-2, read only
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
		fmain = "nsvr=1/ncli=3/icli=1/tcli=2/vcli=" + str(vcli) + "/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=NA/tmw=NA/ttime=100/*rep" + str(rep) + "*.csv"
		fnamelist = glob.glob(resbase + fmain)
		# print len(fnamelist)
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

		if experiment == "1-wo" or experiment == "2-wo":
			tot_rep_settpt = np.sum(rep_settpt)
			weighted = np.multiply(rep_settpt, rep_setlat)
			avg_set_lat = np.divide(np.sum(weighted), tot_rep_settpt)
			settpt.append(tot_rep_settpt)
			setlat.append(avg_set_lat)
		if experiment == "1-ro" or experiment == "2-ro":
			tot_rep_gettpt = np.sum(rep_gettpt)
			weighted = np.multiply(rep_gettpt, rep_getlat)
			avg_get_lat = np.divide(np.sum(weighted), tot_rep_gettpt)
			gettpt.append(tot_rep_gettpt)
			getlat.append(avg_get_lat)

# Convert the lists into numpy arrays
if experiment == "1-wo" or experiment == "2-wo":
	settpt = np.asarray(settpt)
	setlat = np.asarray(setlat)
	settpt = settpt.reshape(len(vlist),len(reps))
	setlat = setlat.reshape(len(vlist),len(reps))
	tpt = settpt
	lat = setlat
if experiment == "1-ro" or experiment == "2-ro":
	gettpt = np.asarray(gettpt)
	getlat = np.asarray(getlat)
	gettpt = gettpt.reshape(len(vlist),len(reps))
	getlat = getlat.reshape(len(vlist),len(reps))
	tpt = gettpt
	lat = getlat

tptavg = np.average(tpt / 1000.0, 1)
tpterr = np.std(tpt / 1000.0, 1)
tptlabel = "Throughput (1000 ops/sec)"
latavg = np.average(lat * 1000, 1)
laterr = np.std(lat * 1000, 1)
latlabel = "Latency (msec)"

if (1):
	y = tptavg
	yerr = tpterr

	vlist = np.asarray(vlist)
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label='Avg. Throughput', marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Virtual clients per instance")
	if experiment == "1-wo" or experiment == "1-ro":
		plt.figtext(.5,.94,'Throughput versus virtual clients per client instance', fontsize=14, ha='center') # CS Baseline-1
		plt.figtext(.5,.90,'Baseline without middleware, one server', fontsize=9, ha='center') # CS Baseline-1
	if experiment == "2-wo" or experiment == "2-ro":
		plt.figtext(.5,.94,'Throughput versus virtual clients per client instance', fontsize=14, ha='center') # CS Baseline-2
		plt.figtext(.5,.90,'Baseline without middleware, two servers', fontsize=9, ha='center') # CS Baseline-2
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,np.max(y)*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/csb" + experiment + "-tp" + ".png")
		plt.clf()

if (1):
	y = latavg
	yerr = laterr

	vlist = np.asarray(vlist)
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label='Avg. Latency', marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Virtual clients per instance")
	if experiment == "1-wo" or experiment == "1-ro":
		plt.figtext(.5,.94,'Latency versus virtual clients per client instance', fontsize=14, ha='center') # CS Baseline-1
		plt.figtext(.5,.90,'Baseline without middleware, one server', fontsize=9, ha='center') # CS Baseline-1
	if experiment == "2-wo" or experiment == "2-ro":
		plt.figtext(.5,.94,'Latency versus virtual clients per client instance', fontsize=14, ha='center') # CS Baseline-2
		plt.figtext(.5,.90,'Baseline without middleware, two servers', fontsize=9, ha='center') # CS Baseline-2
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,np.max(y)*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/csb" + experiment + "-lat" + ".png")
		plt.clf()

tptavg = np.average(tpt, 1)
tpterr = np.std(tpt, 1)
tptlabel = "Throughput"
latavg = np.average(lat * 1000, 1)
laterr = np.std(lat * 1000, 1)
latlabel = "Latency (msec)"

print "vcli" + "\t" + tptlabel + "\t" + latlabel
print "-"*50
for i in range(0, len(vlist)):
	print str(vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]
