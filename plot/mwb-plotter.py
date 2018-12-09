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

plt.rcParams.update({'font.size': 14})
plt.rc('xtick', labelsize=12) 
plt.rc('ytick', labelsize=12) 
params = {'legend.fontsize': 12,
          'legend.handlelength': 2}
plt.rcParams.update(params)

# CHOOSE THE EXPERIMENT TYPE
experiment = sys.argv[1] # e.g. "1-wo"
out_format = sys.argv[2] # e.g. "show" or "save"

if experiment == "1-wo":
	vlist = [1,4,8,12,16,32] # MW Baseline-1, write only
	tlist = [8,16,32,64]
	load = "1:0"
if experiment == "1-ro":
	vlist = [1,2,4,8,16,32] # MW Baseline-1, read only
	tlist = [8,16,32,64]
	load = "0:1"
if experiment == "2-wo":
	vlist = [1,4,8,12,16,32,48] # MW Baseline-2, write only
	tlist = [8,16,32,64]
	load = "1:0"
if experiment == "2-ro":
	vlist = [1,2,3,4,8,32] # MW Baseline-2, read only
	tlist = [8,16,32,64]
	load = "0:1"
reps = [1,2,3]

cli_tpt_plot = []
cli_lat_plot = []
cli_tpt_maxy = 0
cli_lat_maxy = 0

law_cli_tpt_plot = []
law_cli_lat_plot = []
law_cli_tpt_maxy = 0
law_cli_lat_maxy = 0

mw_tpt_plot = []
mw_lat_plot = []
mw_tpt_maxy = 0
mw_lat_maxy = 0

law_mw_tpt_plot = []
law_mw_lat_plot = []
law_mw_tpt_maxy = 0
law_mw_lat_maxy = 0

mw_qlen_plot = []
mw_qtime_plot = []
mw_wtime_plot = []
mw_qlen_maxy = 0
mw_qtime_maxy = 0
mw_wtime_maxy = 0

