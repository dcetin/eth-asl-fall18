# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from summarizer import getAvgClientStat, getMiddlewareStat, drawHist, drawHist2, getClientPercentile, combineClientHists
from summarizer import getMiddlewareHist, combineMiddlewareHists, aggregateHists, getClientOut
import glob
import sys

plt.rcParams.update({'font.size': 14})
plt.rc('xtick', labelsize=14) 
plt.rc('ytick', labelsize=14) 
params = {'legend.fontsize': 12,
          'legend.handlelength': 2}
plt.rcParams.update(params)

op_type = sys.argv[1] # e.g. "set" or "mget"
keys = sys.argv[2] # e.g. "std" or "extra"
out_format = sys.argv[3] # e.g. "show" or "save"
resbase = "/home/doruk/Desktop/asl/asl-fall18-project/res/"
mgshrdList = ["true", "false"]
ttime = 70
reps = [1,2,3]

hist_cuttime = 160
ymax_hist = 14000
if keys == "std":
	mlist = [1,3,6,9]
	ymax_perc = 20
	ystep = 1
if keys == "extra":
	mlist = [9,18,27,54,81]
	ymax_perc = 300
	ystep = 25


# Init plot vals
if True:
	cli_tpt_plot = []
	cli_lat_plot = []
	cli_tpt_maxy = 0
	cli_lat_maxy = 0
	mw_tpt_plot = []
	mw_lat_plot = []
	mw_tpt_maxy = 0
	mw_lat_maxy = 0
	law_cli_tpt_plot = []
	law_cli_lat_plot = []
	law_cli_tpt_maxy = 0
	law_cli_lat_maxy = 0
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

