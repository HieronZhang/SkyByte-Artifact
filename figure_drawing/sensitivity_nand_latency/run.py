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

color_arr = colors_roller_11

# data_file = os.path.join(script_dir, "avg.dat")
data_file = os.path.join(script_dir, "max.dat")
output_file = os.path.join(script_dir, "PerfSensitivityNAND")

try:
  with open(data_file, "r") as f:
    lines = f.read()
except Exception as e:
  exit(1)

settings = []
workloads = []
measurements = []
data_list = {}
# get settings, workloads, and measurements name
sections = [section for section in lines.strip().split("\n\n") if len(section.strip()) != 1]
settings = [setting.strip() for setting in sections[0].split("|")]
for expr_grounp in sections[1:]:
  lines = expr_grounp.strip().split("\n")
  workload = lines[0].strip()
  workloads.append(workload)
  measurements_data_list = [
    [
      arr := line.strip().split(),
      " ".join(arr[0:-len(settings)]).strip(),
      [data.strip() for data in arr[-len(settings):]]
    ][-2:]
    for line in lines[1:]
  ]
  measurements = [measurements_data[0] for measurements_data in measurements_data_list]
  data_list[workload] = [measurements_data[1] for measurements_data in measurements_data_list]

# fill in data and x_tick
data_array = np.zeros((len(workloads), len(settings), len(measurements)))
for (workload_idx, workload), (setting_idx, setting), (measurement_idx, measurement) in itertools.product(enumerate(workloads), enumerate(settings), enumerate(measurements)):
  data_array[workload_idx, setting_idx, measurement_idx] = data_list[workload][measurement_idx][setting_idx]
del data_list
np.set_printoptions(linewidth=200, formatter={'float_kind':'{:20f}'.format})

measurement_num_array = [
  [
    rmatch := re.search(r"^[^\d]*(\d*\.?\d+)", measurement),
    None if rmatch is None else None if len(rmatch.groups()) == 0 else rmatch.group(0)
  ][-1]
  for measurement in measurements
]
assert all([d is not None for d in settings])
x_tick_array = np.array([
  setting_num
  for setting_num in measurements
])
# x_tick_label_array = [
#   int(round(32 / float(d))) for d in measurement_num_array
# ]
# x_tick_label_array = [
#   rf"$\frac{{1}}{{{d}}}$" if d != 1 else "1" for d in x_tick_label_array
# ]
x_tick_label_array = [
  setting_num
  for setting_num in measurements
]

from typing import Any, Sequence
def recursive_flatten(base: Sequence, last: Any=None) -> Sequence:
  if base is last:
    return base
  elif not isinstance(base, Sequence):
    return [base]
  print(base)
  return [item for item_arr in base for item in recursive_flatten(item_arr, base)]

fig, axs = plt.subplots(1, len(workloads), figsize=(27, 8))
plt.subplots_adjust(top=0.3, bottom=0.01, hspace=0.53, wspace=0.25)
# axs = recursive_flatten(axs)
axs = axs.flatten()

for workload_idx, workload in enumerate(workloads):
  ax = axs[workload_idx]

  for setting_idx, setting in enumerate(settings):
    line_style = line_styles[setting_idx % len(line_styles)]
    color_style = color_arr[setting_idx % len(color_arr)]
    marker_style = marker_arr[setting_idx % len(marker_arr)]
    ax.plot(np.arange(len(x_tick_array)), data_array[workload_idx, setting_idx, :] / data_array[workload_idx, 4, 0], linestyle=line_style, color=color_style, marker=marker_style, markerfacecolor="none", label=setting, linewidth=3, markersize=9)

  # ax.set_xlabel(f"SSD St", fontsize=15)
  ax.grid()
  ax.set_xticks(np.arange(len(x_tick_array)))
  ax.set_xticklabels(x_tick_label_array, fontsize=17)
  ylim = ax.get_ylim()
  ax.set_ylim(ylim[0], (ylim[1] - ylim[0]) * 1.2 + ylim[0])
  plt.text(0.5, -0.28, f"({chr(ord('a') + workload_idx)}) {workload}", ha="center", transform=ax.transAxes, fontsize=24)
  if workload_idx == 6:
    ax.set_yticks(np.arange(0, 14, 5))
    ax.set_ylim(0, 14.8)

plt.legend(ncol=7, loc="upper center", bbox_to_anchor=(-3.25, 1.3), fontsize=20)
axs[0].set_ylabel("Normalized\nExecution Time", fontsize=24)

plt.show()

fig.savefig(os.path.join(script_dir, f"{output_file}.png"), bbox_inches='tight')
fig.savefig(os.path.join(script_dir, f"{output_file}.pdf"), bbox_inches='tight')