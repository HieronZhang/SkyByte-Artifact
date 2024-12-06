
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import re
import copy
import os, sys
import subprocess
import argparse
import json
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from statsFiguresUtil import *
from figureUtils import *

parser = argparse.ArgumentParser()
# parser.add_argument()
colors = colors_roller_2
colors = colors_custom1
colors = colors_roller_6
plt.rc("font", size=11)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=15)
plt.rc("legend", fontsize=18)
plt.rc("hatch", color="white")
mpl.rcParams["axes.labelsize"] = 22
mpl.rcParams["hatch.linewidth"] = 0.5
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family': 'serif'})


output_dir = "../../output-mar29/"

workloads = ["bc-4", "dlrm-4", "radix-4", "ycsb-4"]
# workloads = ["ycsb-4", "tpcc-4"]

workload_names = ["bc-sparse", "dlrm-training", "radix", "ycsb"]
# workload_names = ["ycsb-nstore"]

settings = ["baseType3", "flatflash", "assd-W", "assd-WP", "assd-Full"]
# settings = ["baseType3"]

setting_names = ["BaseType3", "FlatFlash-CXL", "SkyByte-W", "SkyByte-WP", "SkyByte-Full"]


# benchmark_names = ["bfs-Twitter", 'bc-Twitter', 'FFT', 'Radix']
# benchmark_names = ["bfs-v-wm"]
# benchmark_display_names = copy.copy(benchmark_names)
# settings = ["lru", "FlashNeuron", "deepUM", "prefetch_lru"]
# benchmark_dir_translation = {
#     "bfs-Twitter" : 'bfs_twitter_v_RW_sample',
#     'bc-Twitter' : 'bc_twitter_v_RW_sample',
#     'FFT' : 'fft_v_wm_RW_sample',
#     'Radix' : 'radix_v_wm_RW_sample'
# }
# settings = ['256MB','512MB','1GB','2GB']
# with open('PageLocalityCDF_benchmark_spec.json','r') as spec:
#     benchmark_dir_translation = json.load(spec)
# benchmark_names = list(benchmark_dir_translation.keys())
# benchmark_display_names = copy.copy(benchmark_names)


# def is_finished(benchName:str, dramSize:int) -> bool:
#     with open(f'dram_sweep_logs/{benchName}.bn.json','r') as infos:
#         data = json.load(infos)
#         return data[str(dramSize)]['miss_rate'] > 0


def read_ltc_d(data_dir_path :str):
    # def parse_split(ln:str) -> dict:
    #     ln.strip()
    #     return {
    #         'k' : float(ln.split(':')[0]),
    #         'cnt' : int(ln.split(':')[1])
    #     }
    # def is_numeric(string):
    #     try:
    #         float(string)  # Try converting the string to a float
    #         return True
    #     except ValueError:
    #         return False
    # numeric_part = dram_size_setting[:-2]
    # unit = 2**20 if dram_size_setting[-2:] == 'MB' else 2**30
    # ds = int(numeric_part) * unit
    # is_bench_finished = is_finished(benchName,ds) # whether this benchmark has completed
    # if is_read_amp:
    #     data_dir_path = os.path.join('input_PageLocalityCDF', data_dir_path, f'DRAM={ds}_R_amp.txt')
    # else:
    #     data_dir_path = os.path.join('input_PageLocalityCDF', data_dir_path, f'DRAM={ds}_W_amp.txt')
    # try:
    tmp = []
    with open(data_dir_path,'r') as ltf:
        find = False
        timestamp_arr = []
        cnt_arr = []
        for line in ltf:
            if line.find(':') == -1: continue
            terms = line.split(":")
            if terms[0]=="Latency_CDF_Timestamp":
                find = True
                timestamp_arr = [int(item) for item in terms[1].strip().split(' ')]
            if terms[0]=="Latency_CDF_Data":
                cnt_arr = [int(item) for item in terms[1].strip().split(' ')]
        if find:
            for i in range(len(timestamp_arr)-1):
                dict_i = {
                    'data_range' : timestamp_arr[i],
                    'cnt' : cnt_arr[i]
                }
                print(dict_i)
                tmp.append(dict_i)
    return tmp
    # except:
    #     print(f'no such file {data_dir_path}', file=sys.stderr)





