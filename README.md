# SkyByte: Architecting An Efficient Memory-Semantic CXL-based SSD with OS and Hardware Co-design  (Artifact)

In this artifact, we provide the source code of SkyByte's simulation framework and the necessary instructions to reproduce the key performance results in our paper.


## 0. Hardware and Software Dependencies

This artifact can be executed on any x86 machine with at least 32 GB of main memory and at least 128 GB of disk space. We highly recommend running the artifact on a workstation with multiple powerful CPU cores and at least 64 GB main memory. The artifact needs a Linux environment (preferably Ubuntu 20.04+) and a compiler that supports the C++11 standard.


## 1. Installation

### 1.1 Downloading the Repository

Use the following command to download the artifact:
```
# TODO (Zenodo)
git clone git@github.com:HieronZhang/SkyByte-Artifact.git
```

### 1.2 Installation

Install the following dependencies (You can also run `pre_req.sh`):
```
sudo apt update
sudo apt-get install libboost-all-dev
sudo apt install scons htop
sudo apt upgrade g++
pip3 install matplotlib networkx pandas PyPDF2 gdown scipy
```

Build the simulator for SkyByte:
```
python3 build.py macsim.config -j NUM_THREADS
```

## 2. Experiment Workflow
This section describes the steps to generate and run the necessasry experiments. We strongly recommend that the reader follow the `scripts-skybyte/README.md` to understand more about each script used in this section.


### 2.1 Preparing the multi-threaded instruction traces

We prepared the instruction traces captured by Intel's PIN tool for the workloads we used in the paper. Download the traces from google drive:

```bash
gdown 1wVEKYsCTQ29tsBiyPfKfTR_CSJvXJF0p
tar -xvf skybyte_new_traces.tar.xz 
```


After uncompressing, make sure to put the ``skybyte_new_traces`` folder and the codebase (the ``SkyByte-Artifact`` folder) in the same directory. 

```bash
the_outer_directory
├── skybyte_new_traces
├── SkyByte-Artifact
└── ...
```

For every set of trace (e.g., the one for `bc` with 16 threads), there are one trace configuration file (`trace.txt`) and several raw trace files (`trace_XX.raw` files). The format of the trace files is the same as Macsim. See section 3.4 of `doc/macsim.pdf` for more details. 

### 2.2 Configuration Files

Under the ``configs`` directory, we have prepared different configuration files for different workloads, design baselines and specific settings (e.g., the context-switch policy). You can refer to ``configs/README.md`` for more details.

### 2.3 Launching A Single Experiment

After compiling the simulation framework, you will find the symbol link ``macsim`` in the ``bin`` directory. Under the ``bin`` directory, the file ``trace_file_list`` is used to specify the location of the instruction trace configuration file (the corresponding `trace.txt`). In this artifact, we will provide scripts to automatically setup the individual experiments (introduced later).

To launch a single experiment, run the following command:

```
cd bin
./macsim -b ../configs/baselines/XX.config -w ../configs/workloads/XX.config (-t ../configs/settings/XX.config) -c {corenum} -o {terminal} -p -f {outputfile_name} (-d) (-r)
```

where the command line arguments are:
```
-b baseline_setting_config_file_name
-w workload_config_filename
-t additional_setting_config_file_name, optional
-c logical_core_num_simulated
-o the_terminal_used_to_print_warmup_logs (e.g. /dev/pts/6)
-p: print detailed runtime information, optional
-f output_file_name
-d: run with infinite host DRAM, optional
-r: output DRAM-only performance results, optional
```

The program will set up corresponding settings (e.g., which design baseline is used), do the warmup, and then replay the instruction traces on multiple simulated CPU cores and the simulated CXL-SSD. The results will be generated in the `output` directory. 


### 2.4 Launching Batched Experiments

To run a large number of experiments at one time, we provide the `scripts-skybyte/run_all.sh` shell script. It can use regular expressions to match multiple config files, and it will automatically spawn different experiments to multiple ``tmux`` windows for parallel execution. 


To run all the experiments conveniently, we provide a shell script, ``artifact_run.sh``, which setup and launches all the needed experiments in a automatic manner. 

```
./artifact_run.sh
```

The variable `MAX_CORES_NUM` in this script is the maximum allowed number of CPU cores used for simulations. Note that user may have to change the `MAX_CORES_NUM` based on their own machine's specification before running the script.

The ``artifact_run.sh`` script will first create multiple ``bin-<workload_name>-<thread_num>-<baseline_name>`` directories for different experiments and setup the corresponding ``trace_file_list`` file under every directory. Under each directory, there will also be a script named ``run_one.sh``, which can be used to run each individual experiment. Then, it will use ``run_all.sh`` to launch parallel experiments. See lines 23-29 of ``artifact_run.sh``:

```
# Setup experiment configurations for figure 2, 3, 4, 14, 15, 16, 17, 18, and Table 3
./run_full.sh
# After running this, you will see a folder named bin-<workload_name>-<thread_num>-<baseline_name> for each experiment
# In each folder, there is a script named run_one.sh, which is used to run the experiment

# Run experiments for figure figure 2, 3, 4, 14, 15, 16, 17, 18, and Table 3 concurrently with multiple cores
./run_all.sh -p "bc|tpcc|srad|radix|ycsb|dlrm|bfs-dense" -dr -j $MAX_CORES_NUM
```


## 3. Evaluation and Expected Results

To evaluate the artifact results, simply run:
```
./artifact_draw_figs.sh
```

This script gathers all the results from the `output` folder, and draws all the needed figures sequentially. A detailed description of each command and the output figures' positions is also included in this script.

We provided the expected result data files and figures in the same directory where the figures will be generated. To verify the results, one can compare the generated figures directly with those in the paper, or compare the data for each figure with the example results we provided.


## 4. Experiment Customization

### 4.1 Custom Simulation Configurations. 

In addition to the provided configurations, users can also customize their own configuration files and evaluate them. We list and describe the knobs that can be used in config files to customize experiments:

1. **promotion_enable**: Whether enabling the adaptive page migration mechanism or not.
2. **write_log_enable**: Whether enabling the CXL-Aware SSD DRAM management or not.
3. **device_triggered_ctx_swt**: Whether enabling the coordinated context switch mechanism or not.
4. **cs_threshold**: The threshold used for the context switch trigger policy. (Unit: ns)
5. **ssd_cache_size_byte**: The size of the SSD DRAM cache. (Unit: Byte)
6. **ssd_cache_way**: The associativity of the SSD DRAM cache.
7. **host_dram_size_byte**: The size of the host main memory. (Unit: Byte)
8. **t_policy**: The thread scheduling policy. (Choose from "RR", "RANDOM" and "FAIRNESS" (CFS))

### 4.2 Capturing Custom Program's Traces

Users can generate their own traces of custom programs on their own machines.  We include a sub-repo called ``macsim-x86trace`` in the artifact. It provides the Intel PIN 3.13 tool and some scripts that can generate both instruction traces and memory warmup traces (our simulation framework will need both) for a custom application. See `macsim-x86trace/README.md` for more details on how to do it. Note that one prerequisite of this is that PIN-3.13 can only run on Ubuntu 18.04.