for tmw in tlist:

	cli_settpt = []
	cli_setlat = []
	cli_gettpt = []
	cli_getlat = []

	mw_settpt = []
	mw_setlat = []
	mw_gettpt = []
	mw_getlat = []

	mw_qlen = []
	mw_qtime = []
	mw_wtime = []

	for vcli in vlist:
		for rep in reps:
			if experiment == "1-wo" or experiment == "1-ro":
				fbase = "nsvr=1/ncli=3/icli=1/tcli=2/vcli=" + str(vcli) + "/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=1/tmw=" + str(tmw) + "/ttime=70/"
			if experiment == "2-wo" or experiment == "2-ro":
				fbase = "nsvr=1/ncli=3/icli=2/tcli=1/vcli=" + str(vcli) + "/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=2/tmw=" + str(tmw) + "/ttime=70/"
			fmain = fbase  + "*rep" + str(rep) + "*.csv"
			cli_rep_settpt = []
			cli_rep_setlat = []
			cli_rep_gettpt = []
			cli_rep_getlat = []
			fnamelist = glob.glob(resbase + fmain)

			for filename in fnamelist:
				avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
				fcli = filename.split("/")[-1]
				# print str(vcli), fcli, avgSetThru, avgSetLat
				cli_rep_settpt.append(avgSetThru)
				cli_rep_setlat.append(avgSetLat)
				cli_rep_gettpt.append(avgGetThru)
				cli_rep_getlat.append(avgGetLat)
				# if (experiment == "2-wo" or experiment == "1-wo") and avgSetThru == 0:
				# 	print tmw, rep, vcli, fcli, avgSetThru
				# if (experiment == "2-ro" or experiment == "1-ro") and avgGetThru == 0:
				# 	print tmw, rep, vcli, fcli, avgGetThru
			cli_rep_settpt = np.asarray(cli_rep_settpt)
			cli_rep_setlat = np.asarray(cli_rep_setlat)
			cli_rep_gettpt = np.asarray(cli_rep_gettpt)
			cli_rep_getlat = np.asarray(cli_rep_getlat)

			mw_rep_settpt = []
			mw_rep_setlat = []
			mw_rep_gettpt = []
			mw_rep_getlat = []

			mw_rep_qlen = []
			mw_rep_qtime = []
			mw_rep_wtime = []

			fmain = fbase + "mwout*rep" + str(rep) + ".out"
			fnamelist = glob.glob(resbase + fmain)
			for filename in fnamelist:
				data, times, counts = getMiddlewareStatHist(filename, 5, 5)
				# print tmw, vcli, rep, filename.split("/")[-1]
				mw_rep_qlen.append(float(data[0]))
				if experiment == "1-wo" or experiment == "2-wo":
					mw_rep_settpt.append(float(data[4]))
					mw_rep_setlat.append(float(data[7]) + float(data[10]))
					mw_rep_qtime.append(float(data[7]))
					mw_rep_wtime.append(float(data[10]))
				if experiment == "1-ro" or experiment == "2-ro":
					mw_rep_gettpt.append(float(data[5]))
					mw_rep_getlat.append(float(data[8]) + float(data[11]))
					mw_rep_qtime.append(float(data[8]))
					mw_rep_wtime.append(float(data[11]))

			if experiment == "1-wo" or experiment == "2-wo":
				mw_rep_settpt = np.asarray(mw_rep_settpt)
				mw_rep_setlat = np.asarray(mw_rep_setlat)
			if experiment == "1-ro" or experiment == "2-ro":
				mw_rep_gettpt = np.asarray(mw_rep_gettpt)
				mw_rep_getlat = np.asarray(mw_rep_getlat)

			mw_rep_qlen = np.asarray(mw_rep_qlen)
			mw_rep_qtime = np.asarray(mw_rep_qtime)
			mw_rep_wtime = np.asarray(mw_rep_wtime)

			if experiment == "1-wo" or experiment == "2-wo":
				tot_cli_rep_settpt = np.sum(cli_rep_settpt)
				weighted_lat = np.multiply(cli_rep_settpt, cli_rep_setlat)
				avg_cli_rep_setlat = np.divide(np.sum(weighted_lat), tot_cli_rep_settpt)
				cli_settpt.append(tot_cli_rep_settpt)
				cli_setlat.append(avg_cli_rep_setlat)

				tot_mw_rep_settpt = np.sum(mw_rep_settpt)
				weighted_lat = np.multiply(mw_rep_settpt, mw_rep_setlat)
				avg_mw_rep_setlat = np.divide(np.sum(weighted_lat), tot_mw_rep_settpt)
				mw_settpt.append(tot_mw_rep_settpt)
				mw_setlat.append(avg_mw_rep_setlat)

				weighted_qtime = np.multiply(mw_rep_settpt, mw_rep_qtime)
				avg_mw_rep_qtime = np.divide(np.sum(weighted_qtime), tot_mw_rep_settpt)
				weighted_wtime = np.multiply(mw_rep_settpt, mw_rep_wtime)
				avg_mw_rep_wtime = np.divide(np.sum(weighted_wtime), tot_mw_rep_settpt)
				avg_mw_rep_qlen = np.average(mw_rep_qlen) # not sure about this
				mw_qlen.append(avg_mw_rep_qlen)
				mw_qtime.append(avg_mw_rep_qtime)
				mw_wtime.append(avg_mw_rep_wtime)

			if experiment == "1-ro" or experiment == "2-ro":
				tot_cli_rep_gettpt = np.sum(cli_rep_gettpt)
				weighted_lat = np.multiply(cli_rep_gettpt, cli_rep_getlat)
				avg_cli_rep_getlat = np.divide(np.sum(weighted_lat), tot_cli_rep_gettpt)
				cli_gettpt.append(tot_cli_rep_gettpt)
				cli_getlat.append(avg_cli_rep_getlat)

				tot_mw_rep_gettpt = np.sum(mw_rep_gettpt)
				weighted_lat = np.multiply(mw_rep_gettpt, mw_rep_getlat)
				avg_mw_rep_getlat = np.divide(np.sum(weighted_lat), tot_mw_rep_gettpt)
				mw_gettpt.append(tot_mw_rep_gettpt)
				mw_getlat.append(avg_mw_rep_getlat)

				weighted_qtime = np.multiply(mw_rep_gettpt, mw_rep_qtime)
				avg_mw_rep_qtime = np.divide(np.sum(weighted_qtime), tot_mw_rep_gettpt)
				weighted_wtime = np.multiply(mw_rep_gettpt, mw_rep_wtime)
				avg_mw_rep_wtime = np.divide(np.sum(weighted_wtime), tot_mw_rep_gettpt)
				avg_mw_rep_qlen = np.average(mw_rep_qlen)
				mw_qlen.append(avg_mw_rep_qlen) # not sure about this
				mw_qtime.append(avg_mw_rep_qtime)
				mw_wtime.append(avg_mw_rep_wtime)

	# Convert the lists into numpy arrays
	mw_qlen = np.asarray(mw_qlen)
	mw_qtime = np.asarray(mw_qtime)
	mw_wtime = np.asarray(mw_wtime)
	mw_qlen = mw_qlen.reshape(len(vlist),len(reps))
	mw_qtime = mw_qtime.reshape(len(vlist),len(reps))
	mw_wtime = mw_wtime.reshape(len(vlist),len(reps))

	if experiment == "1-wo" or experiment == "2-wo":
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

	if experiment == "1-ro" or experiment == "2-ro":
		cli_gettpt = np.asarray(cli_gettpt)
		cli_getlat = np.asarray(cli_getlat)
		cli_gettpt = cli_gettpt.reshape(len(vlist),len(reps))
		cli_getlat = cli_getlat.reshape(len(vlist),len(reps))
		cli_tpt = cli_gettpt
		cli_lat = cli_getlat

		mw_gettpt = np.asarray(mw_gettpt)
		mw_getlat = np.asarray(mw_getlat)
		mw_gettpt = mw_gettpt.reshape(len(vlist),len(reps))
		mw_getlat = mw_getlat.reshape(len(vlist),len(reps))
		mw_tpt = mw_gettpt
		mw_lat = mw_getlat

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

		if experiment == "1-wo" or experiment == "1-ro":
			cliMult = 6
		if experiment == "2-wo" or experiment == "2-ro":
			cliMult = 6
		mult_vlist = np.asarray(vlist) * cliMult
		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", client meas."
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]).encode('utf-8')
		print " "

		law_cli_lat = np.transpose(np.transpose(1/cli_tpt) * mult_vlist)
		law_cli_tpt = np.transpose(np.transpose(1/cli_lat) * mult_vlist)

		law_cli_tptavg = np.average(law_cli_tpt / 1000.0, 1)
		law_cli_tpterr = np.std(law_cli_tpt / 1000.0, 1)
		tptlabel = "Throughput (1000 ops/sec)"
		law_cli_latavg = np.average(law_cli_lat * 1000, 1)
		law_cli_laterr = np.std(law_cli_lat * 1000, 1)
		latlabel = "Latency (msec)"

		law_cli_tpt_plot.append((law_cli_tptavg, law_cli_tpterr, tptlabel))
		law_cli_lat_plot.append((law_cli_latavg, law_cli_laterr, latlabel))

		if np.max(law_cli_tptavg) > law_cli_tpt_maxy:
			law_cli_tpt_maxy = np.max(law_cli_tptavg)
		if np.max(law_cli_latavg) > law_cli_lat_maxy:
			law_cli_lat_maxy = np.max(law_cli_latavg)

		law_cli_tptavg = np.average(law_cli_tpt, 1)
		law_cli_tpterr = np.std(law_cli_tpt, 1)
		tptlabel = "Throughput"
		law_cli_latavg = np.average(law_cli_lat * 1000, 1)
		law_cli_laterr = np.std(law_cli_lat * 1000, 1)
		latlabel = "Latency (msec)"

		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", predictions made using measurements on clients"
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % law_cli_tptavg[i] + " ± " + "%.1f" % law_cli_tpterr[i] + "\t" + "%.3f" % law_cli_latavg[i] + " ± " + "%.3f" % law_cli_laterr[i]).encode('utf-8')
		print " "

	# Middleware aggregation
	if (1):
		tptavg = np.average(mw_tpt / 1000.0, 1)
		tpterr = np.std(mw_tpt / 1000.0, 1)
		tptlabel = "Throughput (1000 ops/sec)"
		latavg = np.average(mw_lat * 1000, 1)
		laterr = np.std(mw_lat * 1000, 1)
		latlabel = "Latency (msec)"

		qlen_avg = np.average(mw_qlen, 1)
		qlen_err = np.std(mw_qlen, 1)
		qtime_avg = np.average(mw_qtime * 1000, 1)
		qtime_err = np.std(mw_qtime * 1000, 1)
		wtime_avg = np.average(mw_wtime * 1000, 1)
		wtime_err = np.std(mw_wtime * 1000, 1)

		qlenlabel = "Average number of requests in the queue"
		mw_tpt_plot.append((tptavg, tpterr, tptlabel))
		mw_lat_plot.append((latavg, laterr, latlabel))
		mw_qlen_plot.append((qlen_avg, qlen_err, qlenlabel))
		mw_qtime_plot.append((qtime_avg, qtime_err, latlabel))
		mw_wtime_plot.append((wtime_avg, wtime_err, latlabel))

		if np.max(tptavg) > mw_tpt_maxy:
			mw_tpt_maxy = np.max(tptavg)
		if np.max(latavg) > mw_lat_maxy:
			mw_lat_maxy = np.max(latavg)

		if np.max(qlen_avg) > mw_qlen_maxy:
			mw_qlen_maxy = np.max(qlen_avg)
		if np.max(qtime_avg) > mw_qtime_maxy:
			mw_qtime_maxy = np.max(qtime_avg)
		if np.max(wtime_avg) > mw_wtime_maxy:
			mw_wtime_maxy = np.max(wtime_avg)

		tptavg = np.average(mw_tpt, 1)
		tpterr = np.std(mw_tpt, 1)
		tptlabel = "Throughput"
		latavg = np.average(mw_lat * 1000, 1)
		laterr = np.std(mw_lat * 1000, 1)
		latlabel = "Latency (msec)"

		if experiment == "1-wo" or experiment == "1-ro":
			cliMult = 6
		if experiment == "2-wo" or experiment == "2-ro":
			cliMult = 6
		mult_vlist = np.asarray(vlist) * cliMult
		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", middleware meas."
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % tptavg[i] + " ± " + "%.1f" % tpterr[i] + "\t" + "%.3f" % latavg[i] + " ± " + "%.3f" % laterr[i]).encode('utf-8')
		print " "

		# Take the difference in calculations into consideration
		latDiff = 2.5 / 1000
		law_mw_lat = np.transpose(np.transpose(1/mw_tpt) * mult_vlist) - latDiff
		law_mw_tpt = np.transpose(np.transpose(1/(mw_lat + latDiff)) * mult_vlist)
		# law_mw_lat = np.transpose(np.transpose(1/mw_tpt) * mult_vlist)
		# law_mw_tpt = np.transpose(np.transpose(1/(mw_lat)) * mult_vlist)

		law_mw_tptavg = np.average(law_mw_tpt / 1000.0, 1)
		law_mw_tpterr = np.std(law_mw_tpt / 1000.0, 1)
		tptlabel = "Throughput (1000 ops/sec)"
		law_mw_latavg = np.average(law_mw_lat * 1000, 1)
		law_mw_laterr = np.std(law_mw_lat * 1000, 1)
		latlabel = "Latency (msec)"

		law_mw_tpt_plot.append((law_mw_tptavg, law_mw_tpterr, tptlabel))
		law_mw_lat_plot.append((law_mw_latavg, law_mw_laterr, latlabel))

		if np.max(law_mw_tptavg) > law_mw_tpt_maxy:
			law_mw_tpt_maxy = np.max(law_mw_tptavg)
		if np.max(law_mw_latavg) > law_mw_lat_maxy:
			law_mw_lat_maxy = np.max(law_mw_latavg)

		law_mw_tptavg = np.average(law_mw_tpt, 1)
		law_mw_tpterr = np.std(law_mw_tpt, 1)
		tptlabel = "Throughput"
		law_mw_latavg = np.average(law_mw_lat * 1000, 1)
		law_mw_laterr = np.std(law_mw_lat * 1000, 1)
		latlabel = "Latency (msec)"

		print "vcli" + "\t" + "numCli" + "\t" + tptlabel + "\t" + latlabel + "\t" + "for tmw: " + str(tmw) + ", predictions made using measurements on middlewares"
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % law_mw_tptavg[i] + " ± " + "%.1f" % law_mw_tpterr[i] + "\t" + "%.3f" % law_mw_latavg[i] + " ± " + "%.3f" % law_mw_laterr[i]).encode('utf-8')
		print " "

		print "vcli" + "\t" + "numCli" + "\t" + "qlen" + "\t\t" + "qtime" + "\t\t" + "wtime" + "\t" + "for tmw: " + str(tmw)
		print "-"*50
		for i in range(0, len(vlist)):
			print (str(vlist[i]) + "\t" + str(mult_vlist[i]) + "\t" + "%.1f" % qlen_avg[i] + " ± " + "%.1f" % qlen_err[i] + "\t" + "%.3f" % qtime_avg[i] + " ± " + "%.3f" % qtime_err[i] + "\t" + "%.1f" % wtime_avg[i] + " ± " + "%.1f" % wtime_err[i]).encode('utf-8')
		print " "

