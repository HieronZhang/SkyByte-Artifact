import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


output_dir = "../../output/"

plt.rc("font", size=11)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=15)
plt.rc("legend", fontsize=18)
plt.rc("hatch", color="white")
mpl.rcParams["axes.labelsize"] = 22
mpl.rcParams["hatch.linewidth"] = 1.8
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family': 'serif'})

# Data
workloads = ["bfs-4", "bc-4", "dlrm-4", "fft-4", "radix-4", "ycsb-4", "tpcc-4"]
benchmark_names = ["bfs-twitter", "bc-twitter", "dlrm-inference", "fft", "radix", "ycsb-nstore", "tpcc-nstore"]
idle_time = [0, 0, 0,0,0,0,0]
busy_time = [0, 0, 0,0,0,0,0]
cs_time = [0, 0, 0,0,0,0,0]


for i in range(len(workloads)):
    data_file = output_dir + workloads[i] + "-" + "assd-Full"
    # print(data_file)
    f = open(data_file, "r")
    lines = f.read()
    # print(lines)
    lines = lines.strip().split("\n")
    find = False
    for line in lines:
        terms = line.split(":")
        if terms[0]=="Total_Cores_Idle_Time":
            idle_time[i] = float(terms[1].strip())
            print(idle_time[i])
        if terms[0]=="Total_Cores_Context_Switch_Time":
            cs_time[i] = float(terms[1].strip())
            print(cs_time[i])
        if terms[0]=="Total_Cores_Busy_Time":
            busy_time[i] = float(terms[1].strip())
            print(busy_time[i])


# Convert the times to percentages
total_time = np.array(idle_time) + np.array(cs_time) + np.array(busy_time)
idle_percent = np.array(idle_time) / total_time * 100
cs_percent = np.array(cs_time) / total_time * 100
busy_percent = np.array(busy_time) / total_time * 100

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.6

# Stacked bar chart
p1 = plt.bar(benchmark_names, busy_percent, width=bar_width, label='Busy Time', color='brown')
p2 = plt.bar(benchmark_names, cs_percent, width=bar_width, bottom=busy_percent, label='Context Switch Time', color='orange')
p3 = plt.bar(benchmark_names, idle_percent, width=bar_width, bottom=busy_percent+cs_percent, label='Idle Time', color='grey')

# Adding labels and title
# plt.xlabel('Benchmark Names')
plt.ylabel('Percentage (%)')
# plt.title('Time Breakdown for Each Benchmark')
plt.legend()

# Rotate x-axis labels
plt.xticks(rotation=45, ha="right")

# Show the plot
plt.show()
extent = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(0.85, 1.45)

x_len, y_len = extent.x1 - extent.x0, extent.y1 - extent.y0

extent.y0 -= y_len * 0.08
extent.y1 -= y_len * 0.11
extent.x0 -= x_len * 0.04
extent.x1 -= x_len * 0.02

fig.savefig(f"output/CPUUtil.png", bbox_inches=extent)
fig.savefig(f"output/CPUUtil.pdf", bbox_inches=extent)