# Returns (cli_tpt, cli_lat, mw_tpt, mw_lat, mw_qtime, mw_wtime, mw_qlen)
def dataFromFiles(mgshrd):
	global resbase
	global reps
	global mlist

	cli_settpt = []
	cli_setlat = []
	mw_settpt = []
	mw_setlat = []
	mw_setqtime = []
	mw_setwtime = []

	cli_mgettpt = []
	cli_mgetlat = []
	mw_mgettpt = []
	mw_mgetlat = []
	mw_mgetqtime = []
	mw_mgetwtime = []

	mw_qlen = []

	for mgsize in mlist:

		fbase = "nsvr=3/ncli=3/icli=2/tcli=1/vcli=2/wrkld=1:" + str(mgsize) + "/mgshrd=" + mgshrd + "/mgsize=" + str(mgsize) + "/nmw=2/tmw=8/ttime="+str(ttime)+"/"

		for rep in reps:

			# Iterate over output files for this repetition
			if(1):
				cli_rep_settpt = []
				cli_rep_setlat = []
				mw_rep_settpt = []
				mw_rep_setlat = []
				mw_rep_setqtime = []
				mw_rep_setwtime = []

				cli_rep_mgettpt = []
				cli_rep_mgetlat = []
				mw_rep_mgettpt = []
				mw_rep_mgetlat = []
				mw_rep_mgetqtime = []
				mw_rep_mgetwtime = []

				mw_rep_qlen = []

				if True:
					fmain = fbase + "cliout*rep" + str(rep) + ".out"
					fnamelist = glob.glob(resbase + fmain)
					for filename in fnamelist:
						fcli = filename.split("/")[-1]
						avgSetThru, avgGetThru, avgSetLat, avgGetLat = getClientOut(filename)
						# print "out", mgsize, mgshrd, rep, fcli, avgSetLat
						cli_rep_settpt.append(avgSetThru)
						cli_rep_setlat.append(avgSetLat)
						cli_rep_mgettpt.append(avgGetThru)
						cli_rep_mgetlat.append(avgGetLat)
						if avgSetThru == 0:
							print mgsize, mgshrd, rep, fcli, avgSetThru

				if False:
					fmain = fbase  + "*rep" + str(rep) + "*.csv"
					fnamelist = glob.glob(resbase + fmain)
					# Iterate over the client files
					for filename in fnamelist:
						fcli = filename.split("/")[-1]
						avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
						# print "cli", mgsize, mgshrd, rep, fcli, avgSetLat
						cli_rep_settpt.append(avgSetThru)
						cli_rep_setlat.append(avgSetLat)
						cli_rep_mgettpt.append(avgGetThru)
						cli_rep_mgetlat.append(avgGetLat)
						if avgSetThru == 0:
							print mgsize, mgshrd, rep, fcli, avgSetThru

				cli_rep_settpt = np.asarray(cli_rep_settpt)
				cli_rep_setlat = np.asarray(cli_rep_setlat)
				cli_rep_mgettpt = np.asarray(cli_rep_mgettpt)
				cli_rep_mgetlat = np.asarray(cli_rep_mgetlat)

				# Iterate over the middleware files
				fmain = fbase + "mwout*rep" + str(rep) + ".out"
				fnamelist = glob.glob(resbase + fmain)
				for filename in fnamelist:
					fcli = filename.split("/")[-1]
					data = getMiddlewareStat(filename, 5, 5)
					mw_rep_qlen.append(float(data[0]))
					mw_rep_settpt.append(float(data[4]))
					mw_rep_setlat.append(float(data[7]) + float(data[10]))
					mw_rep_setqtime.append(float(data[7]))
					mw_rep_setwtime.append(float(data[10]))
					if mgsize > 1:
						mw_rep_mgettpt.append(float(data[6]))
						mw_rep_mgetlat.append(float(data[9]) + float(data[12]))
						mw_rep_mgetqtime.append(float(data[9]))
						mw_rep_mgetwtime.append(float(data[12]))
					else:
						mw_rep_mgettpt.append(float(data[5]))
						mw_rep_mgetlat.append(float(data[8]) + float(data[11]))
						mw_rep_mgetqtime.append(float(data[8]))
						mw_rep_mgetwtime.append(float(data[11]))

				mw_rep_qlen = np.asarray(mw_rep_qlen)
				mw_rep_setqtime = np.asarray(mw_rep_setqtime)
				mw_rep_setwtime = np.asarray(mw_rep_setwtime)
				mw_rep_settpt = np.asarray(mw_rep_settpt)
				mw_rep_setlat = np.asarray(mw_rep_setlat)
				mw_rep_mgetqtime = np.asarray(mw_rep_mgetqtime)
				mw_rep_mgetwtime = np.asarray(mw_rep_mgetwtime)
				mw_rep_mgettpt = np.asarray(mw_rep_mgettpt)
				mw_rep_mgetlat = np.asarray(mw_rep_mgetlat)

			# Repetition aggregation
			if(1):
				# Client set
				tot_cli_rep_settpt = np.sum(cli_rep_settpt)
				weighted = np.multiply(cli_rep_settpt, cli_rep_setlat)
				avg_cli_rep_setlat = np.divide(np.sum(weighted), tot_cli_rep_settpt)
				cli_settpt.append(tot_cli_rep_settpt)
				cli_setlat.append(avg_cli_rep_setlat)
				# Middleware set
				tot_mw_rep_settpt = np.sum(mw_rep_settpt)
				weighted = np.multiply(mw_rep_settpt, mw_rep_setlat)
				avg_mw_rep_setlat = np.divide(np.sum(weighted), tot_mw_rep_settpt)
				mw_settpt.append(tot_mw_rep_settpt)
				mw_setlat.append(avg_mw_rep_setlat)
				# Client mget
				tot_cli_rep_mgettpt = np.sum(cli_rep_mgettpt)
				weighted = np.multiply(cli_rep_mgettpt, cli_rep_mgetlat)
				avg_cli_rep_mgetlat = np.divide(np.sum(weighted), tot_cli_rep_mgettpt)
				cli_mgettpt.append(tot_cli_rep_mgettpt)
				cli_mgetlat.append(avg_cli_rep_mgetlat)
				# Middleware mget
				tot_mw_rep_mgettpt = np.sum(mw_rep_mgettpt)
				weighted = np.multiply(mw_rep_mgettpt, mw_rep_mgetlat)
				avg_mw_rep_mgetlat = np.divide(np.sum(weighted), tot_mw_rep_mgettpt)
				mw_mgettpt.append(tot_mw_rep_mgettpt)
				mw_mgetlat.append(avg_mw_rep_mgetlat)
				# Middleware set details
				weighted_setqtime = np.multiply(mw_rep_settpt, mw_rep_setqtime)
				avg_mw_rep_setqtime = np.divide(np.sum(weighted_setqtime), tot_mw_rep_settpt)
				weighted_setwtime = np.multiply(mw_rep_settpt, mw_rep_setwtime)
				avg_mw_rep_setwtime = np.divide(np.sum(weighted_setwtime), tot_mw_rep_settpt)
				mw_setqtime.append(avg_mw_rep_setqtime)
				mw_setwtime.append(avg_mw_rep_setwtime)
				# Middleware mget details
				weighted_mgetqtime = np.multiply(mw_rep_mgettpt, mw_rep_mgetqtime)
				avg_mw_rep_mgetqtime = np.divide(np.sum(weighted_mgetqtime), tot_mw_rep_mgettpt)
				weighted_mgetwtime = np.multiply(mw_rep_mgettpt, mw_rep_mgetwtime)
				avg_mw_rep_mgetwtime = np.divide(np.sum(weighted_mgetwtime), tot_mw_rep_mgettpt)
				mw_mgetqtime.append(avg_mw_rep_mgetqtime)
				mw_mgetwtime.append(avg_mw_rep_mgetwtime)
				# Middleware qlen
				avg_mw_rep_qlen = np.average(mw_rep_qlen) # averages over middlewares
				mw_qlen.append(avg_mw_rep_qlen)
		
	# Convert the lists into numpy arrays
	if(1):
		cli_settpt = np.asarray(cli_settpt)
		cli_setlat = np.asarray(cli_setlat)
		cli_settpt = cli_settpt.reshape(len(mlist),len(reps))
		cli_setlat = cli_setlat.reshape(len(mlist),len(reps))
		mw_settpt = np.asarray(mw_settpt)
		mw_setlat = np.asarray(mw_setlat)
		mw_settpt = mw_settpt.reshape(len(mlist),len(reps))
		mw_setlat = mw_setlat.reshape(len(mlist),len(reps))
		cli_mgettpt = np.asarray(cli_mgettpt)
		cli_mgetlat = np.asarray(cli_mgetlat)
		cli_mgettpt = cli_mgettpt.reshape(len(mlist),len(reps))
		cli_mgetlat = cli_mgetlat.reshape(len(mlist),len(reps))
		mw_mgettpt = np.asarray(mw_mgettpt)
		mw_mgetlat = np.asarray(mw_mgetlat)
		mw_mgettpt = mw_mgettpt.reshape(len(mlist),len(reps))
		mw_mgetlat = mw_mgetlat.reshape(len(mlist),len(reps))
		mw_qlen = np.asarray(mw_qlen)
		mw_qlen = mw_qlen.reshape(len(mlist),len(reps))
		mw_setqtime = np.asarray(mw_setqtime)
		mw_setwtime = np.asarray(mw_setwtime)
		mw_setqtime = mw_setqtime.reshape(len(mlist),len(reps))
		mw_setwtime = mw_setwtime.reshape(len(mlist),len(reps))
		mw_mgetqtime = np.asarray(mw_mgetqtime)
		mw_mgetwtime = np.asarray(mw_mgetwtime)
		mw_mgetqtime = mw_mgetqtime.reshape(len(mlist),len(reps))
		mw_mgetwtime = mw_mgetwtime.reshape(len(mlist),len(reps))

		if op_type == "set":
			cli_tpt = cli_settpt
			cli_lat = cli_setlat
			mw_tpt = mw_settpt
			mw_lat = mw_setlat
			mw_qtime = mw_setqtime
			mw_wtime = mw_setwtime
		if op_type == "mget":
			cli_tpt = cli_mgettpt
			cli_lat = cli_mgetlat
			mw_tpt = mw_mgettpt
			mw_lat = mw_mgetlat
			mw_qtime = mw_mgetqtime
			mw_wtime = mw_mgetwtime

	return cli_tpt, cli_lat, mw_tpt, mw_lat, mw_qtime, mw_wtime, mw_qlen

