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

rm -r ../bin-*
# make -C "$src_dir" clean
# make -C "$src_dir" -j


baselines=( "$baselines_dir"/assd-W.config "$baselines_dir"/assd-WP.config )
workloads=( "$workloads_dir"/*-8.config  )
# settings=( "$settings_dir"/*.config )

cpu_num=$(nproc)
tty_out="$1"
rm print.txt
touch print.txt
number=0

for baseline in "${baselines[@]}"; do
  filename="$(basename -- "$baseline")"
  baseline_name="${filename%.config}"
  for workload in "${workloads[@]}"; do
    # if [[ $workload =~ ([0-9]+)\.config$ ]]; then
    #     number="${BASH_REMATCH[1]}"
    #     echo "Number extracted from $workload: $number"
    # fi
    filename="$(basename -- "$workload")"
    workload_name="${filename%.config}"
    for i in {1..3}; do
    # for setting in "${settings[@]}"; do
    #   filename="$(basename -- "$setting")"
    #   setting_name="${filename%.config}"
        # if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
        #   echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
        # else
      target_name="bin-$workload_name-$baseline_name-flash$i"
      target_folder="../$target_name"
      cp -r ../bin "$target_folder"
      target_run_script="$target_folder/run_one.sh"
      cat > "$target_run_script" << EOF
#!/bin/bash
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i -d
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
EOF
      chmod +x "$target_run_script"
      echo "$target_name" >> print.txt
      cp "trace_configs/$workload_name" "$target_folder/trace_file_list"
      # cp "param_configs/core$number.in" "$target_folder/params.in"
    done
  done
done



baselines=( "$baselines_dir"/flatflash.config )
workloads=( "$workloads_dir"/*-8.config  )
# settings=( "$settings_dir"/*.config )

cpu_num=$(nproc)

number=0

for baseline in "${baselines[@]}"; do
  filename="$(basename -- "$baseline")"
  baseline_name="${filename%.config}"
  for workload in "${workloads[@]}"; do
    # if [[ $workload =~ ([0-9]+)\.config$ ]]; then
    #     number="${BASH_REMATCH[1]}"
    #     echo "Number extracted from $workload: $number"
    # fi
    filename="$(basename -- "$workload")"
    workload_name="${filename%.config}"
    for i in {1..3}; do
    # for setting in "${settings[@]}"; do
    #   filename="$(basename -- "$setting")"
    #   setting_name="${filename%.config}"
        # if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
        #   echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
        # else
      target_name="bin-$workload_name-$baseline_name-flash$i"
      target_folder="../$target_name"
      cp -r ../bin "$target_folder"
      target_run_script="$target_folder/run_one.sh"
      cat > "$target_run_script" << EOF
#!/bin/bash
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i -d
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
EOF
      chmod +x "$target_run_script"
      echo "$target_name" >> print.txt
      cp "trace_configs/$workload_name" "$target_folder/trace_file_list"
      # cp "param_configs/core$number.in" "$target_folder/params.in"
    done
  done
done




baselines=( "$baselines_dir"/assd-Full-rr.config )
workloads=( "$workloads_dir"/*24.config "$workloads_dir"/*32.config "$workloads_dir"/*16.config)
# settings=( "$settings_dir"/*.config )

cpu_num=$(nproc)

number=0

for baseline in "${baselines[@]}"; do
  filename="$(basename -- "$baseline")"
  baseline_name="${filename%.config}"
  for workload in "${workloads[@]}"; do
    # if [[ $workload =~ ([0-9]+)\.config$ ]]; then
    #     number="${BASH_REMATCH[1]}"
    #     echo "Number extracted from $workload: $number"
    # fi
    filename="$(basename -- "$workload")"
    workload_name="${filename%.config}"
    for i in {1..3}; do
    # for setting in "${settings[@]}"; do
    #   filename="$(basename -- "$setting")"
    #   setting_name="${filename%.config}"
        # if [ -e "$output_folder/$workload_name-$baseline_name-$setting_name" ]; then
        #   echo "$output_folder/$workload_name-$baseline_name-$setting_name already exists!"
        # else
      target_name="bin-$workload_name-$baseline_name-flash$i"
      target_folder="../$target_name"
      cp -r ../bin "$target_folder"
      target_run_script="$target_folder/run_one.sh"
      cat > "$target_run_script" << EOF
#!/bin/bash
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i -d
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
$emulator -b $baseline -w $workload -o $tty_out -p -c 8 -s $i -f $workload_name-$baseline_name-flash$i
EOF
      chmod +x "$target_run_script"
      echo "$target_name" >> print.txt
      cp "trace_configs/$workload_name" "$target_folder/trace_file_list"
      # cp "param_configs/core$number.in" "$target_folder/params.in"
    done
  done
done



# W             3
# WP            4
# baseType3     2
# flatflash(P)  3