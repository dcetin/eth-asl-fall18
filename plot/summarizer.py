import numpy as np

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

def getMiddlewareStatHist(fname, htype):

	# Data header:
	# secs: qlen,thru,msrt,items,nset,nget,nmget,sqt,gqt,mqt,swt,gwt,mwt
	# ids:  0   ,1   ,2   ,3    ,4   ,5   ,6    ,7  ,8  ,9, ,10 ,11 ,12

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