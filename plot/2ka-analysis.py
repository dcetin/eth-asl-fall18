# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from summarizer import getAvgClientStat, getMiddlewareStat
import glob
import sys

resbase = "/home/doruk/Desktop/asl/asl-fall18-project/res/"
reps = [1,2,3]
load = sys.argv[1] # e.g. "1:0" or "0:1"
experiment = sys.argv[2] # e.g. "cli_tpt", "cli_lat", "mw_tpt", "mw_lat"
level = int(sys.argv[3]) # e.g. "cli_tpt", "cli_lat", "mw_tpt", "mw_lat"
model_type = sys.argv[4] # e.g. "add" or "mult"

# Returns (cli_tpt, cli_lat, mw_tpt, mw_lat, mw_qtime, mw_wtime, mw_qlen)
def dataFromFiles(nmw, nsvr, tmw, load):
	global resbase
	global reps

	cli_settpt = []
	cli_setlat = []
	mw_settpt = []
	mw_setlat = []
	mw_setqtime = []
	mw_setwtime = []

	cli_gettpt = []
	cli_getlat = []
	mw_gettpt = []
	mw_getlat = []
	mw_getqtime = []
	mw_getwtime = []

	mw_qlen = []

	if nmw == 2:
		fbase = "nsvr=" + str(nsvr) + "/ncli=3/icli=2/tcli=1/vcli=32/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=2/tmw=" + str(tmw) + "/ttime=70/"
	if nmw == 1:
		fbase = "nsvr=" + str(nsvr) + "/ncli=3/icli=1/tcli=2/vcli=32/wrkld=" + load + "/mgshrd=NA/mgsize=NA/nmw=1/tmw=" + str(tmw) + "/ttime=70/"

	for rep in reps:
		# Iterate over output files for this repetition
		if(1):
			cli_rep_settpt = []
			cli_rep_setlat = []
			mw_rep_settpt = []
			mw_rep_setlat = []
			mw_rep_setqtime = []
			mw_rep_setwtime = []

			cli_rep_gettpt = []
			cli_rep_getlat = []
			mw_rep_gettpt = []
			mw_rep_getlat = []
			mw_rep_getqtime = []
			mw_rep_getwtime = []

			mw_rep_qlen = []

			fmain = fbase  + "*rep" + str(rep) + "*.csv"
			fnamelist = glob.glob(resbase + fmain)

			# Iterate over the client files
			for filename in fnamelist:
				fcli = filename.split("/")[-1]
				avgSetThru, avgGetThru, avgSetLat, avgGetLat = getAvgClientStat(filename, 5, 5)
				cli_rep_settpt.append(avgSetThru)
				cli_rep_setlat.append(avgSetLat)
				cli_rep_gettpt.append(avgGetThru)
				cli_rep_getlat.append(avgGetLat)
				if load == "1:0" and avgSetThru == 0:
					print nmw, nsvr, tmw, load, rep, fcli, avgSetThru
				if load == "0:1" and avgGetThru == 0:
					print nmw, nsvr, tmw, load, rep, fcli, avgGetThru
			cli_rep_settpt = np.asarray(cli_rep_settpt)
			cli_rep_setlat = np.asarray(cli_rep_setlat)
			cli_rep_gettpt = np.asarray(cli_rep_gettpt)
			cli_rep_getlat = np.asarray(cli_rep_getlat)

			# Iterate over the middleware files
			fmain = fbase + "mwout*rep" + str(rep) + ".out"
			fnamelist = glob.glob(resbase + fmain)
			for filename in fnamelist:
				fcli = filename.split("/")[-1]
				data = getMiddlewareStat(filename, 5, 5)
				mw_rep_qlen.append(float(data[0]))
				if load == "1:0":
					mw_rep_settpt.append(float(data[4]))
					mw_rep_setlat.append(float(data[7]) + float(data[10]))
					mw_rep_setqtime.append(float(data[7]))
					mw_rep_setwtime.append(float(data[10]))
				if load == "0:1":
					mw_rep_gettpt.append(float(data[5]))
					mw_rep_getlat.append(float(data[8]) + float(data[11]))
					mw_rep_getqtime.append(float(data[8]))
					mw_rep_getwtime.append(float(data[11]))

			mw_rep_qlen = np.asarray(mw_rep_qlen)
			mw_rep_setqtime = np.asarray(mw_rep_setqtime)
			mw_rep_setwtime = np.asarray(mw_rep_setwtime)
			mw_rep_settpt = np.asarray(mw_rep_settpt)
			mw_rep_setlat = np.asarray(mw_rep_setlat)
			mw_rep_getqtime = np.asarray(mw_rep_getqtime)
			mw_rep_getwtime = np.asarray(mw_rep_getwtime)
			mw_rep_gettpt = np.asarray(mw_rep_gettpt)
			mw_rep_getlat = np.asarray(mw_rep_getlat)

		# Repetition aggregation
		if(1):
			if load == "1:0":
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
				# Middleware set details
				weighted_setqtime = np.multiply(mw_rep_settpt, mw_rep_setqtime)
				avg_mw_rep_setqtime = np.divide(np.sum(weighted_setqtime), tot_mw_rep_settpt)
				weighted_setwtime = np.multiply(mw_rep_settpt, mw_rep_setwtime)
				avg_mw_rep_setwtime = np.divide(np.sum(weighted_setwtime), tot_mw_rep_settpt)
				mw_setqtime.append(avg_mw_rep_setqtime)
				mw_setwtime.append(avg_mw_rep_setwtime)
			if load == "0:1":
				# Client get
				tot_cli_rep_gettpt = np.sum(cli_rep_gettpt)
				weighted = np.multiply(cli_rep_gettpt, cli_rep_getlat)
				avg_cli_rep_getlat = np.divide(np.sum(weighted), tot_cli_rep_gettpt)
				cli_gettpt.append(tot_cli_rep_gettpt)
				cli_getlat.append(avg_cli_rep_getlat)
				# Middleware get
				tot_mw_rep_gettpt = np.sum(mw_rep_gettpt)
				weighted = np.multiply(mw_rep_gettpt, mw_rep_getlat)
				avg_mw_rep_getlat = np.divide(np.sum(weighted), tot_mw_rep_gettpt)
				mw_gettpt.append(tot_mw_rep_gettpt)
				mw_getlat.append(avg_mw_rep_getlat)
				# Middleware get details
				weighted_getqtime = np.multiply(mw_rep_gettpt, mw_rep_getqtime)
				avg_mw_rep_getqtime = np.divide(np.sum(weighted_getqtime), tot_mw_rep_gettpt)
				weighted_getwtime = np.multiply(mw_rep_gettpt, mw_rep_getwtime)
				avg_mw_rep_getwtime = np.divide(np.sum(weighted_getwtime), tot_mw_rep_gettpt)
				mw_getqtime.append(avg_mw_rep_getqtime)
				mw_getwtime.append(avg_mw_rep_getwtime)
			# Middleware qlen
			avg_mw_rep_qlen = np.average(mw_rep_qlen) # averages over middlewares
			mw_qlen.append(avg_mw_rep_qlen)
		
	# Convert the lists into numpy arrays
	if(1):
		if load == "1:0":
			cli_settpt = np.asarray(cli_settpt)
			cli_setlat = np.asarray(cli_setlat)
			cli_settpt = cli_settpt.reshape(1,len(reps))
			cli_setlat = cli_setlat.reshape(1,len(reps))
			mw_settpt = np.asarray(mw_settpt)
			mw_setlat = np.asarray(mw_setlat)
			mw_settpt = mw_settpt.reshape(1,len(reps))
			mw_setlat = mw_setlat.reshape(1,len(reps))
			mw_setqtime = np.asarray(mw_setqtime)
			mw_setwtime = np.asarray(mw_setwtime)
			mw_setqtime = mw_setqtime.reshape(1,len(reps))
			mw_setwtime = mw_setwtime.reshape(1,len(reps))
		if load == "0:1":
			cli_gettpt = np.asarray(cli_gettpt)
			cli_getlat = np.asarray(cli_getlat)
			cli_gettpt = cli_gettpt.reshape(1,len(reps))
			cli_getlat = cli_getlat.reshape(1,len(reps))
			mw_gettpt = np.asarray(mw_gettpt)
			mw_getlat = np.asarray(mw_getlat)
			mw_gettpt = mw_gettpt.reshape(1,len(reps))
			mw_getlat = mw_getlat.reshape(1,len(reps))
			mw_getqtime = np.asarray(mw_getqtime)
			mw_getwtime = np.asarray(mw_getwtime)
			mw_getqtime = mw_getqtime.reshape(1,len(reps))
			mw_getwtime = mw_getwtime.reshape(1,len(reps))
		mw_qlen = np.asarray(mw_qlen)
		mw_qlen = mw_qlen.reshape(1,len(reps))


		if load == "1:0":
			cli_tpt = cli_settpt
			cli_lat = cli_setlat
			mw_tpt = mw_settpt
			mw_lat = mw_setlat
			mw_qtime = mw_setqtime
			mw_wtime = mw_setwtime
		if load == "0:1":
			cli_tpt = cli_gettpt
			cli_lat = cli_getlat
			mw_tpt = mw_gettpt
			mw_lat = mw_getlat
			mw_qtime = mw_getqtime
			mw_wtime = mw_getwtime

	return cli_tpt, cli_lat, mw_tpt, mw_lat, mw_qtime, mw_wtime, mw_qlen

