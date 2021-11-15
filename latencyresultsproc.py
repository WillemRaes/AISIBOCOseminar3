import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

tx2log = pd.read_csv('./data/latencylogtx2.csv', names=['topic', 'server_time', 'latency'])
nanolog = pd.read_csv('./data/latencylog.csv',  names=['topic', 'server_time', 'latency'])

tx2group = tx2log.groupby(['topic'])

tx2compute = tx2group.get_group('jetsontx2/latency')
tx2total = tx2group.get_group('jetsontx2/RTlatency')

ax = sns.boxplot(y="latency",  data=nanolog,  palette="Set2", fliersize=3, linewidth=2)
# plt.ylim(0, 50)
plt.xlabel("Latency Distribution Jetson Nano")
plt.ylabel("Latency (ms)")
plt.grid()
plt.savefig('boxplot_nano_latency.pdf')
plt.show()

df_total = pd.concat([nanolog, tx2total],0)
ax = sns.boxplot(x='topic', y="latency",  data=df_total,  palette="Set2", fliersize=3, linewidth=2)
plt.xlabel("Latency Distribution Jetson Nano")
plt.ylabel("Latency (ms)")
plt.grid()
plt.ylim(0, 0.2)
plt.semilogy()
plt.savefig('boxplot_total_latency.pdf')
plt.show()