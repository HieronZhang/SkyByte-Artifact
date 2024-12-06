import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import os, sys, functools

script_program = os.path.abspath(__file__)
script_name = os.path.basename(script_program)
script_dir = os.path.dirname(script_program)

sys.path.append(os.path.dirname(script_dir))
from pyplotter.figure_utils.figure_utils import *
FigurePresets.apply_default_style()

normalize_base = None
normalize_base = "1GB"

# hatch_color = "#78756e"
hatch_color = "white"

color_arr = colors_roller_6
hatch_arr = ["", "-", "/", "\\", "x", ""]

@functools.cache
def should_normalize() -> bool:
  return normalize_base is not None and len(normalize_base) != 0

fig, ax0 = plt.subplots(1, 1, figsize=(14, 2.5))
plt.subplots_adjust(top = 1.02, bottom=0.01, hspace=0.6, wspace=0.20)

data_file = os.path.join(script_dir, f"avg.dat")
# data_file = os.path.join(script_dir, f"max.dat")
output_file = os.path.join(script_dir, "PerfSensitivityDRAM")

bar_width = 0.12
horiz_margin = 0.65
horiz_major_tick = 0.75
try:
  with open(data_file, "r") as f:
    lines = f.read()
except Exception as e:
  print(f"Data file {data_file} not found")
  exit(1)

settings = []
workloads = []
sections = lines.strip().split("\n\n")
settings = [setting.strip() for setting in sections[0].split("|")]
data_array = np.zeros((len(sections) - 1, len(settings)))
settings = settings
x_tick_array = np.zeros((len(sections) - 1, len(settings)))
for section_idx, section in enumerate(sections[1:]):
  lines = section.strip().split("\n")
  workload = lines[0].strip()
  workloads.append(workload)
  data_array[section_idx, :] = np.array([float(data) for data in lines[1].split()])
  x_tick_array[section_idx, :] = section_idx * horiz_major_tick + (np.arange(len(settings)) - (len(settings) - 1) / 2) * bar_width
for j, setting in enumerate(settings):
  if should_normalize():
    base_array = data_array[:, settings.index(normalize_base)]
  else:
    base_array = np.ones(data_array.shape[0])
  ax0.bar(x_tick_array[:, j], data_array[:, j] / base_array, color=color_arr[j], width=bar_width, edgecolor=hatch_color, hatch=hatch_arr[j], label=setting, zorder=3)
  ax0.bar(x_tick_array[:, j], data_array[:, j] / base_array, color="none", width=bar_width, edgecolor="white", linewidth=0.8, zorder=3)
# for x_tick, data in zip(x_tick_array[:, 0], data_array[:, 0]):
#   ax.text(x_tick, 1.05, f"{data:5.2f} kops/s", ha="center", va="bottom", rotation=90, fontsize=10)
ymax = np.max(data_array)

ax0.set_xticks(np.arange(len(workloads)) * horiz_major_tick)
ax0.set_xticklabels([workload.replace("|", "\n") for workload in workloads])
ax0.set_xlim([-horiz_margin * horiz_major_tick, (len(workloads) - 1 + horiz_margin) * horiz_major_tick])
if should_normalize():
  ax0.set_yticks(np.arange(0, 1.2, 0.2))
  ax0.set_ylim([0, 1.3])
else:
  ax0.set_ylim([0, ymax * 1.2])
# ax0.set_ylabel("Normalized\nPerformance", fontsize=20)
if not should_normalize():
  y_label = "Normalized\nExecution Time"
else:
  y_label = "Execution\nTime"
ax0.set_ylabel(y_label, fontsize=20)
# ax0.yaxis.set_label_coords(-0.06, 0.4)
# ax0.hlines(y=1, xmin=ax0.get_xlim()[0], xmax=ax0.get_xlim()[1], colors="grey", linestyles="--")
ax0.yaxis.grid(zorder=0)
ax0.hlines(0, xmin=ax0.get_xlim()[0], xmax=ax0.get_xlim()[1], zorder=9, color='black', linewidth=1)

handles, labels = ax0.get_legend_handles_labels()
legend = ax0.legend(handles, labels, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=6, columnspacing=2.5)

fig.savefig(os.path.join(script_dir, f"{output_file}.png"), bbox_inches='tight')
fig.savefig(os.path.join(script_dir, f"{output_file}.pdf"), bbox_inches='tight')
