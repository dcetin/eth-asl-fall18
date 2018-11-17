# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from summarizer import getAvgClientStat
from summarizer import getMiddlewareStatHist
import glob
import sys

out_format = sys.argv[1] # e.g. "show" or "save"

# resbase="/home/doruk/Desktop/asl/asl-fall18-project/res/test/"
resbase = "/home/doruk/Desktop/asl/asl-fall18-project/res/"

vlist = [1,4,8,16,24,32,48]

vlist = np.asarray(vlist)
tptitle = 'Throughput versus number of clients for 64 worker threads'
lattitle = 'Latency versus number of clients for 64 worker threads'
cliMult = 6
subtitle = 'Consistency test 2 for tpfw and mwb2, same physical machines'
vlist = vlist * cliMult
xticks = vlist

tptlabel = "Throughput (1000 ops/sec)"
latlabel = "Latency (msec)"
# Client plots
if (1):
	# tpfw
	y = [1.04550273, 3.80449727, 5.18798361, 7.44327322, 8.16146448, 8.2233388, 8.28180874]
	yerr = [0.01479104, 0.04084526, 0.05146598, 0.02187991, 0.02519309, 0.01572063, 0.00207989]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="tpfw", marker='o', capsize=2, capthick=1)
	# mwb2
	y = [1.14212568, 4.27407104, 5.60064481, 7.82260656, 8.34472678, 8.42131694, 8.43222404]
	yerr = [0.00551857, 0.02368042, 0.02432744, 0.01376546, 0.00908509, 0.01674838, 0.01016441]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="mwb2", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tptitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,8.43*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/consistency-2-tp_cli.png")
		plt.clf()

if (1):
	# tpfw
	y = [5.77484434, 6.43910218, 9.35003412, 12.94902027, 17.67304797, 23.45406892, 34.86433786]
	yerr = [0.06304048, 0.2267549, 0.20353602, 0.07692725, 0.05633633, 0.13494337, 0.04846228]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="tpfw", marker='o', capsize=2, capthick=1)
	# mwb2
	y = [5.25208599, 5.64361541, 8.57786435, 12.28502584, 17.34516934, 22.86304293, 34.21111949]
	yerr = [0.02607809, 0.06455544, 0.0395557, 0.02033671, 0.05096685, 0.01205368, 0.04096703]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="mwb2", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,34.86*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/consistency-2-lat_cli.png")
		plt.clf()

# Middleware plots
if (1):
	# tpfw
	y = [1.04544785, 3.8035623, 5.18782514, 7.44350925, 8.1610951, 8.22179508, 8.28385246]
	yerr = [0.01473773, 0.04008829, 0.05109108, 0.0221418, 0.0249315, 0.01486309, 0.00212665]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="tpfw", marker='o', capsize=2, capthick=1)
	# mwb2
	y = [1.14199339, 4.2739562, 5.60081588, 7.82176794, 8.3447377, 8.42170492, 8.43216393]
	yerr = [0.00537342, 0.02474875, 0.02467159, 0.01152628, 0.00917766, 0.01681492, 0.00983919]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="mwb2", marker='o', capsize=2, capthick=1)

	plt.ylabel(tptlabel)
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,tptitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,8.43*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/consistency-2-tp_mw.png")
		plt.clf()

if (1):
	# tpfw
	y = [3.71477596, 4.339865, 7.25867283, 11.18071471, 15.72534505, 21.20200357, 32.49780026]
	yerr = [0.0731543, 0.19480009, 0.02098795, 0.06367567, 0.05952149, 0.08729283, 0.12726476]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="tpfw", marker='o', capsize=2, capthick=1)
	# mwb2
	y = [3.17687716, 3.570259, 6.59419515, 10.58877002, 15.46638996, 20.91113998, 32.30182523]
	yerr = [0.04313666, 0.03289049, 0.04294515, 0.02715571, 0.11655549, 0.12665713, 0.09145182]
	line = plt.errorbar(x=vlist, y=y, yerr=yerr, label="mwb2", marker='o', capsize=2, capthick=1)

	plt.ylabel(latlabel) # just here if need be: μ
	plt.xlabel("Number of clients")
	plt.figtext(.5,.94,lattitle, fontsize=12, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=9, ha='center')
	plt.legend(loc='upper left')
	plt.xticks(vlist)
	plt.ylim((0,32.49*1.2))
	plt.grid(True, axis="both")
	if out_format == "show":
		plt.show()
		plt.clf()
	if out_format == "save":
		plt.savefig("./out/plot/consistency-2-lat_mw.png")
		plt.clf()