vlist = np.asarray(vlist)
tptitle = 'Throughput versus number of clients' # + ' for diff. # worker threads in mw'
lattitle = 'Latency versus number of clients' # + ' for diff. # worker threads in mw'
vlist = np.asarray(vlist)
if experiment == "1-wo" or experiment == "1-ro":
	cliMult = 6
	subtitle = 'Baseline with mw, one mw'
if experiment == "2-wo" or experiment == "2-ro":
	cliMult = 6
	subtitle = 'Baseline with mw, two mws'
mult_vlist = vlist * cliMult
xticks = mult_vlist
if experiment == "1-wo":
	xticks = np.delete(xticks, 1)

if experiment == "1-wo" or experiment == "2-wo":
	subtitle = subtitle + ', write-only load'
if experiment == "1-ro" or experiment == "2-ro":
	subtitle = subtitle + ', read-only load'

# Client plots
if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = cli_tpt_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tptitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle + ", client meas.", fontsize=12, ha='center')
	plt.legend(loc='upper left')
	if experiment == "1-ro" or experiment == "2-ro":
		plt.legend(loc='lower right')
	plt.xticks(mult_vlist)
	plt.ylim((0,cli_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-tp" + "_cli.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, latlabel = cli_lat_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle + ", client meas.", fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,cli_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-lat" + "_cli.png")
		plt.clf()

# Middleware plots
if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = mw_tpt_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tptitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle + ", middleware meas.", fontsize=12, ha='center')
	plt.legend(loc='upper left')
	if experiment == "1-ro" or experiment == "2-ro":
		plt.legend(loc='lower right')
	plt.xticks(mult_vlist)
	plt.ylim((0,mw_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-tp" + "_mw.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, latlabel = mw_lat_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle + ", middleware meas.", fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,mw_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-lat" + "_mw.png")
		plt.clf()

# Law plots
law_tptitle = 'Predicted throughput versus # of clients' # + ' for diff. # worker threads in mw'
law_lattitle = 'Predicted latency versus number of clients' # + ' for diff. # worker threads in mw'
subtitle = 'Baseline with mw, one mw, interactive law'
law_cli_subtitle = subtitle + ' on client meas.'
law_mw_subtitle = subtitle + ' on middleware meas.'

if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = law_cli_tpt_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_tptitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,law_cli_subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	if experiment == "1-ro" or experiment == "2-ro":
		plt.legend(loc='lower right')
	plt.xticks(mult_vlist)
	plt.ylim((0,law_cli_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-tp" + "_law_cli.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, latlabel = law_cli_lat_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_lattitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,law_cli_subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,law_cli_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-lat" + "_law_cli.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, tptlabel = law_mw_tpt_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_tptitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,law_mw_subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	if experiment == "1-ro" or experiment == "2-ro":
		plt.legend(loc='lower right')
	plt.xticks(mult_vlist)
	plt.ylim((0,law_mw_tpt_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-tp" + "_law_mw.png")
		plt.clf()

if (1):
	for i in range(0,len(tlist)):
		y, yerr, latlabel = law_mw_lat_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,law_lattitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,law_mw_subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,law_mw_lat_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-lat" + "_law_mw.png")
		plt.clf()

# Additional plots
qlentitle = "Queue length versus number of clients"
qtimetitle = "Queue time versus number of clients"
wtimetitle = "Waiting time versus number of clients"
if experiment == "1-wo" or experiment == "1-ro":
	subtitle = 'Baseline with mw, one mw'
if experiment == "2-wo" or experiment == "2-ro":
	subtitle = 'Baseline with mw, two mws'

if experiment == "1-wo" or experiment == "2-wo":
	subtitle = subtitle + ', write-only load'
if experiment == "1-ro" or experiment == "2-ro":
	subtitle = subtitle + ', read-only load'

if (1):
	# plt.figure(figsize=(5,4))
	for i in range(0,len(tlist)):
		y, yerr, qlenlabel = mw_qlen_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(qlenlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,qlentitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,mw_qlen_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-qlen" + "_mw.png")
		plt.clf()

if (1):
	# plt.figure(figsize=(5,4))
	for i in range(0,len(tlist)):
		y, yerr, latlabel = mw_qtime_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,qtimetitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,mw_qtime_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-qtime" + "_mw.png")
		plt.clf()

if (1):
	# plt.figure(figsize=(5,4))
	for i in range(0,len(tlist)):
		y, yerr, latlabel = mw_wtime_plot[i]
		line = plt.errorbar(x=mult_vlist, y=y, yerr=yerr, label=str(tlist[i]) + " threads", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,wtimetitle, fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mult_vlist)
	plt.ylim((0,mw_wtime_maxy*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/mwb" + experiment + "-wtime" + "_mw.png")
		plt.clf()