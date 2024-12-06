# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools
import matplotlib.ticker as mtick

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
normalize_idx = 0

color_arr = colors_dark6

data_file = os.path.join(script_dir, "avg.dat")

# data_file = os.path.join(script_dir, "max.dat")

output_file = os.path.join(script_dir, "PerfContextSwitch")

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
  float(setting_num) for setting_num in measurement_num_array
])
x_tick_label_array = [f"{int(s) // 1000}" for s in measurement_num_array]


x_tick_exp_array = [2000, 10000, 20000, 40000, 60000, 80000]
x_tick_exp_label_array = [f"{int(s) // 1000}" for s in x_tick_exp_array]

from typing import Any, Sequence
def recursive_flatten(base: Sequence, last: Any=None) -> Sequence:
  if base is last:
    return base
  elif not isinstance(base, Sequence):
    return [base]
  print(base)
  return [item for item_arr in base for item in recursive_flatten(item_arr, base)]

fig, axs = plt.subplots(2, 2, figsize=(13, 14))
plt.subplots_adjust(top=0.8, bottom=0.3, hspace=0.3, wspace=0.20)
# axs = recursive_flatten(axs)
axs = axs.flatten()

for workload_idx, workload in enumerate(workloads):
  ax = axs[workload_idx]

  for setting_idx, setting in enumerate(settings):
    assert setting_idx < len(line_styles)
    assert setting_idx < len(color_arr)
    assert setting_idx < len(marker_arr)
    y_arr = data_array[workload_idx, setting_idx, :]
    divisor = 1
    if normalize_idx is not None:
      divisor = y_arr[normalize_idx]
    ax.plot(x_tick_array, y_arr / divisor, linestyle=line_styles[setting_idx], color=color_arr[setting_idx], marker=marker_arr[setting_idx], markerfacecolor="none", label=setting, linewidth=3, markersize=9)

  ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
  ax.grid()
  ax.set_xticks(x_tick_exp_array)
  ax.set_xticklabels(x_tick_exp_label_array)
  ylim = ax.get_ylim()
  ax.set_ylim([ylim[0], ylim[0] + (ylim[1] - ylim[0]) * 1.2])
  # ax.text(ax.get_xlim()[1], 0, r"1e3", fontsize=18)

  label_offset = 0
  if workload_idx % 2 == 0:
    ax.set_ylabel("Normalized\nExecution Time", fontsize=25)
    ax.yaxis.set_label_coords(-0.2, 0.5)
  if workload_idx // 2 == 1:
    ax.set_xlabel(f"Context Switch Trigger\nThreshold ($\mu$s)", fontsize=23)
    label_offset = 0.25

  plt.text(0.5, -0.26 - label_offset, f"({chr(ord('a') + workload_idx)}) {workload}", ha="center", transform=ax.transAxes, fontsize=30)

plt.show()

fig.savefig(os.path.join(script_dir, f"{output_file}.png"), bbox_inches='tight')
fig.savefig(os.path.join(script_dir, f"{output_file}.pdf"), bbox_inches='tight')