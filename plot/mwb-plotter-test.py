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
	vlist = [1,2] # MW Baseline-1, write only
	tlist = [8,16]
	load = "1:0"
if experiment == "1-ro":
	vlist = [] # MW Baseline-1, read only
	tlist = []
	load = "0:1"
if experiment == "2-wo":
	vlist = [] # MW Baseline-2, write only
	tlist = []
	load = "1:0"
if experiment == "2-ro":
	vlist = [] # MW Baseline-2, read only
	tlist = []
	load = "0:1"
reps = [1,2,3]

cli_tpt_plot = []
cli_lat_plot = []
for tmw in tlist:
	cli_settpt = []
	cli_setlat = []
	cli_gettpt = []
	cli_getlat = []
	for vcli in vlist:
		for rep in reps:
			fbase = "nsvr=1/ncli=3/icli=1/tcli=2/vcli=" + str(vcli) + "/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=1/tmw=" + str(tmw) + "/ttime=100/"
			fmain = fbase  + "*rep" + str(rep) + "*.csv"
			cli_rep_settpt = []
			cli_rep_setlat = []
			cli_rep_gettpt = []
			cli_rep_getlat = []
			fnamelist = glob.glob(resbase + fmain)
			# print len(fnamelist)
			for filename in fnamelist:
				avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
				fcli = filename.split("/")[-1]
				# print str(vcli), fcli, avgSetThru, avgSetLat
				cli_rep_settpt.append(avgSetThru)
				cli_rep_setlat.append(avgSetLat)
				cli_rep_gettpt.append(avgGetThru)
				cli_rep_getlat.append(avgGetLat)
			cli_rep_settpt = np.asarray(cli_rep_settpt)
			cli_rep_setlat = np.asarray(cli_rep_setlat)
			cli_rep_gettpt = np.asarray(cli_rep_gettpt)
			cli_rep_getlat = np.asarray(cli_rep_getlat)

			# fmain = fbase + "mwout*"
			# fnamelist = glob.glob(resbase + fmain)
			# for filename in fnamelist:
			# 	data, times, counts = getMiddlewareStatHist(filename, 5, 5)
			# 	# print tmw, vcli, rep, filename.split("/")[-1]
			# 	print data

			if experiment == "1-wo" or experiment == "2-wo":
				tot_cli_rep_settpt = np.sum(cli_rep_settpt)
				weighted = np.multiply(cli_rep_settpt, cli_rep_setlat)
				avg_cli_rep_setlat = np.divide(np.sum(weighted), tot_cli_rep_settpt)
				cli_settpt.append(tot_cli_rep_settpt)
				cli_setlat.append(avg_cli_rep_setlat)
			if experiment == "1-ro" or experiment == "2-ro":
				tot_cli_rep_gettpt = np.sum(cli_rep_gettpt)
				weighted = np.multiply(cli_rep_gettpt, cli_rep_getlat)
				avg_cli_rep_getlat = np.divide(np.sum(weighted), tot_cli_rep_gettpt)
				cli_gettpt.append(tot_cli_rep_gettpt)
				cli_getlat.append(avg_cli_rep_getlat)

	# Convert the lists into numpy arrays
	if experiment == "1-wo" or experiment == "2-wo":
		cli_settpt = np.asarray(cli_settpt)
		cli_setlat = np.asarray(cli_setlat)
		cli_settpt = cli_settpt.reshape(len(vlist),len(reps))
		cli_setlat = cli_setlat.reshape(len(vlist),len(reps))
		cli_tpt = cli_settpt
		cli_lat = cli_setlat
	if experiment == "1-ro" or experiment == "2-ro":
		cli_gettpt = np.asarray(cli_gettpt)
		cli_getlat = np.asarray(cli_getlat)
		cli_gettpt = cli_gettpt.reshape(len(vlist),len(reps))
		cli_getlat = cli_getlat.reshape(len(vlist),len(reps))
		cli_tpt = cli_gettpt
		cli_lat = cli_getlat

	tptavg = np.average(cli_tpt / 1000.0, 1)
	tpterr = np.std(cli_tpt / 1000.0, 1)
	tptlabel = "Throughput (1000 ops/sec)"
	latavg = np.average(cli_lat * 1000, 1)
	laterr = np.std(cli_lat * 1000, 1)
	latlabel = "Latency (msec)"

	cli_tpt_plot.append((tptavg, tpterr, tptlabel))
	cli_lat_plot.append((latavg, laterr, latlabel))

	tptavg = np.average(cli_tpt, 1)
	tpterr = np.std(cli_tpt, 1)
	tptlabel = "Throughput"
	latavg = np.average(cli_lat * 1000, 1)
	laterr = np.std(cli_lat * 1000, 1)
	latlabel = "Latency (msec)"

	print "vcli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", measured on clients"
	print "-"*50
	for i in range(0, len(vlist)):
		print str(vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]
	print " "

if (1):
	vlist = np.asarray(vlist)

	for i in range(0,len(tlist)):
		y, yerr, tptlabel = cli_tpt_plot[i]
		line = plt.errorbar(x=vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Virtual clients per instance")
	if experiment == "1-wo" or experiment == "1-ro":
		plt.figtext(.5,.94,'Throughput versus virtual clients p.c.i. for different thread pool sizes', fontsize=12, ha='center') # MW Baseline-1
		plt.figtext(.5,.90,'Baseline with middleware, one middleware, measured on clients', fontsize=9, ha='center') # MW Baseline-1
	if experiment == "2-wo" or experiment == "2-ro":
		plt.figtext(.5,.94,'Throughput versus virtual clients p.c.i. for different thread pool sizes', fontsize=12, ha='center') # MW Baseline-2
		plt.figtext(.5,.90,'Baseline with middleware, two middlewares, measured on clients', fontsize=9, ha='center') # MW Baseline-2
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
	vlist = np.asarray(vlist)

	for i in range(0,len(tlist)):
		y, yerr, latlabel = cli_lat_plot[i]
		line = plt.errorbar(x=vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Virtual clients per instance")
	if experiment == "1-wo" or experiment == "1-ro":
		plt.figtext(.5,.94,'Latency versus virtual clients p.c.i. for different thread pool sizes', fontsize=12, ha='center') # MW Baseline-1
		plt.figtext(.5,.90,'Baseline with middleware, one middleware, measured on clients', fontsize=9, ha='center') # MW Baseline-1
	if experiment == "2-wo" or experiment == "2-ro":
		plt.figtext(.5,.94,'Latency versus virtual clients p.c.i. for different thread pool sizes', fontsize=12, ha='center') # MW Baseline-2
		plt.figtext(.5,.90,'Baseline with middleware, two middlewares, measured on clients', fontsize=9, ha='center') # MW Baseline-2
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
