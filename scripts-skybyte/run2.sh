#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
base_dir="$(dirname -- "$script_dir")"
src_dir="$base_dir/src"
configs_dir="$base_dir/configs"
output_folder="$base_dir/output"

baselines_dir="$configs_dir/baselines"
workloads_dir="$configs_dir/workloads"
settings_dir="$configs_dir/settings"

emulator="$src_dir/main"

mkdir -p "$output_folder"


make -C "$src_dir" clean
make -C "$src_dir" -j


baselines=( $baselines_dir/*.config )
workloads=( $workloads_dir/*4.config )
settings=( $settings_dir/*.config )

cpu_num=4
tty_out="/dev/pts/8"

# for baseline in "${baselines[@]}"; do
#   filename="$(basename -- "$baseline")"
#   baseline_name="${filename%.config}"
#   for workload in "${workloads[@]}"; do
#     filename="$(basename -- "$workload")"
#     workload_name="${filename%.config}"
#     for setting in "${settings[@]}"; do
#       filename="$(basename -- "$setting")"
#       setting_name="${filename%.config}"
#       if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
#         echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
#       else
#         "$emulator" -b "$baseline" -w "$workload" -t "$setting" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-$setting_name"
#         if [ $? -ne 0 ]; then
#           "$emulator" -b "$baseline" -w "$workload" -t "$setting" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-$setting_name"
#         fi
#       fi
#       # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-SLC" -s 1 
#       # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-MLC" -s 2 
#       # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-TLC" -s 3 
#     done
#     "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name"
#   done
# done


baseline="../configs/baselines/baseType3.config"
baseline_name="baseType3"
# for workload in "${workloads[@]}"; do
  workload="../configs/workloads/fft-4.config"
  filename="$(basename -- "$workload")"
  workload_name="${filename%.config}"
  for setting in "${settings[@]}"; do
    filename="$(basename -- "$setting")"
    setting_name="${filename%.config}"
    if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
      echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
    else
      "$emulator" -b "$baseline" -w "$workload" -t "$setting" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-$setting_name"
    fi
    # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-SLC" -s 1 
    # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-MLC" -s 2 
    # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name-TLC" -s 3 
  done
  # "$emulator" -b "$baseline" -w "$workload" -c"$cpu_num" -o "$tty_out" -p -f "$workload_name-$baseline_name"
# done