def prepForPlot(aggRet):
	cli_tpt, cli_lat, mw_tpt, mw_lat, mw_qtime, mw_wtime, mw_qlen = aggRet
	if(1):
		global cli_tpt_plot
		global cli_lat_plot
		global cli_tpt_maxy
		global cli_lat_maxy
		global mw_tpt_plot
		global mw_lat_plot
		global mw_tpt_maxy
		global mw_lat_maxy
		global law_cli_tpt_plot
		global law_cli_lat_plot
		global law_cli_tpt_maxy
		global law_cli_lat_maxy
		global law_mw_tpt_plot
		global law_mw_lat_plot
		global law_mw_tpt_maxy
		global law_mw_lat_maxy
		global mw_qlen_plot
		global mw_qtime_plot
		global mw_wtime_plot
		global mw_qlen_maxy
		global mw_qtime_maxy
		global mw_wtime_maxy

	tptavg = np.average(cli_tpt / 1000.0, 1)
	tpterr = np.std(cli_tpt / 1000.0, 1)
	tptlabel = "Throughput (1000 ops/sec)"
	# latavg = np.average(cli_lat * 1000, 1)
	# laterr = np.std(cli_lat * 1000, 1)
	# latlabel = "Latency (msec)"
	latavg = np.average(cli_lat, 1)
	laterr = np.std(cli_lat, 1)
	latlabel = "Latency (msec)"

	cli_tpt_plot.append((tptavg, tpterr, tptlabel))
	cli_lat_plot.append((latavg, laterr, latlabel))

	if np.max(tptavg) > cli_tpt_maxy:
		cli_tpt_maxy = np.max(tptavg)
	if np.max(latavg) > cli_lat_maxy:
		cli_lat_maxy = np.max(latavg)

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

