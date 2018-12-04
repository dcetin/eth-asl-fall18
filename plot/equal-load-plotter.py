import numpy as np
import matplotlib.pyplot as plt

def makePlot(tps, exp, subtitle, maxy):
	title = "Distribution of requests to servers with " + exp
	tps = tps/10000.0
	y = tps[:,0]
	bar = plt.bar(reps-0.25, y, align='center', width=0.23, color=(0.2, 0.8, 0.2), capsize=10, label="Server 1")
	y = tps[:,1]
	bar = plt.bar(reps, y, align='center', width=0.23, color=(0.2, 0.2, 0.8), capsize=10, label="Server 2")
	y = tps[:,2]
	bar = plt.bar(reps+0.25, y, align='center', width=0.23, color=(0.8, 0.2, 0.2), capsize=10, label="Server 3")

	plt.ylabel("Aggregated throughput (10000 ops)") # just here if need be: μ
	plt.xlabel("Repetitions")
	plt.figtext(.5,.94,title, fontsize=15, ha='center')
	plt.figtext(.5,.90,subtitle, fontsize=11, ha='center')
	plt.legend(loc='lower right')
	plt.xticks(reps)
	plt.ylim((0,maxy))
	plt.grid(True, axis="both")
	plt.show()
	plt.clf()

twok_nmw1_tmw8_ro = np.array([[152174,152133,152182],[154936,154922,154913],[159095,159097,159084]])
twok_nmw1_tmw8_wo = np.array([[186618,186870,186873],[181028,181357,181355],[186705,186948,186950]])
gmg_true_1_to_6 = np.array([[77814,77955,77955],[77933,78088,78096],[78135,78269,78268]])

reps = np.array([1,2,3])

makePlot(twok_nmw1_tmw8_ro, "read-only load", "1 middleware, 8 threads, from 2K experiments", 18)
makePlot(twok_nmw1_tmw8_wo, "write-only load", "1 middleware, 8 threads, from 2K experiments", 21)
makePlot(gmg_true_1_to_6, "sharded get requests", "one of 2 mws, 1:6 workload ratio, from gets and multi-gets experiments", 9)
