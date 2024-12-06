cd ../src

make clean
make -j

./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/bc-4.config -c 4 -o /dev/pts/3 -p -f bc-4-assd-Full
./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/bfs-4.config -c 4 -o /dev/pts/3 -p -f bfs-4-assd-Full
./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/fft-4.config -c 4 -o /dev/pts/3 -p -f fft-4-assd-Full
./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/radix-4.config -c 4 -o /dev/pts/3 -p -f radix-4-assd-Full
./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/tpcc-4.config -c 4 -o /dev/pts/3 -p -f tpcc-4-assd-Full
./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/dlrm-4.config -c 4 -o /dev/pts/3 -p -f dlrm-4-assd-Full
./main -b ../configs/baselines/assd-Full.config -w ../configs/workloads/ycsb-4.config -c 4 -o /dev/pts/3 -p -f ycsb-4-assd-Full

# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/bc-4.config -c 4 -o /dev/pts/3 -p -f bc-4-assd-WP
# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/bfs-4.config -c 4 -o /dev/pts/3 -p -f bfs-4-assd-WP
# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/fft-4.config -c 4 -o /dev/pts/3 -p -f fft-4-assd-WP
# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/radix-4.config -c 4 -o /dev/pts/3 -p -f radix-4-assd-WP
# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/tpcc-4.config -c 4 -o /dev/pts/3 -p -f tpcc-4-assd-WP
# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/dlrm-4.config -c 4 -o /dev/pts/3 -p -f dlrm-4-assd-WP
# ./main -b ../configs/baselines/assd-WP.config -w ../configs/workloads/ycsb-4.config -c 4 -o /dev/pts/3 -p -f ycsb-4-assd-WP

# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/bc-4.config -c 4 -o /dev/pts/3 -p -f bc-4-assd-W
# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/bfs-4.config -c 4 -o /dev/pts/3 -p -f bfs-4-assd-W
# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/fft-4.config -c 4 -o /dev/pts/3 -p -f fft-4-assd-W
# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/radix-4.config -c 4 -o /dev/pts/3 -p -f radix-4-assd-W
# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/tpcc-4.config -c 4 -o /dev/pts/3 -p -f tpcc-4-assd-W
# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/dlrm-4.config -c 4 -o /dev/pts/3 -p -f dlrm-4-assd-W
# ./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/ycsb-4.config -c 4 -o /dev/pts/3 -p -f ycsb-4-assd-W

# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/bc-4.config -c 4 -o /dev/pts/3 -p -f bc-4-flatflash
# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/bfs-4.config -c 4 -o /dev/pts/3 -p -f bfs-4-flatflash
# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/fft-4.config -c 4 -o /dev/pts/3 -p -f fft-4-flatflash
# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/radix-4.config -c 4 -o /dev/pts/3 -p -f radix-4-flatflash
# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/tpcc-4.config -c 4 -o /dev/pts/3 -p -f tpcc-4-flatflash
# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/dlrm-4.config -c 4 -o /dev/pts/3 -p -f dlrm-4-flatflash
# ./main -b ../configs/baselines/flatflash.config -w ../configs/workloads/ycsb-4.config -c 4 -o /dev/pts/3 -p -f ycsb-4-flatflash

# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/bc-4.config -c 4 -o /dev/pts/3 -p -f bc-4-baseType3
# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/bfs-4.config -c 4 -o /dev/pts/3 -p -f bfs-4-baseType3
# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/fft-4.config -c 4 -o /dev/pts/3 -p -f fft-4-baseType3
# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/radix-4.config -c 4 -o /dev/pts/3 -p -f radix-4-baseType3
# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/tpcc-4.config -c 4 -o /dev/pts/3 -p -f tpcc-4-baseType3
# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/dlrm-4.config -c 4 -o /dev/pts/3 -p -f dlrm-4-baseType3
# ./main -b ../configs/baselines/baseType3.config -w ../configs/workloads/ycsb-4.config -c 4 -o /dev/pts/3 -p -f ycsb-4-baseType3

# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/bc-4.config -c 4 -o /dev/pts/3 -p -f bc-4-assd-CW
# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/bfs-4.config -c 4 -o /dev/pts/3 -p -f bfs-4-assd-CW
# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/fft-4.config -c 4 -o /dev/pts/3 -p -f fft-4-assd-CW
# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/radix-4.config -c 4 -o /dev/pts/3 -p -f radix-4-assd-CW
# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/tpcc-4.config -c 4 -o /dev/pts/3 -p -f tpcc-4-assd-CW
# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/dlrm-4.config -c 4 -o /dev/pts/3 -p -f dlrm-4-assd-CW
# ./main -b ../configs/baselines/assd-CW.config -w ../configs/workloads/ycsb-4.config -c 4 -o /dev/pts/3 -p -f ycsb-4-assd-CW


# Bugs Finding

./main -b ../configs/baselines/assd-W.config -w ../configs/workloads/bfs-4.config -t ../configs/settings/main8g-0_25-w0_25.config -c 4 -o /dev/pts/3 -p -f bfs-4-assd-W-main8g-0_25-w0_25gdb --args 