def prepHistograms(percDict, mgshrd, op_type, histmaxy, cutTime):
	global resbase
	global reps
	global mlist

	for mgsize in mlist:
		fbase = "nsvr=3/ncli=3/icli=2/tcli=1/vcli=2/wrkld=1:" + str(mgsize) + "/mgshrd=" + mgshrd + "/mgsize=" + str(mgsize) + "/nmw=2/tmw=8/ttime="+str(ttime)+"/"

		mw_mgsize_sethist = []
		mw_mgsize_mgethist = []
		cli_mgsize_sethist = []
		cli_mgsize_mgethist = []
		cli_mgsize_setperc = []
		cli_mgsize_mgetperc = []

		for rep in reps:
			# Iterate over output files for this repetition
			mw_rep_sethist = []
			mw_rep_mgethist = []
			cli_rep_sethist = []
			cli_rep_mgethist = []
			cli_rep_setperc = []
			cli_rep_mgetperc = []

			# Iterate over the client files
			fmain = fbase  + "cliout*rep" + str(rep) + ".out"
			fnamelist = glob.glob(resbase + fmain)
			for filename in fnamelist:
				fcli = filename.split("/")[-1]
				set_perc = getClientPercentile(filename, ttime, "SET")
				mget_perc = getClientPercentile(filename, ttime, "GET")
				set_hist = set_perc[:2]
				mget_hist = mget_perc[:2]
				set_perc = set_perc[4]
				mget_perc = mget_perc[4]
				cli_rep_sethist.append(set_hist)
				cli_rep_mgethist.append(mget_hist)
				cli_rep_setperc.append(set_perc)
				cli_rep_mgetperc.append(mget_perc)

			cli_mgsize_sethist.append(combineClientHists(cli_rep_sethist))
			cli_mgsize_mgethist.append(combineClientHists(cli_rep_mgethist))
			cli_mgsize_setperc.append(np.average(cli_rep_setperc, 0))
			cli_mgsize_mgetperc.append(np.average(cli_rep_mgetperc, 0))

			# Iterate over the middleware files
			fmain = fbase + "mwout*rep" + str(rep) + ".out"
			fnamelist = glob.glob(resbase + fmain)
			for filename in fnamelist:
				fcli = filename.split("/")[-1]
				set_hist = getMiddlewareHist(filename, "SET")
				if mgsize > 1:
					mget_hist = getMiddlewareHist(filename, "MGET")
				else:
					mget_hist = getMiddlewareHist(filename, "GET")
				mw_rep_sethist.append(set_hist)
				mw_rep_mgethist.append(mget_hist)
			mw_mgsize_sethist.append(combineMiddlewareHists(mw_rep_sethist))
			mw_mgsize_mgethist.append(combineMiddlewareHists(mw_rep_mgethist))

		if mgsize == 6 and op_type == "set":
			print "Non-zero cut percentages: "
			temp1 = aggregateHists(cli_mgsize_sethist, cutTime)
			temp2 = aggregateHists(mw_mgsize_sethist, cutTime)
			drawHist(temp1[1], temp1[4], subtitle=("clients", mgsize, mgshrd, "set"), out_format=out_format, maxy=histmaxy)
			drawHist(temp2[1], temp2[4], subtitle=("middlewares", mgsize, mgshrd, "set"), out_format=out_format, maxy=histmaxy)
			# drawHist(temp1[1], temp1[2], temp1[3], subtitle=("clients", mgsize, mgshrd, "set"), out_format=out_format, maxy=histmaxy)
			# drawHist(temp2[1], temp2[2], temp2[3], subtitle=("middlewares", mgsize, mgshrd, "set"), out_format=out_format, maxy=histmaxy)
			# drawHist2(temp1[1], temp1[2], temp2[1], temp2[2], temp1[3], temp2[3], subtitle=(mgsize, mgshrd, "mget"), out_format=out_format, maxy=histmaxy)
			print " "

		if mgsize == 6 and op_type == "mget":
			print "Non-zero cut percentages: "
			temp1 = aggregateHists(cli_mgsize_mgethist, cutTime)
			temp2 = aggregateHists(mw_mgsize_mgethist, cutTime)
			drawHist(temp1[1], temp1[4], subtitle=("clients", mgsize, mgshrd, "mget"), out_format=out_format, maxy=histmaxy)
			drawHist(temp2[1], temp2[4], subtitle=("middlewares", mgsize, mgshrd, "mget"), out_format=out_format, maxy=histmaxy)
			# drawHist(temp1[1], temp1[2], temp1[3], subtitle=("clients", mgsize, mgshrd, "mget"), out_format=out_format, maxy=histmaxy)
			# drawHist(temp2[1], temp2[2], temp2[3], subtitle=("middlewares", mgsize, mgshrd, "mget"), out_format=out_format, maxy=histmaxy)
			# drawHist2(temp1[1], temp1[2], temp2[1], temp2[2], temp1[3], temp2[3], subtitle=(mgsize, mgshrd, "mget"), out_format=out_format, maxy=histmaxy)
			print " "

		percDict[mgshrd + "-set-" + str(mgsize) + "-avg"] = np.average(np.vstack(cli_mgsize_setperc), 0)
		percDict[mgshrd + "-set-" + str(mgsize) + "-std"] = np.std(np.vstack(cli_mgsize_setperc), 0)
		percDict[mgshrd + "-mget-" + str(mgsize) + "-avg"] = np.average(np.vstack(cli_mgsize_mgetperc), 0)
		percDict[mgshrd + "-mget-" + str(mgsize) + "-std"] = np.std(np.vstack(cli_mgsize_mgetperc), 0)

	return percDict