y_values = []
for tmw in [8,32]:
	for nsvr in [1,3]:
		for nmw in [1,2]:
				cli_tpt, cli_lat, mw_tpt, mw_lat, mw_qtime, mw_wtime, mw_qlen = dataFromFiles(nmw, nsvr, tmw, load)
				if experiment == "cli_tpt":
					y_val = cli_tpt
				if experiment == "cli_lat":
					y_val = cli_lat
				if experiment == "mw_tpt":
					y_val = mw_tpt
				if experiment == "mw_lat":
					y_val = mw_lat
				print "nmw=" + str(nmw) + ", nsvr=" + str(nsvr) + ", tmw=" + str(tmw), np.average(y_val)
				# print (y_val - np.average(y_val))
				if model_type == "mult":
					y_val = np.log(y_val)
				y_values.append(y_val)
print " "

y_values = np.vstack(y_values)

factors_1 = np.array([
	[1, -1, -1, -1],
    [1, +1, -1, -1],
    [1, -1, +1, -1],
    [1, +1, +1, -1],
    [1, -1, -1, +1],
    [1, +1, -1, +1],
    [1, -1, +1, +1],
    [1, +1, +1, +1]
    ])

factors_2 = np.array([
	[1, -1, -1, -1, +1, +1, +1],
    [1, +1, -1, -1, -1, +1, -1],
    [1, -1, +1, -1, -1, -1, +1],
    [1, +1, +1, -1, +1, -1, -1],
    [1, -1, -1, +1, +1, -1, -1],
    [1, +1, -1, +1, -1, -1, +1],
    [1, -1, +1, +1, -1, +1, -1],
    [1, +1, +1, +1, +1, +1, +1]
    ])

