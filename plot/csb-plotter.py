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
		if experiment == "1-ro" or experiment == "1-wo":
			fmain = "nsvr=1/ncli=3/icli=1/tcli=2/vcli=" + str(vcli) + "/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=NA/tmw=NA/ttime=100/*rep" + str(rep) + "*.csv"
		if experiment == "2-ro" or experiment == "2-wo":
			fmain = "nsvr=2/ncli=1/icli=2/tcli=1/vcli=" + str(vcli) + "/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=NA/tmw=NA/ttime=100/*rep" + str(rep) + "*.csv"
		fnamelist = glob.glob(resbase + fmain)
		# print rep, vcli, len(fnamelist)
		for filename in fnamelist:
			avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
			fcli = filename.split("/")[-1]
			# print str(vcli), fcli, avgSetThru, avgSetLat
			rep_settpt.append(avgSetThru)
			rep_setlat.append(avgSetLat)
			rep_gettpt.append(avgGetThru)
			rep_getlat.append(avgGetLat)
			if (experiment == "2-wo" or experiment == "1-wo") and avgSetThru == 0:
				print rep, vcli, fcli, avgSetThru
			if (experiment == "2-ro" or experiment == "1-ro") and avgGetThru == 0:
				print rep, vcli, fcli, avgGetThru
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

tpttitle = 'Throughput versus number of clients'
lattitle = 'Latency versus number of clients'
law_lattitle = 'Actual and predicted latency versus number of clients'
law_tpttitle = 'Actual and predicted throughput versus number of clients'

vlist = np.asarray(vlist)
if experiment == "1-wo" or experiment == "1-ro":
	cliMult = 6
	subtitle = 'Baseline without middleware, one server'
if experiment == "2-wo" or experiment == "2-ro":
	cliMult = 2
	subtitle = 'Baseline without middleware, two servers'
mult_vlist = vlist * cliMult
xticks = mult_vlist
if experiment == "1-wo":
	xticks = np.delete(xticks, 1)

if experiment == "1-wo" or experiment == "2-wo":
	subtitle = subtitle + ', write-only load'
if experiment == "1-ro" or experiment == "2-ro":
	subtitle = subtitle + ', read-only load'

import matplotlib
matplotlib.rc('xtick', labelsize=10) 

if (1):
	y = tptavg
	yerr = tpterr
	line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label='Throughput', marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tpttitle, fontsize=14, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(xticks)
	plt.ylim((0,np.max(y)*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/csb" + experiment + "-tp" + ".png")
		plt.clf()

if (1):
	y = latavg
	yerr = laterr
	line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label='Latency', marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=14, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(xticks)
	plt.ylim((0,np.max(y)*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/csb" + experiment + "-lat" + ".png")
		plt.clf()

tptavg = np.average(tpt, 1)
tpterr = np.std(tpt, 1)
tptlabel = "Throughput"
latavg = np.average(lat * 1000, 1)
laterr = np.std(lat * 1000, 1)
latlabel = "Latency (msec)"

print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel
print "-"*50
for i in range(0, len(vlist)):
	print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]).encode('utf-8')

law_lat = np.transpose(np.transpose(1/tpt) * mult_vlist)
law_latavg = np.average(1000 * law_lat, 1)
law_laterr = np.std(1000 * law_lat, 1)
latavg = np.average(1000 * lat, 1)
laterr = np.std(1000 * lat, 1)

law_tpt = np.transpose(np.transpose(1/lat) * mult_vlist)
law_tptavg = np.average(law_tpt / 1000.0, 1)
law_tpterr = np.std(law_tpt / 1000.0, 1)
tptavg = np.average(tpt / 1000.0, 1)
tpterr = np.std(tpt / 1000.0, 1)
tptlabel = "Throughput (1000 ops/sec)"
latlabel = "Latency (msec)"

if (1):
	y = law_tptavg
	yerr = law_tpterr
	line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label='Predicted throughput', marker='o', capsize=2, capthick=1)
	y = tptavg
	yerr = tpterr
	line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label='Actual throughput', marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_tpttitle, fontsize=14, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(xticks)
	plt.ylim((0,np.max(y)*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/csb" + experiment + "-law_tpt" + ".png")
		plt.clf()

if (1):
	y = law_latavg
	yerr = law_laterr
	line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label='Predicted latency', marker='o', capsize=2, capthick=1)
	y = latavg
	yerr = laterr
	line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label='Actual latency', marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_lattitle, fontsize=14, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(xticks)
	plt.ylim((0,np.max(y)*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/csb" + experiment + "-law_lat" + ".png")
		plt.clf()