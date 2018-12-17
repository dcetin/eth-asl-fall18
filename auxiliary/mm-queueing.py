import numpy as np
from math import factorial
import sys

tmw = int(sys.argv[1])
numCli = int(sys.argv[2])
modelConfig = sys.argv[3]

# Helper functions for probability calculations
def mm1_pSmallerthanN(rho, n):
	# Smaller than or equal
	if n == 0:
		return mm1_pn(rho, n)
	return mm1_pn(rho, n) + mm1_pSmallerthanN(rho, n-1)

def mm1_pMorethanN(rho, n):
	# Greater than or equal
	return pow(rho, n)

def mm1_pn(rho, n):
	retval = (1-rho) * pow(rho,n)
	return retval

def mmm_pSmallerthanN(rho, m, n):
	# Smaller than or equal
	if n == 0:
		return mmm_p0(rho, m)
	return mmm_pn(rho, m, n) + mmm_pSmallerthanN(rho, m,  n-1)

def mmm_pn(rho, m, n):
	prob0 = mmm_p0(rho, m)
	if n < m:
		return prob0 * (pow(m*rho, n) / factorial(n))
	else:
		return (prob0 * pow(rho, n) * pow(m, m)) / factorial(m)

def mmm_p0(rho, m):
	retval = 1/(1 + pow(m*rho, m) / (factorial(m) * (1-rho)) + np.sum([(pow(m*rho,n)/factorial(n))for n in range(1,m)]))
	return retval

# Modelling functions
def model_mm1(service_rate, arrival_rate, numCli):
	print "M/M/1 Model"
	print " "

	# 1-	Parameters
	print "Number of clients: ", numCli
	print "Arrival rate: ", arrival_rate
	print "Service rate: ", service_rate

	# 2-	Traffic intensity
	rho = arrival_rate / service_rate
	print "Traffic intensity: ", rho

	# 3-	Stability condition
	is_stable = rho < 1.0
	print "Stability condition: ", is_stable

	if is_stable:
		# 4-	Probability of zero jobs in the system
		p0 = mm1_pn(rho, 0)
		print "Probability of zero jobs in the system: ", p0

		# 5-	Probability of n jobs in the system
		# for n in [6, 48, 72, 144, 288]:
		# 	print "Prob. of smaller than", n, "jobs in the system: ", mm1_pSmallerthanN(rho, n-1)

		# 6-	Mean number of jobs in the system
		mean_jobs = rho / (1-rho)
		print "Mean number of jobs in the system: ", mean_jobs

		# 7-	Variance of number of jobs in the system
		var_jobs = rho / pow(1-rho, 2)
		# print "Variance of number of jobs in the system: ", var_jobs

		# 9-	Mean number of jobs in the queue
		mean_jobs_queue = pow(rho, 2) / (1-rho)
		print "Mean number of jobs in the queue: ", mean_jobs_queue

		# 10-	Variance of number of jobs in the queue
		var_jobs_queue = pow(rho, 2)*(1 + rho - pow(rho, 2)) / pow(1-rho, 2)
		# print "Variance of number of jobs in the queue: ", var_jobs_queue

		# 12-	Mean response time
		mean_response_time = (1/service_rate) / (1-rho)
		print "Mean response time: ", mean_response_time

		# 13-	Variance of the response time
		var_response_time = (1/pow(service_rate, 2)) / pow(1-rho, 2)
		# print "Variance of the response time: ", var_response_time

		# 17-	Mean waiting time
		mean_wait_time = (rho/service_rate) / (1-rho)
		print "Mean waiting time: ", mean_wait_time

	print " "

