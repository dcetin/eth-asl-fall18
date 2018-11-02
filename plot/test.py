import numpy as np
import matplotlib.pyplot as plt

from summarizer import getMiddlewareStatHist

data, times, counts = getMiddlewareStatHist("./mwtestout.txt", 1, 1)
n = times.shape[0]
times = times / 10.0

tot = float(np.sum(counts))

end = n
begin = 0
x = times[begin:end]
y = counts[begin:end]

# plt.hist(x, weights=y, bins=end-begin)
plt.bar(x, width=0.1,height=y, align="edge")
plt.xlim(min(x),max(x)+0.1)
plt.figtext(.5,.94,'Response time histogram', fontsize=14, ha='center')
plt.figtext(.5,.90,'Test run with a single client/server pair', fontsize=9, ha='center')
plt.grid(True)
plt.xlabel('Latency (ms)')
plt.ylabel('Count')
plt.xticks(np.arange(min(x), max(x)+1, 1))
plt.show()