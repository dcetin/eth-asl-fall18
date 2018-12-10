import numpy as np

def pSmallerthanN(rho, n):
	if n == 0:
		return pn(rho, n)
	return pn(rho, n) + pSmallerthanN(rho, n-1)

def pMorethanN(rho, n):
	return pow(rho, n)

def pn(rho, n):
	return (1-rho) * pow(rho,n)

def model_mm1(service_rate, arrival_rate, numCli):
	# 1-	Parameters
	print "Number of clients: ", numCli
	print "Arrival rate: ", arrival_rate

	# 2-	Traffic intensity
	rho = arrival_rate / service_rate
	print "Traffic intensity: ", rho

	# 3-	Stability condition
	is_stable = rho < 1.0
	print "Stability condition: ", is_stable

	# 4-	Probability of zero jobs in the system
	p0 = pn(rho, 0)
	print "Probability of zero jobs in the system: ", p0

	# 5-

	# 6-	Mean number of jobs in the system
	mean_jobs = rho / (1-rho)
	print "Mean number of jobs in the system: ", mean_jobs

	# 7-	Variance of number of jobs in the system
	var_jobs = rho / pow(1-rho, 2)
	print "Variance of number of jobs in the system: ", var_jobs

	# 8-

	# 9-	Mean number of jobs in the queue
	mean_jobs_queue = pow(rho, 2) / (1-rho)
	print "Mean number of jobs in the queue: ", mean_jobs_queue

	# 10-	Variance of number of jobs in the queue
	var_jobs_queue = pow(rho, 2)*(1 + rho - pow(rho, 2)) / pow(1-rho, 2)
	print "Variance of number of jobs in the queue: ", var_jobs_queue

	# 11-

	# 12-	Mean response time
	mean_response_time = (1/service_rate) / (1-rho)
	print "Mean response time: ", mean_response_time

	# 13-	Variance of the response time
	var_response_time = (1/pow(service_rate, 2)) / pow(1-rho, 2)
	print "Variance of the response time: ", var_response_time

	# 14-

	# 15-

	# 16-

	# 17-	Mean waiting time
	mean_wait_time = (rho/service_rate) / (1-rho)
	print "Mean waiting time: ", mean_wait_time

	# 18-

	# 19-

	# 20-

	# 21-

	# 22-

	for n in [10, 48, 100, 144, 200]:
		print n, pSmallerthanN(rho, n), pMorethanN(rho, n), pSmallerthanN(rho, n) + pMorethanN(rho, n)

	print " "

# Absolute maximum observed for tpfw with tmw=64 and numCli=288
service_rate = 8284.57377049
avg_tps = {}
avg_tps[16] = [ [4887.2, 48], [5159.3, 288] ]
avg_tps[32] = [ [5206.7, 48], [1046.7, 6  ] ]
avg_tps[64] = [ [5184.4, 48], [8124.1, 144] ]

# Complete analysis
if False:
	for tmw in [16, 32, 64]:
		datalist = avg_tps[tmw]
		for x in datalist:
			print "Number of worker threads: ", tmw
			arrival_rate, numCli = x
			model_mm1(service_rate, arrival_rate, numCli)

print "Number of worker threads: ", 64
model_mm1(service_rate, 8124.1, 144)
# probSmallerOrEqualJobsThanNumCli = pSmallerthanN(rho, numCli+1)
# print "probSmallerOrEqualJobsThanNumCli: ", probSmallerOrEqualJobsThanNumCli