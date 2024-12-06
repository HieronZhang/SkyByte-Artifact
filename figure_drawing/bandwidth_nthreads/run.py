# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from matplotlib.ticker import FixedLocator, PercentFormatter

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyplotter.figure_utils.figure_utils import *
import pyplotter.utils.multidim_repr as mdr

from matplotlib.cm import get_cmap
import numpy as np

script_program = os.path.abspath(__file__)
script_name = os.path.basename(script_program)
script_dir = os.path.dirname(script_program)

color_arr = colors_roller_9
# color_arr = colors_test
hatch_color = "white"
hatch_arr = ["..", "//", "\\\\", "xx", ""]
# hatch_arr = ["//", "\\\\", "xx", "+", ""]

# plot font size options
plt.rc("font", size=15)
plt.rc("axes", titlesize=30)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=18)
plt.rc("legend", fontsize=18)
plt.rc("hatch", color="white")
mpl.rcParams["hatch.linewidth"] = 1.8
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family': 'serif'})

output_file = os.path.join(script_dir, "dram-miss-and-flash-latency")

fig, ax = plt.subplots(1, 2, figsize=(14, 3))
plt.subplots_adjust(top = 1.02, bottom=0.01, hspace=0.6, wspace=0.24)
axs = ax.flatten()

with open(os.path.join(script_dir, "mem_request_nr.dat")) as fin:
  lines = fin.read()

sections = [section.strip() for section in lines.split("\n\n")]
settings = [setting.strip() for setting in sections[0].split("|")]
data = [float(data.strip()) for data in sections[1].split()]

ax = axs[0]
ax.tick_params(
    axis='x', which='both', bottom=False, top=False)
x_arr = np.arange(len(settings))
x_tick_arr = settings
y_arr = np.array(data) * 100
ax.bar(x_arr, y_arr, zorder=9, color="#019E73")
y_arr = np.arange(0, 11, 2)
y_tick_arr = [f"{y:.0f}%" for y in y_arr]
ax.set_yticks(y_arr)
ax.set_yticklabels(y_tick_arr)
ax.set_ylabel("Percentage of Flash\nRead Requests", fontsize=20)
ax.set_xticks(x_arr + 0.3)
ax.set_xticklabels(x_tick_arr, fontsize=22, rotation=30, ha="right")
ax.grid(axis='y')
ax.set_ylim([0, 11])

with open(os.path.join(script_dir, "cache_miss_lat.dat")) as fin:
  lines = fin.read()

sections = [section.strip() for section in lines.split("\n\n")]
settings = [setting.strip() for setting in sections[0].split("|")]
data = [float(data.strip()) for data in sections[1].split()]

ax = axs[1]
ax.tick_params(
    axis='x', which='both', bottom=False, top=False)
x_arr = np.arange(len(settings))
x_tick_arr = settings
y_arr = np.array(data) / 1000
ax.bar(x_arr, y_arr, zorder=9, color="#47A4D9")
ax.set_ylabel("Average Flash\nRead Latency ($\mu$s)", fontsize=20)
ax.set_xticks(x_arr + 0.3)
ax.set_xticklabels(x_tick_arr, fontsize=22, rotation=30, ha="right")
ax.grid(axis='y')

pdf = PdfPages(f"{output_file}.pdf")
pdf.savefig(bbox_inches="tight")
pdf.close()