def plot_search_trace(lists, bname, ax, color_list,
                      linestyles = ["-.", "--", ":", "-", "-.", 'dashdot'], 
                      labels = [], ylim = None, title = "",
                      bs_list = None, ytick_base = 1, ylabel = ""):
    '''
    color_list[0] for T10, color_list[1:] for baseline_points;
    baseline_points: [poplib (mem, time), roller (mem, time)]
    '''

    ymax = 0
    for idx, lst in enumerate(lists):
        glst = {}
        flag = False
        for e in lst:
            # if e['fin'] == False:
            #     flag = True; break
            timestamp = e['data_range']
            cnt = e['cnt']
            glst[timestamp] = cnt
        if flag:
            continue
        # glst = dict(sorted(glst.items(), key=lambda x:x[0]))
        sorted_data = []
        for val, cnt in glst.items():
            for i in range(cnt):
                sorted_data.append(val)

        cdf = np.arange(1, len(sorted_data) + 1) / float(len(sorted_data))
        
        if len(cdf) > 60000:
            from numpy.random import default_rng
            rng = default_rng()
            max_samples = len(cdf) // 600
            rand_idxs = np.array(sorted(rng.choice(len(cdf), size=max_samples, replace=False)))
            cdf = cdf[rand_idxs]
            sorted_data = np.array(sorted_data)[rand_idxs]
            print(f"IDX: {idx} {len(cdf)}")
        
        ax.plot(cdf, sorted_data, color=color_list[idx], zorder=3, linestyle=linestyles[idx],  linewidth=3, label=bname[idx])
        
        ax.text(1.12, -0.05, "CDF", ha='center', va="bottom", fontsize=12)
    # ax.invert_xaxis()
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.grid(which="major", axis="both", linestyle="-", linewidth=0.5, color="grey", zorder=1)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(title)

    
    # x_labels = np.arange(0, 1.1, 0.25)
    # x_labels = [0, 0.25, 0.5, 0.75, 1.0]
    y_labels = [3000, 10000, 100000, 1000000]
    x_labels = [0.97, 0.99, 0.999, 0.9999, 1]
    # x_labels_actual = [1 - x for x in x_labels]
    ax.set_xticks(x_labels)
    ax.set_yticks(y_labels)
    ax.set_xticklabels([f"{x * 100:.3g}%" for x in x_labels])
    ax.set_ylim(3000, 1000000)
    ax.set_xlim(0.97, 1)
    # # ax.set_xlim(1, 0.0005)
    # ax.set_xlim(0.25, 0)
    # if title.find("ResNet152") != -1:
    #     ax.set_ylim(0.9, ymax / 100)
    # elif title.find("BERT") != -1:
    #     ax.set_ylim(0.9, ymax / 5)
    # elif title.find("SENet") != -1:
    #     ax.set_ylim(0.9, ymax / 90)
    # else:
    #     ax.set_ylim(0.9, ymax * 1.5)
    # ax.legend()


def plot_ltc_cdf(is_read_amp: bool):

    
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2, figsize=(20, 20))
    plt.subplots_adjust(top=0.3, bottom=0.01, hspace=0.9, wspace=0.3)
    axs = (ax0, ax1, ax2, ax3)

    for bm_idx, bm_name in enumerate(workload_names):
        ax = axs[bm_idx]
        lsts = []

        for setting in settings:
            data_file = output_dir + workloads[bm_idx] + "-" + setting
            # print(f"bm_name: {bm_name}, dram_size: {dram_sz_setting}, translation: {benchmark_dir_translation[bm_name]}, read: {is_read_amp}")
            latency_lst = read_ltc_d(data_file)
            # print(len(latency_lst))
            # print(latency_lst)
            lsts.append(latency_lst)
        ylabel = 'Latency (ns)'
        plot_search_trace(lsts, settings, ax, color_list=colors, labels=workload_names, title=f"({chr(ord('a') + bm_idx)}) {workload_names[bm_idx]}", ylabel=ylabel if bm_idx == 0 else "")

    fig.suptitle(f'Latency CDF', y=0.5, x=0.1)
    handles, labels = ax0.get_legend_handles_labels()
    fig.legend(labels, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 0.36), ncol=6, handlelength=3.5, handletextpad=0.55, columnspacing=1.8)

    # plt.show()
    

    extent = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(0.85, 1.45)
    x_len, y_len = extent.x1 - extent.x0, extent.y1 - extent.y0
    extent.y0 += y_len * 0.11
    extent.y1 -= y_len * 0.6
    extent.x0 += x_len * 0.018
    extent.x1 -= x_len * 0.02
    # figname = list(net_name_translation.values())[model]
    # fig.savefig(f"OverallPerf{figname}.png", bbox_inches=extent)
    output_file_dir = 'output'
    subprocess.run(f'mkdir -p {output_file_dir}',shell=True)
    fig.savefig(f'{output_file_dir}/{"LatencyCDF" if is_read_amp else "LatencyCDF"}.png', bbox_inches=extent)
    fig.savefig(f'{output_file_dir}/{"LatencyCDF" if is_read_amp else "LatencyCDF"}.pdf', bbox_inches=extent)


plot_ltc_cdf(True)
# plot_RW_amp(False)