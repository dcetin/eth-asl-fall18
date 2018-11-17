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

out_format = sys.argv[1] # e.g. "show" or "save"

def_vlist = [1,4,8,16,32,48]
tlist = [8,16,32,64]
vcli_lists = [ [1,4,8,16,32,48], [1,4,6,8,16,32,48], [1,4,8,12,16,32,48], [1,4,8,16,24,32,48] ]
reps = [1,2,3]

cli_tpt_plot = []
cli_lat_plot = []
cli_tpt_maxy = 0
cli_lat_maxy = 0

law_tpt_plot = []
law_lat_plot = []
law_tpt_maxy = 0
law_lat_maxy = 0

mw_tpt_plot = []
mw_lat_plot = []
mw_tpt_maxy = 0
mw_lat_maxy = 0

for tmw_idx, tmw in enumerate(tlist):

	cli_settpt = []
	cli_setlat = []

	mw_settpt = []
	mw_setlat = []

	vlist = vcli_lists[tmw_idx]

	for vcli in vlist:
		for rep in reps:
			fbase = "nsvr=3/ncli=3/icli=2/tcli=1/vcli=" + str(vcli) + "/wrkld=1:0/mgshrd=NA/mgsize=NA/nmw=2/tmw=" + str(tmw) + "/ttime=70/"
			fmain = fbase  + "*rep" + str(rep) + "*.csv"
			cli_rep_settpt = []
			cli_rep_setlat = []
			fnamelist = glob.glob(resbase + fmain)

			for filename in fnamelist:
				avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
				fcli = filename.split("/")[-1]
				# print str(vcli), fcli, avgSetThru, avgSetLat
				cli_rep_settpt.append(avgSetThru)
				cli_rep_setlat.append(avgSetLat)
				if avgSetThru == 0:
					print tmw, rep, vcli, fcli, avgSetThru
			cli_rep_settpt = np.asarray(cli_rep_settpt)
			cli_rep_setlat = np.asarray(cli_rep_setlat)

			mw_rep_settpt = []
			mw_rep_setlat = []
			fmain = fbase + "mwout*rep" + str(rep) + ".out"
			fnamelist = glob.glob(resbase + fmain)
			for filename in fnamelist:
				data, times, counts = getMiddlewareStatHist(filename, 5, 5)
				# print tmw, vcli, rep, filename.split("/")[-1]
				mw_rep_settpt.append(float(data[4]))
				mw_rep_setlat.append(float(data[7]) + float(data[10]))
			mw_rep_settpt = np.asarray(mw_rep_settpt)
			mw_rep_setlat = np.asarray(mw_rep_setlat)

			tot_cli_rep_settpt = np.sum(cli_rep_settpt)
			weighted = np.multiply(cli_rep_settpt, cli_rep_setlat)
			avg_cli_rep_setlat = np.divide(np.sum(weighted), tot_cli_rep_settpt)
			cli_settpt.append(tot_cli_rep_settpt)
			cli_setlat.append(avg_cli_rep_setlat)

			tot_mw_rep_settpt = np.sum(mw_rep_settpt)
			weighted = np.multiply(mw_rep_settpt, mw_rep_setlat)
			avg_mw_rep_setlat = np.divide(np.sum(weighted), tot_mw_rep_settpt)
			mw_settpt.append(tot_mw_rep_settpt)
			mw_setlat.append(avg_mw_rep_setlat)

	# Convert the lists into numpy arrays
	cli_settpt = np.asarray(cli_settpt)
	cli_setlat = np.asarray(cli_setlat)
	cli_settpt = cli_settpt.reshape(len(vlist),len(reps))
	cli_setlat = cli_setlat.reshape(len(vlist),len(reps))
	cli_tpt = cli_settpt
	cli_lat = cli_setlat

	mw_settpt = np.asarray(mw_settpt)
	mw_setlat = np.asarray(mw_setlat)
	mw_settpt = mw_settpt.reshape(len(vlist),len(reps))
	mw_setlat = mw_setlat.reshape(len(vlist),len(reps))
	mw_tpt = mw_settpt
	mw_lat = mw_setlat

	# Client aggregation
	if (1):
		tptavg = np.average(cli_tpt / 1000.0, 1)
		tpterr = np.std(cli_tpt / 1000.0, 1)
		tptlabel = "Throughput (1000 ops/sec)"
		latavg = np.average(cli_lat * 1000, 1)
		laterr = np.std(cli_lat * 1000, 1)
		latlabel = "Latency (msec)"

		cli_tpt_plot.append((tptavg, tpterr, tptlabel))
		cli_lat_plot.append((latavg, laterr, latlabel))

		if np.max(tptavg) > cli_tpt_maxy:
			cli_tpt_maxy = np.max(tptavg)
		if np.max(latavg) > cli_lat_maxy:
			cli_lat_maxy = np.max(latavg)

		tptavg = np.average(cli_tpt, 1)
		tpterr = np.std(cli_tpt, 1)
		tptlabel = "Throughput"
		latavg = np.average(cli_lat * 1000, 1)
		laterr = np.std(cli_lat * 1000, 1)
		latlabel = "Latency (msec)"

		cliMult = 6
		mult_vlist = np.asarray(vlist) * cliMult

		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", measured on clients"
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]).encode('utf-8')
		print " "

		law_lat = np.transpose(np.transpose(1/cli_tpt) * mult_vlist)
		law_tpt = np.transpose(np.transpose(1/cli_lat) * mult_vlist)

		law_tptavg = np.average(law_tpt / 1000.0, 1)
		law_tpterr = np.std(law_tpt / 1000.0, 1)
		tptlabel = "Throughput (1000 ops/sec)"
		law_latavg = np.average(law_lat * 1000, 1)
		law_laterr = np.std(law_lat * 1000, 1)
		latlabel = "Latency (msec)"

		law_tpt_plot.append((law_tptavg, law_tpterr, tptlabel))
		law_lat_plot.append((law_latavg, law_laterr, latlabel))

		if np.max(law_tptavg) > law_tpt_maxy:
			law_tpt_maxy = np.max(law_tptavg)
		if np.max(law_latavg) > law_lat_maxy:
			law_lat_maxy = np.max(law_latavg)

		law_tptavg = np.average(law_tpt, 1)
		law_tpterr = np.std(law_tpt, 1)
		tptlabel = "Throughput"
		law_latavg = np.average(law_lat * 1000, 1)
		law_laterr = np.std(law_lat * 1000, 1)
		latlabel = "Latency (msec)"

		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", predictions made using measurements on clients"
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % law_tptavg[i] + " ± " + "%.1f" % law_tpterr[i] + "\t" + "%.3f" % law_latavg[i] + " ± " + "%.3f" % law_laterr[i]).encode('utf-8')
		print " "

	# Middleware aggregation
	if (1):
		tptavg = np.average(mw_tpt / 1000.0, 1)
		tpterr = np.std(mw_tpt / 1000.0, 1)
		tptlabel = "Throughput (1000 ops/sec)"
		latavg = np.average(mw_lat * 1000, 1)
		laterr = np.std(mw_lat * 1000, 1)
		latlabel = "Latency (msec)"

		mw_tpt_plot.append((tptavg, tpterr, tptlabel))
		mw_lat_plot.append((latavg, laterr, latlabel))

		if np.max(tptavg) > mw_tpt_maxy:
			mw_tpt_maxy = np.max(tptavg)
		if np.max(latavg) > mw_lat_maxy:
			mw_lat_maxy = np.max(latavg)

		tptavg = np.average(mw_tpt, 1)
		tpterr = np.std(mw_tpt, 1)
		tptlabel = "Throughput"
		latavg = np.average(mw_lat * 1000, 1)
		laterr = np.std(mw_lat * 1000, 1)
		latlabel = "Latency (msec)"

		cliMult = 6
		mult_vlist = np.asarray(vlist) * cliMult

		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", measured on middlewares"
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]).encode('utf-8')
		print " "

