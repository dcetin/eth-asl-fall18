def getAvgClientStat(base, fname, warmup, cooldown):

	with open(base + fname) as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	baseIdx = 2 + warmup
	lastIdx = content.index("Full-Test GET Latency") - 1 - cooldown

	totSetThru = 0
	totGetThru = 0
	totSetLat = 0
	totGetLat = 0
	for x in range(baseIdx, lastIdx):
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