def makePlot(plot_list, plot_maxy, plot_file, title, subtitle):
	mgshrdLabelList = ["Sharded", "Non-sharded"]
	mticks = np.arange(len(mlist))
	y, yerr, label = plot_list[0]
	bar = plt.bar(mticks-0.20, y, yerr=yerr, align='center', width=0.40, color=(0.2, 0.8, 0.2), capsize=7, label=mgshrdLabelList[0])
	y, yerr, label = plot_list[1]
	bar = plt.bar(mticks+0.20, y, yerr=yerr, align='center', width=0.40, color=(0.8, 0.2, 0.2), capsize=7, label=mgshrdLabelList[1])

	plt.ylabel(label) # just here if need be: μ
	plt.xlabel("Number of keys")
	plt.figtext(.5,.94,title + " versus number of keys", fontsize=16, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mticks, mlist)
	plt.ylim((0,plot_maxy*1.3))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		if keys == "extra":
			plt.savefig("./out/plot/gmg-extra-" + plot_file)
		else:
			plt.savefig("./out/plot/gmg-" + plot_file)
		plt.clf()

def plotPercentiles(percDict, op_type, mgshrd, out_format, ystep, ymax=None):
	global mlist

	avgs = []
	stds = []
	for mgsize in mlist:
		key = mgshrd + "-" + op_type + "-" + str(mgsize) + "-avg"
		avgs.append(percDict[key])
		key = mgshrd + "-" + op_type + "-" + str(mgsize) + "-std"
		stds.append(percDict[key])
	avgs = np.vstack(avgs).T
	stds = np.vstack(stds).T
	plist = ["25th", "50th", "75th", "90th", "99th"]

	if ymax is None:
		plot_maxy = np.max(avgs)*1.3
	else:
		plot_maxy = ymax

	colorlist = [
		(57,106,177),
		(218,124,48),
		(62,150,81),
		(204,37,41),
		(83,81,84)]
	for i,x in enumerate(colorlist):
		colorlist[i] = x[0]/255.0, x[1]/255.0, x[2]/255.0

	mticks = np.arange(len(mlist))
	width = 0.15
	bar = plt.bar(mticks-2*width, avgs[0], yerr=stds[0], align='center', width=width, color=colorlist[0], capsize=3, label=plist[0])
	bar = plt.bar(mticks-width, avgs[1], yerr=stds[1], align='center', width=width, color=colorlist[1], capsize=3, label=plist[1])
	bar = plt.bar(mticks, avgs[2], yerr=stds[2], align='center', width=width, color=colorlist[2], capsize=3, label=plist[2])
	bar = plt.bar(mticks+width, avgs[3], yerr=stds[3], align='center', width=width, color=colorlist[3], capsize=3, label=plist[3])
	bar = plt.bar(mticks+2*width, avgs[4], yerr=stds[4], align='center', width=width, color=colorlist[4], capsize=3, label=plist[4])

	plt.ylabel("Latency (msec)")
	plt.xlabel("Number of keys")
	plt.figtext(.5,.94,"Response time percentiles" + " versus number of keys", fontsize=16, ha='center')
	plt.figtext(.5,.90,"Sharded gets: " + mgshrd + ", " +  op_type + " operations", fontsize=12, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(mticks, mlist)
	plt.yticks(np.arange(0,plot_maxy,ystep))
	plt.ylim((0,plot_maxy))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		if keys == "extra":
			plt.savefig("./out/plot/gmg-extra-perc-" + op_type + "-" + mgshrd + ".png")
		else:
			plt.savefig("./out/plot/gmg-perc-" + op_type + "-" + mgshrd + ".png")
		plt.clf()

def printSummary(title, plot_list, mgshrdList, mlist):
	t = "\t"
	print title
	for i in range(0, len(mgshrdList)):
		if mgshrdList[i] == "true":
			print "Sharded"
		else:
			print "Non-sharded"
		x = plot_list[i]
		for j in range(0, len(mlist)):
			print (str(mlist[j]) + " keys" +t+ "%.3f" % (x[0][j]) +" ± "+ "%.3f" % (x[1][j])).encode('utf-8')
	print " "

percDict = {}
for mgshrd in mgshrdList:
	data = dataFromFiles(mgshrd)
	prepForPlot(data)
	percDict = prepHistograms(percDict, mgshrd, op_type, ymax_hist, hist_cuttime)

plotPercentiles(percDict, op_type, "true", out_format, ystep, ymax=ymax_perc)
plotPercentiles(percDict, op_type, "false", out_format, ystep, ymax=ymax_perc)

tpttitle = "Throughput"
lattitle = "Latency"
qlentitle = "Queue length"
qtimetitle = "Queue time"
wtimetitle = "Waiting time"
nitemstitle = "Number of query items"
subtitle = 'Gets and multi-gets exp., ' + op_type + ' operations'

cli_nitems_plot = []
for x in cli_tpt_plot:
	cli_nitems_plot.append((np.multiply(x[0], mlist), np.multiply(x[1], mlist), x[2]))

cli_nitems_maxy = np.max(  [np.max(cli_nitems_plot[0][0]), np.max(cli_nitems_plot[1][0])]  )

if(1):
	# Client latency
	makePlot(cli_lat_plot, cli_lat_maxy, op_type + "-lat_cli.png", lattitle, subtitle + ', measured on clients')
	# Client throughput
	makePlot(cli_tpt_plot, cli_tpt_maxy, op_type + "-tpt_cli.png", tpttitle, subtitle + ', measured on clients')
	# Client num_items
	makePlot(cli_nitems_plot, cli_nitems_maxy, op_type + "-nitems_cli.png", nitemstitle, subtitle + ', measured on clients')
	# Middleware latency
	makePlot(mw_lat_plot, mw_lat_maxy, op_type + "-lat_mw.png", lattitle, subtitle + ', measured on middlewares')
	# Middleware throughput
	makePlot(mw_tpt_plot, mw_tpt_maxy, op_type + "-tpt_mw.png", tpttitle, subtitle + ', measured on middlewares')
	# Middleware qlen
	makePlot(mw_qlen_plot, mw_qlen_maxy, "qlen_mw.png", qlentitle, subtitle + ', measured on middlewares')
	# Middleware qtime
	makePlot(mw_qtime_plot, mw_qtime_maxy, op_type + "-qtime_mw.png", qtimetitle, subtitle + ', measured on middlewares')
	# Middleware wtime
	makePlot(mw_wtime_plot, mw_wtime_maxy, op_type + "-wtime_mw.png", wtimetitle, subtitle + ', measured on middlewares')

printSummary("Client latency", cli_lat_plot, mgshrdList, mlist)
printSummary("Client throughput", cli_tpt_plot, mgshrdList, mlist)
printSummary("Client num_items", cli_nitems_plot, mgshrdList, mlist)
printSummary("Middleware latency", mw_lat_plot, mgshrdList, mlist)
printSummary("Middleware throughput", mw_tpt_plot, mgshrdList, mlist)
printSummary("Middleware qlen", mw_qlen_plot, mgshrdList, mlist)
printSummary("Middleware qtime", mw_qtime_plot, mgshrdList, mlist)
printSummary("Middleware wtime", mw_wtime_plot, mgshrdList, mlist)