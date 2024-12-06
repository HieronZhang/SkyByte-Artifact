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

line_styles = ["-.", "--", ":", "-", "-"]
# hatch_color = "#78756e"
hatch_color = "white"
data_scale = 1

x_step = 25
zigzag = True

assert x_step > 0 and x_step <= 100
percent = x_step < 1

color_arr = colors_dark6

data_file = os.path.join(script_dir, "cdf.dat")
output_file = os.path.join(script_dir, "WriteModificationCDF")

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
measurement_percentage = all([
  float(measurement) <= 1 for measurement in measurements
])
measurements_nparr = np.array([float(measurement) for measurement in measurements]) * (100 if measurement_percentage else 1)
append0 = not np.isclose(measurements_nparr[0], 0)
append1 = not np.isclose(measurements_nparr[-1], 100)
if append0:
  measurements_nparr = np.hstack(([0], measurements_nparr))
if append1:
  measurements_nparr = np.hstack((measurements_nparr, [100]))

# fill in data and x_tick
data_array = np.zeros((len(workloads), len(settings), len(measurements)))
for (workload_idx, workload), (setting_idx, setting), (measurement_idx, measurement) in itertools.product(enumerate(workloads), enumerate(settings), enumerate(measurements)):
  data_array[workload_idx, setting_idx, measurement_idx] = data_list[workload][measurement_idx][setting_idx]
del data_list
np.set_printoptions(linewidth=200, formatter={'float_kind':'{:20f}'.format})

assert all([d is not None for d in settings])
x_tick_array = np.arange(0, (1 if percent else 100) + x_step, x_step)
x_tick_label_array = [f"{x_tick * (100 if percent else 1):.0f}%" for x_tick in x_tick_array]

from typing import Any, Sequence
def recursive_flatten(base: Sequence, last: Any=None) -> Sequence:
  if base is last:
    return base
  elif not isinstance(base, Sequence):
    return [base]
  return [item for item_arr in base for item in recursive_flatten(item_arr, base)]

fig, axs = plt.subplots(1, len(workloads), figsize=(27, 10))
plt.subplots_adjust(top=0.3, bottom=0.01, hspace=0.53, wspace=0.25)
# axs = recursive_flatten(axs)
axs = axs.flatten()

for workload_idx, workload in enumerate(workloads):
  ax = axs[workload_idx]

  for setting_idx, setting in enumerate(settings):
    assert setting_idx < len(line_styles)
    assert setting_idx < len(color_arr)
    x_arr = measurements_nparr
    y_arr = data_array[workload_idx, setting_idx, :]
    if append0:
      y_arr = np.hstack(([0], y_arr))
    if append1:
      y_arr = np.hstack((y_arr, [100]))
    if zigzag:
      x_arr = np.hstack([
        x_arr[0], np.vstack([x_arr[1:], x_arr[1:]]).flatten("F")
      ])
      y_arr = np.hstack([
        np.vstack([y_arr[:-1], y_arr[:-1]]).flatten("F"), y_arr[-1]
      ])
    ax.plot(y_arr * 100, x_arr, linestyle=line_styles[setting_idx], color=color_arr[setting_idx], markerfacecolor="none", label=setting, linewidth=2)

  ax.legend(loc="upper right", bbox_to_anchor=(1, 1.7))
  ax.grid()
  ax.set_xticks(x_tick_array)
  ax.set_xticklabels(x_tick_label_array)
  plt.text(0.5, -0.29, f"({chr(ord('a') + workload_idx)}) {workload}", ha="center", transform=ax.transAxes, fontsize=20)

axs[0].set_ylabel("[%] of CL Written")

plt.show()

fig.savefig(os.path.join(script_dir, f"{output_file}.png"), bbox_inches='tight')
fig.savefig(os.path.join(script_dir, f"{output_file}.pdf"), bbox_inches='tight')