def_vlist = np.asarray(def_vlist)
tptitle = 'Throughput versus number of clients for diff. # worker threads in mw'
lattitle = 'Latency versus number of clients for diff. # worker threads in mw'
cliMult = 6
subtitle = 'Throughput for writes, full system, measured on clients'
def_vlist = def_vlist * cliMult
for i,x in enumerate(vcli_lists):
	vcli_lists[i] = np.asarray(vcli_lists[i]) * cliMult
xticks = def_vlist
subtitle = subtitle + ', write-only load'

# Client plots
if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = cli_tpt_plot[i]
		line = plt.errorbar(x=vcli_lists[i] , y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tptitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(def_vlist)
	plt.ylim((0,cli_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/tpfw-tp_cli.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = cli_lat_plot[i]
		line = plt.errorbar(x=vcli_lists[i] , y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(def_vlist)
	plt.ylim((0,cli_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/tpfw-lat_cli.png")
		plt.clf()

# Middleware plots
if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = mw_tpt_plot[i]
		line = plt.errorbar(x=vcli_lists[i] , y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tptitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(def_vlist)
	plt.ylim((0,mw_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/tpfw-tp_mw.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = mw_lat_plot[i]
		line = plt.errorbar(x=vcli_lists[i] , y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(def_vlist)
	plt.ylim((0,mw_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/tpfw-lat_mw.png")
		plt.clf()

law_tptitle = 'Predicted throughput versus # of clients for diff. # worker threads in mw'
law_lattitle = 'Predicted latency versus number of clients for diff. # worker threads in mw'

# Law plots
if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = law_tpt_plot[i]
		line = plt.errorbar(x=vcli_lists[i], y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_tptitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(def_vlist)
	plt.ylim((0,law_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/tpfw-law_tp" + "_cli.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, latlabel = law_lat_plot[i]
		line = plt.errorbar(x=vcli_lists[i], y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_lattitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(def_vlist)
	plt.ylim((0,law_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/tpfw-law_lat" + "_cli.png")
		plt.clf()