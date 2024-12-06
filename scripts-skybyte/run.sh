#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
base_dir="$(dirname -- "$script_dir")"
src_dir="$base_dir/src"
configs_dir="$base_dir/configs"
output_folder="$base_dir/output"

baselines_dir="$configs_dir/baselines"
workloads_dir="$configs_dir/workloads"
settings_dir="$configs_dir/settings"

emulator="./macsim"

mkdir -p "$output_folder"


# make -C "$src_dir" clean
# make -C "$src_dir" -j


baselines=( $baselines_dir/*.config )
workloads=( $workloads_dir/*8.config )
settings=( $settings_dir/*.config )

cpu_num=8
tty_out="/dev/pts/6"

for baseline in "${baselines[@]}"; do
  filename="$(basename -- "$baseline")"
  baseline_name="${filename%.config}"
  for workload in "${workloads[@]}"; do
    filename="$(basename -- "$workload")"
    workload_name="${filename%.config}"
    # for setting in "${settings[@]}"; do
    #   filename="$(basename -- "$setting")"
    #   setting_name="${filename%.config}"
      # if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
      #   echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
      # else
    cp -r ../bin "../bin-$workload_name-$baseline_name"
    touch run_one.sh
    echo "$emulator -b $baseline -w $workload -o $tty_out -p -f $workload_name-$baseline_name -d" >> run_one.sh
    echo "$emulator -b $baseline -w $workload -o $tty_out -p -f $workload_name-$baseline_name" >> run_one.sh
    echo "$emulator -b $baseline -w $workload -o $tty_out -p -f $workload_name-$baseline_name" >> run_one.sh
    chmod +x run_one.sh
    cp run_one.sh "../bin-$workload_name-$baseline_name"
    rm run_one.sh
      # fi
    cp "trace_configs/$workload_name" "../bin-$workload_name-$baseline_name/trace_file_list"
  done
done

