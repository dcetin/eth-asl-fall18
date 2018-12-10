import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 12})

def makePlot(tps, exp, subtitle, maxy, sp, ylabel=False):
	plt.subplot(sp)
	tps = tps/10000.0
	y = tps[:,0]
	bar = plt.bar(reps-0.25, y, align='center', width=0.23, color=(0.2, 0.8, 0.2), capsize=10, label="Server 1")
	y = tps[:,1]
	bar = plt.bar(reps, y, align='center', width=0.23, color=(0.2, 0.2, 0.8), capsize=10, label="Server 2")
	y = tps[:,2]
	bar = plt.bar(reps+0.25, y, align='center', width=0.23, color=(0.8, 0.2, 0.2), capsize=10, label="Server 3")

	if ylabel:
		plt.ylabel("Aggregated throughput (10000 ops)") 
	plt.xlabel("Repetitions")
	plt.title(exp)
	# plt.figtext(.5,.90,subtitle, fontsize=11, ha='center')
	plt.legend(loc='lower right')
	plt.xticks(reps)
	plt.ylim((0,maxy))
	plt.grid(True, axis="both")

twok_nmw1_tmw8_ro = np.array([[152174,152133,152182],[154936,154922,154913],[159095,159097,159084]])
twok_nmw1_tmw8_wo = np.array([[186618,186870,186873],[181028,181357,181355],[186705,186948,186950]])
gmg_true_1_to_6 = np.array([[77814,77955,77955],[77933,78088,78096],[78135,78269,78268]])

reps = np.array([1,2,3])

plt.figure(figsize=(12,5))
plt.figtext(.5,.96,"Distribution of requests to multiple servers under different workloads", fontsize=16, ha='center')

makePlot(twok_nmw1_tmw8_ro, "Read-only load", "1 middleware, 8 threads, from 2K experiments", 18, 131, ylabel=True)
makePlot(twok_nmw1_tmw8_wo, "Write-only load", "1 middleware, 8 threads, from 2K experiments", 21, 132)
makePlot(gmg_true_1_to_6, "Sharded get requests", "one of 2 mws, 1:6 workload ratio, from gets and multi-gets experiments", 9, 133)

plt.show()
plt.clf()
