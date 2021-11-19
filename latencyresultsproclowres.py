import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

tx2log = pd.read_csv('./data/latencylogtx2-lowres-new.csv', names=['topic', 'server_time', 'latency'])
nanolog = pd.read_csv('./data/latencylognano-lowres.csv',  names=['topic', 'server_time', 'latency'])

tx2log['latency'] = tx2log['latency'] * 1000
nanolog['latency'] = nanolog['latency'] * 1000

tx2group = tx2log.groupby(['topic'])

tx2compute = tx2group.get_group('jetsontx2/latency')
tx2total = tx2group.get_group('jetsontx2/RTlatency')
print("tx2 compute")
print(tx2compute['latency'].quantile([0.5, 0.95]))
print("tx2 total")
print(tx2total['latency'].quantile([0.5, 0.95]))

print("nano total")
print(nanolog['latency'].quantile([0.5, 0.95]))


tx2total['mean'] = np.array((tx2total['latency'] - np.median(tx2total['latency']))).copy()
nanolog['mean'] = np.array(nanolog['latency'] - np.median(nanolog['latency'])).copy()

ax = sns.boxplot(y="latency",  data=nanolog,  palette="Set2", fliersize=3, linewidth=2)
# plt.ylim(0, 50)
plt.xlabel("Latency Distribution Jetson Nano")
plt.ylabel("Latency (ms)")
plt.grid()
plt.savefig('boxplot_nano_latency_lowres.pdf')
plt.show()
ax = sns.boxplot(y="latency",  data=tx2total,  palette="Set2", fliersize=3, linewidth=2)
# plt.ylim(0, 50)
plt.xlabel("Latency Distribution Jetson TX2")
plt.ylabel("Latency (ms)")
plt.grid()
plt.savefig('boxplot_tx2_totallatency_lowres.pdf')
plt.show()


df_total = pd.concat([nanolog, tx2total], 0)

ax = sns.boxplot(x='topic', y="mean",  data=df_total,  palette="Set2", fliersize=3, linewidth=2)
plt.xlabel("Hardware")
plt.ylabel("Latency deviation from median (ms)")
plt.grid()
plt.ylim(-30, 32)
ax.set(xticklabels=["Jetson Nano", "Jetson TX2"])
plt.savefig('boxplot_total_latency_lowres.pdf')
plt.show()

indices = np.linspace(1, 100, 100) / 100.
tx2tot_cdf = tx2total['latency'].quantile(indices)
nanotot_cdf = nanolog['latency'].quantile(indices)

plt.plot(np.array(tx2tot_cdf), indices, label='Jetson-TX2')
# plt.plot(nanotot_cdf, indices, label='Jetson Nano')
plt.xlabel("Latency (ms)")
plt.xlim(150, 500)
plt.ylabel("CDF")
plt.grid()

plt.legend()
plt.savefig('cdf_tx2_total_lowres.pdf')
plt.show()

# plt.plot(tx2tot_cdf, indices, label='Jetson-TX2')
plt.plot(nanotot_cdf, indices, label='Jetson Nano')
plt.grid()
plt.xlabel("Latency (ms)")
plt.ylabel("CDF")
plt.legend()
plt.savefig('cdf_nano_total_lowres.pdf')
plt.show()

tx2_tmp = np.array(np.array(tx2total['latency']) - np.array(tx2compute['latency']))

print(np.percentile(tx2_tmp, [50, 95]))

# sns.violinplot(y="latency",  data=df_total, hue='topic',  palette="Set2", fliersize=3, linewidth=2)
# plt.ylim(0, 250)
# plt.grid()
# plt.show()

# plt.plot(tx2tot_cdf, indices, label='Jetson-TX2')
# plt.plot(nanotot_cdf, indices, label='Jetson Nano')
# plt.grid()
# plt.xlabel("Latency (ms)")
# plt.ylabel("CDF")
# plt.legend()
# plt.xlim(100, 200)
# plt.savefig('cdf_comb_total_lowres.pdf')
# plt.show()