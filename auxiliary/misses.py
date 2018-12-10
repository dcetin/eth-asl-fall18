import numpy as np
# mwb1-ro-cli
reps = []
reps.append(np.asarray([969.50, 960.23, 9.27]) + np.asarray([974.87, 965.52, 9.36]) + np.asarray([1019.86, 1010.26, 9.60]))
reps.append(np.asarray([965.35, 956.18, 9.17]) + np.asarray([986.96, 977.43, 9.53]) + np.asarray([1015.52, 1005.92, 9.60]))
reps.append(np.asarray([971.08, 961.78, 9.30]) + np.asarray([990.44, 980.90, 9.54]) + np.asarray([1023.61, 1014.01, 9.60]))
reps = np.vstack(reps)
missRates = np.divide(reps[:,2], reps[:,0])
print "mwb1-ro-cli: " + str(np.average(missRates))
# mwb2-ro-cli
reps = []
reps.append(np.asarray([498.45, 493.65, 4.80]) + np.asarray([563.38, 558.15, 5.23]) + np.asarray([469.95, 465.46, 4.49]) + np.asarray([450.44, 446.12, 4.31]) + np.asarray([473.01, 468.48, 4.53]) + np.asarray([507.11, 502.24, 4.87]))
reps.append(np.asarray([500.36, 495.54, 4.81]) + np.asarray([570.63, 565.32, 5.31]) + np.asarray([460.15, 455.78, 4.37]) + np.asarray([458.03, 453.64, 4.39]) + np.asarray([468.71, 464.23, 4.47]) + np.asarray([509.52, 504.63, 4.89]))
reps.append(np.asarray([496.73, 491.94, 4.79]) + np.asarray([555.92, 550.73, 5.19]) + np.asarray([458.60, 454.22, 4.37]) + np.asarray([458.47, 454.10, 4.37]) + np.asarray([478.47, 473.89, 4.57]) + np.asarray([516.63, 511.66, 4.97]))
reps = np.vstack(reps)
missRates = np.divide(reps[:,2], reps[:,0])
print "mwb2-ro-cli: " + str(np.average(missRates))
# mwb1-ro-mw
missRates = [0.00962831246919, 0.00958564096945, 0.00940735961242]
print "mwb1-ro-mw: " + str(np.average(missRates))
# mwb2-ro-mw
missRates = [0.0092754559267, 0.00937157087257, 0.00930958140649, 0.00937334604974, 0.00945719341045, 0.00940158817207]
print "mwb2-ro-mw: " + str(np.average(missRates))