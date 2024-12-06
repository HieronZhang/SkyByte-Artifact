# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools

import os, sys, re

script_program = os.path.abspath(__file__)
script_name = os.path.basename(script_program)
script_dir = os.path.dirname(script_program)

sys.path.append(os.path.dirname(script_dir))
from pyplotter.figure_utils.figure_utils import *
FigurePresets.apply_default_style()

marker_arr = ["s", "o", "x", "^"]
line_styles = ["-.", "--", ":", "-"]
# hatch_color = "#78756e"
hatch_color = "white"
data_scale = 1

color_arr = colors_roller_12


dict_json = [
    {
        "Category": "H-R/W",
        "bc": "98.6",
        "bfs-dense": "83.5",
        "dlrm": "65.9",
        "radix": "82.3",
        "srad": "50.0",
        "tpcc": "60.8",
        "ycsb": "78.9"
    },
    {
        "Category": "S-R-H",
        "bc": "0.9",
        "bfs-dense": "10.7",
        "dlrm": "23.5",
        "radix": "10.3",
        "srad": "6.1",
        "tpcc": "3.3",
        "ycsb": "18.6"
    },
    {
        "Category": "S-R-M",
        "bc": "0.1",
        "bfs-dense": "3.5",
        "dlrm": "4.0",
        "radix": "1.5",
        "srad": "0.9",
        "tpcc": "0.9",
        "ycsb": "2.5"
    },
    {
        "Category": "S-W",
        "bc": "0.4",
        "bfs-dense": "2.3",
        "dlrm": "6.6",
        "radix": "5.9",
        "srad": "43.0",
        "tpcc": "35.0",
        "ycsb": "0.02"
    }
]

settings = ["H-R/W", "S-R-H", "S-R-M", "S-W"]
workloads = ["bc", "bfs-dense", "dlrm", "radix", "srad", "tpcc", "ycsb"]
data = []
for workload in workloads:
  data.append([float(dict_json[i][workload]) for i in range(len(dict_json))])

print(data)

results = {}

for workload_idx, workload in enumerate(workloads):
  results[workload] = data[workload_idx]
  
print(results)
  



fig, axs = plt.subplots(1, len(workloads), figsize=(40, 3))
# plt.subplots_adjust(top=0.3, bottom=0.01, hspace=0.53, wspace=0.25)
# axs = recursive_flatten(axs)
axs = axs.flatten()

for workload_idx, workload in enumerate(workloads):
  ax = axs[workload_idx]

  for setting_idx, setting in enumerate(settings):
    line_style = line_styles[setting_idx % len(line_styles)]
    color_style = color_arr[setting_idx % len(color_arr)]
    marker_style = marker_arr[setting_idx % len(marker_arr)]
    wedges, texts= ax.pie(data[workload_idx], colors=color_arr)
    # ax.set_title(workload, fontsize=24)
    # plt.setp(autotexts, size=12, weight="bold")
    bbox_props = dict(boxstyle="square,pad=0.4", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(str(data[workload_idx][i])+"%", xy=(x, y), xytext=(1.2*np.sign(x), 1.2*y),
                    horizontalalignment=horizontalalignment, **kw, fontsize=20)
    
# axs[len(axs)-1].legend(ncol=4, settings, title=workload, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=20)

    ax.set_xlabel(workload, fontsize=22)
#   ax.grid()
#   ax.set_xticks(np.arange(len(x_tick_array)))
#   ax.set_xticklabels(x_tick_label_array, fontsize=17)
#   ylim = ax.get_ylim()
#   ax.set_ylim(ylim[0], (ylim[1] - ylim[0]) * 1.2 + ylim[0])
#   plt.text(0.5, -0.28, f"({chr(ord('a') + workload_idx)}) {workload}", ha="center", transform=ax.transAxes, fontsize=24)
#   if workload_idx == 6:
#     ax.set_yticks(np.arange(0, 14, 5))
#     ax.set_ylim(0, 14.8)

plt.legend(settings, ncol=7, loc="upper center", bbox_to_anchor=(-3.1, 1.22), fontsize=20)

plt.show()

fig.savefig(os.path.join(script_dir, f"output.png"), bbox_inches='tight')
fig.savefig(os.path.join(script_dir, f"output.pdf"), bbox_inches='tight')