factors_3 = np.array([
	[1, -1, -1, -1, +1, +1, +1, -1],
    [1, +1, -1, -1, -1, +1, -1, +1],
    [1, -1, +1, -1, -1, -1, +1, +1],
    [1, +1, +1, -1, +1, -1, -1, -1],
    [1, -1, -1, +1, +1, -1, -1, +1],
    [1, +1, -1, +1, -1, -1, +1, -1],
    [1, -1, +1, +1, -1, +1, -1, -1],
    [1, +1, +1, +1, +1, +1, +1, +1]
    ])

if level == 1:
	x = np.linalg.lstsq(factors_1, y_values)
if level == 2:
	x = np.linalg.lstsq(factors_2, y_values)
if level == 3:
	x = np.linalg.lstsq(factors_3, y_values)

params = np.average(x[0],1)
if level > 0:
	factornames_1 = ["1", "a", "b", "c"]
	q0 = params[0]
	qa = params[1]
	qb = params[2]
	qc = params[3]
if level > 1:
	factornames_2 = ["1", "a", "b", "c", "a*b", "b*c", "a*c"]
	qab = params[4]
	qbc = params[5]
	qac = params[6]
if level > 2:
	factornames_3 = ["1", "a", "b", "c", "a*b", "b*c", "a*c", "a*b*c"]
	qabc = params[7]
