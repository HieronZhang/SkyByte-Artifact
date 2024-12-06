
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import re
import copy
import os, sys
import subprocess
import argparse
import json
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
settings = ['1:128', '1:64','1:32','1:16','1:8','1:4','1:2']
setting_strings = ["main0_25g-0_25-w0_25", "main0_5g-0_25-w0_25", "main1g-0_25-w0_25", "main2g-0_25-w0_25", "main4g-0_25-w0_25", "main8g-0_25-w0_25", "main16g-0_25-w0_25"]

with open('PageLocalityCDF_benchmark_spec.json','r') as spec:
    benchmark_dir_translation = json.load(spec)
benchmark_names = list(benchmark_dir_translation.keys())
benchmark_display_names = copy.copy(benchmark_names)


# def is_finished(benchName:str, dramSize:int) -> bool:
#     with open(f'dram_sweep_logs/{benchName}.bn.json','r') as infos:
#         data = json.load(infos)
#         return data[str(dramSize)]['miss_rate'] > 0


def read_amp(data_dir_path :str, dram_size_setting_idx : int, is_read_amp : bool, benchName:str):
    def parse_split(ln:str) -> dict:
        ln.strip()
        return {
            'k' : float(ln.split(':')[0]),
            'cnt' : int(ln.split(':')[1])
        }
    def is_numeric(string):
        try:
            float(string)  # Try converting the string to a float
            return True
        except ValueError:
            return False
    # numeric_part = dram_size_setting[:-2]
    # unit = 2**20 if dram_size_setting[-2:] == 'MB' else 2**30
    # ds = int(numeric_part) * unit
    # is_bench_finished = is_finished(benchName,ds) # whether this benchmark has completed
    if is_read_amp:
        data_dir_path = os.path.join('../../output-mar29', data_dir_path + '-' + setting_strings[dram_size_setting_idx] + "_" + "parsed_R_amp.txt")
    else:
        data_dir_path = os.path.join('../../output-mar29', data_dir_path + '-' + setting_strings[dram_size_setting_idx] + "_" + "parsed_W_amp.txt")
    # try:
    tmp = []
    with open(data_dir_path,'r') as ltf:
        for line in ltf:
            if line.find(':') == -1: continue
            if len(line.split(':')) > 0:
                point_dict = parse_split(line)
                # point_dict['fin'] = is_bench_finished
                tmp.append(point_dict)
    return tmp
    # except:
    #     print(f'no such file {data_dir_path}', file=sys.stderr)





def plot_search_trace(lists, bname, ax, color_list,
                      linestyles = ["-.", "--", ":", "-", "-.", 'dashdot', ":"], 
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
            access_ratio = e['k']
            cnt = e['cnt']
            assert(access_ratio not in glst.keys())
            glst[access_ratio] = cnt
        if flag:
            continue
        glst = dict(sorted(glst.items(), key=lambda x:x[0]))
        sorted_data = []
        for val, cnt in glst.items():
            for i in range(cnt):
                sorted_data.append(val)

        cdf = np.arange(1, len(sorted_data) + 1) / float(len(sorted_data))
        
        if len(cdf) > 600000:
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
    # ax.set_xscale("log")
    # ax.set_yscale("log")

    ax.grid(which="major", axis="both", linestyle="-", linewidth=0.5, color="grey", zorder=1)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(title)

    
    # x_labels = np.arange(0, 1.1, 0.25)
    x_labels = [0, 0.25, 0.5, 0.75, 1.0]
    # x_labels = [0.6, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    # x_labels_actual = [1 - x for x in x_labels]
    ax.set_xticks(x_labels)
    ax.set_xticklabels([f"{x * 100:.3g}%" for x in x_labels])
    # ax.set_xlim(1, 0.0005)
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


def plot_RW_amp(is_read_amp: bool):

    fig, (((ax0, ax1), (ax2, ax3))) = plt.subplots(2, 2, figsize=(13, 20))
    plt.subplots_adjust(top=0.3, bottom=0.01, hspace=0.4, wspace=0.4)
    axs = (ax0, ax1, ax2, ax3)

    for bm_idx, bm_name in enumerate(benchmark_names):
        ax = axs[bm_idx]
        lsts = []
        for dram_sz_setting_idx in range(len(settings)):
            # print(f"bm_name: {bm_name}, dram_size: {dram_sz_setting}, translation: {benchmark_dir_translation[bm_name]}, read: {is_read_amp}")
            latency_lst = read_amp(benchmark_dir_translation[bm_name], dram_sz_setting_idx, is_read_amp, bm_name)
            # print(len(latency_lst))
            lsts.append(latency_lst)
        ylabel = 'Ratio of CL accessed' if is_read_amp else 'Ratio of CL written'
        plot_search_trace(lsts, settings, ax, color_list=colors, labels=benchmark_display_names, title=f"({chr(ord('a') + bm_idx)}) {benchmark_display_names[bm_idx]}", ylabel=ylabel)

    fig.suptitle(f'Page Locality {"Read" if is_read_amp else "Write"} CDF', y=0.5, x=0.1)
    handles, labels = ax0.get_legend_handles_labels()
    fig.legend(labels, frameon=False, loc="upper left", ncol=4, handlelength=3.5, handletextpad=0.55, columnspacing=1.8)

    # plt.show()
    

    extent = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(0.85, 1.45)
    x_len, y_len = extent.x1 - extent.x0, extent.y1 - extent.y0
    extent.y0 += y_len * 0.13
    extent.y1 -= y_len * 0.595
    extent.x0 -= x_len * 0.06
    extent.x1 += x_len * 0.02
    # figname = list(net_name_translation.values())[model]
    # fig.savefig(f"OverallPerf{figname}.png", bbox_inches=extent)
    output_dir = 'output_PageLocalityCDF'
    subprocess.run(f'mkdir -p {output_dir}',shell=True)
    fig.savefig(f'{output_dir}/{"READ_page_locality" if is_read_amp else "WRITE_page_locality"}.png', bbox_inches=extent)
    fig.savefig(f'{output_dir}/{"READ_page_locality" if is_read_amp else "WRITE_page_locality"}.pdf', bbox_inches=extent)


plot_RW_amp(True)
plot_RW_amp(False)