import numpy as np
import matplotlib.pyplot as plt

def getMiddlewareStatHist(fname, warmup, cooldown):

	# Data header:
	# secs: qlen,thru,msrt,items,nset,nget,nmget,sqt,gqt,mqt,swt,gwt,mwt
	# ids:  0   ,1   ,2   ,3    ,4   ,5   ,6    ,7  ,8  ,9, ,10 ,11 ,12

	with open(fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	baseIdx = content.index("STAT START") + 2 + warmup
	lastIdx = content.index("STAT END") - cooldown
	headerIdx = content.index("STAT START") + 1
	colsize = len(content[headerIdx].split(",")) - 1
	seconds = (lastIdx - baseIdx)
	runsum = np.zeros(colsize,)
	for x in range(baseIdx, lastIdx):
		data = content[x].split(",")
		data = np.asarray(data[1:], dtype="float32")
		runsum += data
	data = runsum / (seconds)

	val = []
	ws = []

	baseIdx = content.index("HIST START") + 2
	lastIdx = content.index("HIST END")
	for x in range(baseIdx, lastIdx):
		temp = content[x].split(" ")
		val.append(temp[0])
		ws.append(temp[1])

	val = np.asarray(val, dtype="int")
	ws = np.asarray(ws, dtype="int")

	return data, val, ws

def getAvgClientStat(fname, warmup, cooldown):

	with open(fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	baseIdx = 2 + warmup
	lastIdx = content.index("Full-Test GET Latency") - 1 - cooldown

	totSetThru = 0
	totGetThru = 0
	totSetLat = 0
	totGetLat = 0
	for x in range(baseIdx, lastIdx):
		# print content[x]
		data = content[x].split(",")
		totSetThru += float(data[1])
		totSetLat += float(data[2])
		totGetThru += float(data[4])
		totGetLat += float(data[5])

	seconds = (lastIdx - baseIdx)

	avgSetThru = totSetThru / seconds
	avgGetThru = totGetThru / seconds
	avgSetLat = totSetLat / seconds
	avgGetLat = totGetLat / seconds

	return avgSetThru, avgGetThru, avgSetLat, avgGetLat

def getClientOut(fname):

	with open(fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	setdata = content[9].split()
	getdata = content[10].split()
	avgSetThru = float(setdata[1])
	avgGetThru = float(getdata[1])
	avgSetLat = float(setdata[4])
	avgGetLat = float(getdata[4])

	return avgSetThru, avgGetThru, avgSetLat, avgGetLat

def getMiddlewareStat(fname, warmup, cooldown):

	# Data header:
	# secs: qlen,thru,msrt,items,nset,nget,nmget,sqt,gqt,mqt,swt,gwt,mwt
	# ids:  0   ,1   ,2   ,3    ,4   ,5   ,6    ,7  ,8  ,9, ,10 ,11 ,12

	with open(fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	baseIdx = content.index("STAT START") + 2 + warmup
	lastIdx = content.index("STAT END") - cooldown
	headerIdx = content.index("STAT START") + 1
	colsize = len(content[headerIdx].split(",")) - 1
	seconds = (lastIdx - baseIdx)
	runsum = np.zeros(colsize,)
	for x in range(baseIdx, lastIdx):
		data = content[x].split(",")
		data = np.asarray(data[1:], dtype="float32")
		runsum += data
	data = runsum / (seconds)

	return data

def getMiddlewareHist(fname, htype):

	with open(fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	val = []
	ws = []

	baseIdx = content.index(htype + " HIST START") + 2
	lastIdx = content.index(htype + " HIST END")
	for x in range(baseIdx, lastIdx):
		temp = content[x].split(" ")
		val.append(temp[0])
		ws.append(temp[1])

	val = np.asarray(val, dtype="int")
	ws = np.asarray(ws, dtype="int")

	return val, ws

def drawHist(times, counts, errs=None, title='Response time histogram', subtitle='', out_format="save", maxy=None):
	if subtitle != '':
		mgsize, mgshrd, op_type = subtitle
		subtitle = str(mgsize) + " keys, sharded read: " + mgshrd + ", set"


	n = times.shape[0]
	times = times / 10.0

	tot = float(np.sum(counts))

	end = n
	begin = 0
	x = times[begin:end]
	y = counts[begin:end]

	# plt.hist(x, weights=y, bins=end-begin)
	if errs is None:
		plt.bar(x, width=0.1,height=y, align="edge")
	else:
		plt.bar(x, width=0.1,height=y, yerr=errs, align="edge")
	plt.xlim(min(x),max(x)+0.1)
	plt.figtext(.5,.94,title, fontsize=14, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.grid(True)
	plt.xlabel('Latency (ms)')
	plt.ylabel('Count')
	if maxy:
		plt.ylim((0,maxy))
	plt.xticks(np.arange(min(x), max(x)+1, 1))

	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/gmg-hist" + str(mgsize) + "-" + mgshrd + "-" + op_type + ".png")
		plt.clf()

def combineMiddlewareHists(histList):
	values0, weights0 = histList[0]
	values1, weights1 = histList[1]
	if values0.shape[0] > values1.shape[0]:
		long_values, long_weights = values0, weights0
		short_values, short_weights = values1, weights1
	else:
		long_values, long_weights = values1, weights1
		short_values, short_weights = values0, weights0

	long_weights[short_values] = long_weights[short_values] + short_weights
	return long_values, long_weights

def aggregateMiddlewareHists(histList, commonCutIdx=None):

	if commonCutIdx is None:
		# Find the best cut index automatically
		cutList = []
		for i, (val, ws) in enumerate(histList):
			# Construct the cdf
			cdf = np.cumsum(ws) / np.sum(ws, dtype='float32')
			# Index where the 0.995 of the data resides
			cutidx = np.argmax(cdf > 0.995)
			# Shift the index just after a millisecond
			cutidx = cutidx - (val[cutidx] - 10*(val[cutidx]/10))
			cutList.append(cutidx)

		commonCutIdx = np.min(cutList)

	for i, (val, ws) in enumerate(histList):
		# New weights correct except the last bin
		new_weights = ws[:commonCutIdx+1]
		# Aggregate the outlier weights
		new_weights[commonCutIdx] = np.sum(ws[commonCutIdx+1:])
		# Set the new values
		new_values = val[:commonCutIdx+1]
		histList[i] = (new_values, new_weights)

	wss = []
	for val, ws in histList:
		wss.append(ws)
	wss = np.vstack(wss)
	avg = np.average(wss,0)
	err = np.std(wss, 0)
	return commonCutIdx, val, avg, err