print "params:", params
print " "

ssa = pow(2,2)*(qa*qa)
ssb = pow(2,2)*(qb*qb)
ssc = pow(2,2)*(qc*qc)
if level > 1:
	ssab = pow(2,2)*(qab*qab)
	ssbc = pow(2,2)*(qbc*qbc)
	ssac = pow(2,2)*(qac*qac)
if level > 2:
	ssabc = pow(2,2)*(qabc*qabc)

y_avgs =  np.average(y_values,1)
y_errs =  (y_values.T - np.average(y_values,1)).T
err_sq = np.multiply(y_errs, y_errs)
sse = np.sum(err_sq)
print np.average(y_errs)
# num_reps = len(reps)
# dof_sse = pow(2,2)*(num_reps-1)
# mse = sse / dof_sse
# dof_var = 1

if level == 1:
	sst =  ssa + ssb + ssc
if level == 2:
	sst =  ssa + ssb + ssc + ssab + ssbc + ssac
if level == 3:
	sst =  ssa + ssb + ssc + ssab + ssbc + ssac + ssabc
sst += sse

t = "\t"
print "Mean Estimate" +t+ "Sum of Squares" +t+t+		"Variation Explained"
if level > 0:
	print "qa:" +t+ "%.4f" % qa+t+ "ssa:"+t+"%.6f" % ssa+t+			"ssa/sst:"+t+"%.3f" % (ssa/sst)
	print "qb:" +t+ "%.4f" % qb+t+ "ssb:"+t+"%.6f" % ssb+t+			"ssb/sst:"+t+"%.3f" % (ssb/sst)
	print "qc:" +t+ "%.4f" % qc+t+ "ssc:"+t+"%.6f" % ssc+t+			"ssc/sst:"+t+"%.3f" % (ssc/sst)
if level > 1:
	print "qab:" +t+ "%.4f" % qab+t+ "ssab:"+t+"%.6f" % ssab+t+	"ssab/sst:"+t+"%.3f" % (ssab/sst)
	print "qbc:" +t+ "%.4f" % qbc+t+ "ssbc:"+t+"%.6f" % ssbc+t+	"ssbc/sst:"+t+"%.3f" % (ssbc/sst)
	print "qac:" +t+ "%.4f" % qac+t+ "ssac:"+t+"%.6f" % ssac+t+	"ssac/sst:"+t+"%.3f" % (ssac/sst)
if level > 2:
	print "qabc:" +t+ "%.4f" % qabc+t+ "ssabc:"+t+"%.6f" % ssabc+t+	"ssabc/sst:"+t+"%.3f" % (ssabc/sst)
print t+t+ "sse:"+t+"%.6f" % sse+t+			"sse/sst:"+t+"%.3f" % (sse/sst)
print t+t+ "sst:"+t+"%.6f" % sst
print " "

nmwList = [[-1,1],[1,2]]
nsvrList = [[-1,1],[1,3]]
tmwList = [[-1,8],[1,32]]

y_modeled = []
for c, tmw in tmwList:
	for b, nsvr in nsvrList:
		for a, nmw in nmwList:
			factorvalues_1 = [1, a, b, c]
			factorvalues_2 = [1, a, b, c, a*b, b*c, a*c]
			factorvalues_3 = [1, a, b, c, a*b, b*c, a*c, a*b*c]
			if level == 1:
				factorvalues = factorvalues_1
			if level == 2:
				factorvalues = factorvalues_2
			if level == 3:
				factorvalues = factorvalues_3
			y_pred = np.sum(np.multiply(params, factorvalues))
			if model_type == "mult":
				y_pred = np.exp(y_pred)
			print "nmw="+str(nmw)+", nsvr="+str(nsvr)+", tmw="+str(tmw)+": "+str(y_pred)
			y_modeled.append(y_pred)
y_modeled = np.array(y_modeled, dtype='float32')
print " "

if model_type == "mult":
	y_avgs = np.exp(y_avgs)
fit_error = y_avgs - y_modeled
print "Mean absoulte fit error: ", np.average(np.abs(fit_error))
print "Total squared fit error:", np.sum(np.multiply(fit_error, fit_error))
print "Factors a,b,c are nmw,nsvr,tmw."