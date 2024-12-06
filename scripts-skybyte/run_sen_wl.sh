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

rm -r ../bin-*
rm ../run_wl_*.sh

baselines=( $baselines_dir/assd-WP.config $baselines_dir/assd-W.config )
workloads=( $workloads_dir/*8.config )
settings=( $settings_dir/write_log/*.config )

cpu_num=8
tty_out="$1"
rm print.txt
touch print.txt


for workload in "${workloads[@]}"; do
  filename="$(basename -- "$workload")"
  workload_name="${filename%.config}"
  for baseline in "${baselines[@]}"; do
    filename="$(basename -- "$baseline")"
    baseline_name="${filename%.config}"

    touch "../run_wl_$workload_name-$baseline_name.sh"

    for setting in "${settings[@]}"; do
      filename="$(basename -- "$setting")"
      setting_name="${filename%.config}"
        # if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
        #   echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
        # else
      cp -r ../bin "../bin-$workload_name-$baseline_name-$setting_name"
      touch run_one.sh
      echo "$emulator -b $baseline -w $workload -t $setting -o $tty_out -p -c 8 -f $workload_name-$baseline_name-$setting_name -d" >> run_one.sh
      echo "$emulator -b $baseline -w $workload -t $setting -o $tty_out -p -c 8 -f $workload_name-$baseline_name-$setting_name" >> run_one.sh
      echo "$emulator -b $baseline -w $workload -t $setting -o $tty_out -p -c 8 -f $workload_name-$baseline_name-$setting_name" >> run_one.sh
      echo "$emulator -b $baseline -w $workload -t $setting -o $tty_out -p -c 8 -f $workload_name-$baseline_name-$setting_name" >> run_one.sh
      chmod +x run_one.sh
      cp run_one.sh "../bin-$workload_name-$baseline_name-$setting_name"
      echo "cd bin-$workload_name-$baseline_name-$setting_name" >> "../run_wl_$workload_name-$baseline_name.sh"
      echo "./run_one.sh" >> "../run_wl_$workload_name-$baseline_name.sh"
      echo "cd ../" >> "../run_wl_$workload_name-$baseline_name.sh"
      echo "bin-$workload_name-$baseline_name-$setting_name" >> print.txt
      rm run_one.sh
      # fi
      cp "trace_configs/$workload_name" "../bin-$workload_name-$baseline_name-$setting_name/trace_file_list"
    done


  done
done