def model_mmm(service_rate, arrival_rate, numCli, m):
	print "M/M/m Model"
	print " "

	# 1-	Parameters
	print "Number of clients: ", numCli
	print "Arrival rate: ", arrival_rate
	print "Service rate: ", service_rate
	print "Number of workers: ", m

	# 2-	Traffic intensity
	rho = arrival_rate / (service_rate*m)
	print "Traffic intensity: ", rho

	# 3-	Stability condition
	is_stable = rho < 1.0
	print "Stability condition: ", is_stable

	if is_stable:
		# 4-	Probability of zero jobs in the system
		prob0 = mmm_p0(rho, m)
		print "Probability of zero jobs in the system: ", prob0

		# 5-	Probability of n jobs in the system
		# for n in [6, 48, 72, 144, 288]:
		# 	print "Prob. of smaller than", n, "jobs in the system: ", mmm_pSmallerthanN(rho, m, n-1)

		# 6-	Probability of queueing
		probQ = (pow(m*rho, m) * prob0) / (factorial(m) * (1-rho))
		# print "Probability of queueing: ", probQ

		# 7-	Mean number of jobs in the system
		mean_jobs = m*rho + (rho*probQ)/(1-rho)
		print "Mean number of jobs in the system: ", mean_jobs

		# 8-	Variance of number of jobs in the system
		var_jobs = m*rho + rho * probQ * ( ( (1+rho-rho*probQ) / pow(1-rho, 2) ) + m )
		# print "Variance of number of jobs in the system: ", var_jobs

		# 9-	Mean number of jobs in the queue
		mean_jobs_queue = (rho * probQ) / (1 - rho)
		print "Mean number of jobs in the queue: ", mean_jobs_queue

		# 13-	Mean response time
		mean_response_time = (1/service_rate) * (1 + (probQ / ( m * (1-rho))))
		print "Mean response time: ", mean_response_time

		# 14-	Variance of the response time
		var_response_time = (1 / pow(service_rate, 2)) * ( 1 + (( probQ - 2*probQ ) / (pow(m,2)*pow(1-rho,2))) )
		# print "Variance of the response time: ", var_response_time

		# 16-	Mean waiting time
		mean_wait_time = mean_jobs_queue / arrival_rate
		print "Mean waiting time: ", mean_wait_time
		print " "
		return arrival_rate, rho, mean_jobs, mean_jobs_queue, mean_response_time, mean_wait_time

	print " "
	return None

if False:
	# avg_tps[tmw-numCli]
	avg_tps = {
		"8-6":		1060.2,
		"8-24":		3492.8,
		"8-48":		3783.9,
		"8-96":		3740.4,
		"8-192":	3737.8,
		"8-288":	3814.9,
		"16-6":		1056.0,
		"16-24":	3824.3,
		"16-36":	4674.3,
		"16-48":	4887.2,
		"16-96":	5092.6,
		"16-192":	5077.0,
		"16-288":	5159.3,
		"32-6":		1046.7,
		"32-24":	3825.5,
		"32-48":	5206.7,
		"32-72":	6412.2,
		"32-96":	6714.9,
		"32-192":	6742.4,
		"32-288":	6776.6,
		"64-6":		1045.5,
		"64-24":	3804.5,
		"64-48":	5188.0,
		"64-96":	7443.3,
		"64-144":	8161.5,
		"64-192":	8223.3,
		"64-288":	8281.8
	}

	mm1_service_rate = {
		"8":  3814.9,
		"16": 5159.3,
		"32": 6776.6,
		"64": 8281.8
	}

	mmm_service_rate = {
		"8":  3814.9 / 16,
		"16": 5159.3 / 32,
		"32": 6776.6 / 64,
		"64": 8281.8 / 128
	}

if True:
	# avg_tps[tmw-numCli]
	avg_tps = {
		"8-6": 1060.2,
		"8-24": 3492.9,
		"8-48": 3783.7,
		"8-96": 3740.3,
		"8-192": 3737.8,
		"8-288": 3814.9,
		"16-6": 1056.0,
		"16-24": 3823.2,
		"16-36": 4673.6,
		"16-48": 4887.3,
		"16-96": 5091.2,
		"16-192": 5077.2,
		"16-288": 5159.4,
		"32-6": 1046.8,
		"32-24": 3823.6,
		"32-48": 5206.5,
		"32-72": 6411.0,
		"32-96": 6715.1,
		"32-192": 6742.6,
		"32-288": 6776.7,
		"64-6": 1045.4,
		"64-24": 3803.6,
		"64-48": 5187.8,
		"64-96": 7443.5,
		"64-144": 8161.1,
		"64-192": 8221.8,
		"64-288": 8283.9
	}

	mm1_service_rate = {
		"8":  3814.9,
		"16": 5159.4,
		"32": 6776.7,
		"64": 8283.9
	}

	mmm_service_rate = {
		"8":  3814.9 / 16,
		"16": 5159.4 / 32,
		"32": 6776.7 / 64,
		"64": 8283.9 / 128
	}

mm1_service_rate = mm1_service_rate[modelConfig]
mmm_service_rate = mmm_service_rate[modelConfig]

key = str(tmw) + "-" + str(numCli)
print "Number of worker threads: ", tmw
print "Number of clients: ", numCli
print "Model based on: ", modelConfig, "thread results"
print " "
model_mm1(mm1_service_rate, avg_tps[key], numCli)
arrival_rate, rho, mean_jobs, mean_jobs_queue, mean_response_time, mean_wait_time = model_mmm(mmm_service_rate, avg_tps[key], numCli, tmw*2)

# Re-iterate over the probability calculations
