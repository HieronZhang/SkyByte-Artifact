#!/bin/bash

# This is an automated script to run the experiments and generate key results in the paper.

# --------------------------------- IMPORTART -------------------------------------------------
# ! Please modify this number based on your machine. 
MAX_CORES_NUM=16
# ---------------------------------------------------------------------------------------------

# Prerequisite: 
# ./pre_req.sh


python3 build.py -c
python3 build.py macsim.config -j "$(nproc)"
cd scripts-skybyte


#-------------------------------- Running Experiments -----------------------------------------------------------------------------------
# Make sure there is no other experiment running in the background (in tmux)
tmux kill-server

# Setup experiment configurations for figure 2, 3, 4, 14, 15, 16, 17, 18, and Table 3
./run_full.sh
# After running this, you will see a folder named bin-<workload_name>-<thread_num>-<baseline_name> for each experiment
# In each folder, there is a script named run_one.sh, which is used to run the experiment

# Run experiments for figure figure 2, 3, 4, 14, 15, 16, 17, 18, and Table 3 concurrently with multiple cores
./run_all.sh -p "bc|tpcc|srad|radix|ycsb" -dr -j $MAX_CORES_NUM
# The time for running this could be long



# Setup experiment configurations for figure 23
./run_new_comparison.sh
# After running this, you will see a folder named bin-<workload_name>-<thread_num>-<baseline_name> for each experiment
# In each folder, there is a script named run_one.sh, which is used to run the experiment

# Run experiments for figure 23 concurrently with multiple cores
./run_all.sh -p "bc|tpcc|srad|radix|ycsb" -dr -j $MAX_CORES_NUM
# The time for running this could be long