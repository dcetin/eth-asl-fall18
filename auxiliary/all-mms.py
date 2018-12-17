import numpy as np
from math import factorial
import sys

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

def model_mmm(service_rate, arrival_rate, numCli, m):
	rho = arrival_rate / (service_rate*m)
	is_stable = rho < 1.0
	if is_stable:
		prob0 = mmm_p0(rho, m)
		probQ = (pow(m*rho, m) * prob0) / (factorial(m) * (1-rho))
		mean_jobs = m*rho + (rho*probQ)/(1-rho)
		var_jobs = m*rho + rho * probQ * ( ( (1+rho-rho*probQ) / pow(1-rho, 2) ) + m )
		mean_jobs_queue = (rho * probQ) / (1 - rho)
		mean_response_time = (1/service_rate) * (1 + (probQ / ( m * (1-rho))))
		var_response_time = (1 / pow(service_rate, 2)) * ( 1 + (( probQ - 2*probQ ) / (pow(m,2)*pow(1-rho,2))) )
		mean_wait_time = mean_jobs_queue / arrival_rate
		return arrival_rate, rho, mean_jobs, mean_jobs_queue, mean_response_time, mean_wait_time
	return None

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

tmw = 64
modelConfig = "64"
# numCliArr = [6, 24, 48, 96, 192, 288]
# numCliArr = [6, 24, 36, 48, 96, 192, 288]
# numCliArr = [6, 24, 48, 72, 96, 192, 288]
numCliArr = [6, 24, 48, 96, 144, 192, 288]

mmm_service_rate = mmm_service_rate[modelConfig]
print mmm_service_rate
print "\\hline"
for numCli in numCliArr:
	key = str(tmw) + "-" + str(numCli)
	tup = model_mmm(mmm_service_rate, avg_tps[key], numCli, tmw*2)
	if tup != None:
		arrival_rate, rho, mean_jobs, mean_jobs_queue, mean_response_time, mean_wait_time = tup
		resArr = [str(numCli), "%.1f" % arrival_rate, "%.3f" % rho, "%.2f" % mean_jobs, "%.2f" % mean_jobs_queue, "%.2f" % (mean_response_time * 1000), "%.2f" % (mean_wait_time * 1000)]
		print " & ".join(resArr)
		print "\\hline"

# Re-iterate over the probability calculations

