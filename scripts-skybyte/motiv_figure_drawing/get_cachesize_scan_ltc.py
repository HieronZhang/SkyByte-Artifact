import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


output_dir = "../../output/"

workloads = ["bfs-4", "bc-4", "dlrm-4", "fft-4", "radix-4", "ycsb-4", "tpcc-4"]

workload_names = ["bfs-twitter", "bc-twitter", "dlrm-inference", "fft", "radix", "ycsb-nstore", "tpcc-nstore"]

design = "baseType3"

dramsizes = ["main0_25g-0_25-w0_25", "main0_5g-0_25-w0_25", "main1g-0_25-w0_25", "main2g-0_25-w0_25", "main4g-0_25-w0_25", "main8g-0_25-w0_25", "main16g-0_25-w0_25", "main32g-0_25-w0_25"]
# dramsizes = ["baseType3", "flatflash", "assd-W", "assd-WP"]

output_file = f"cachesize_scan_avg_lat.txt"
fout = open(output_file, 'w')

fout.write("64MB | 128MB | 256MB | 512MB | 1GB | 2GB | 4GB | 8GB\n\n")
# fout.write("BaseType3 | FlatFlash-CXL | SkyByte-W | SkyByte-WP\n\n")

for i in range(len(workloads)):
    fout.write(workload_names[i]+"\n")
    for j in range(len(dramsizes)):
        data_file = output_dir + workloads[i] + "-" + design + "-" + dramsizes[j]
        # print(data_file)
        if os.path.exists(data_file):
            f = open(data_file, "r")
            lines = f.read()
            # print(lines)
            lines = lines.strip().split("\n")
            find = False
            for line in lines:
                terms = line.split(":")
                if terms[0]=="Overall_Average_Latency":
                    avg_ltc = terms[1].strip()
                    find = True
            if find:
                fout.write(avg_ltc+" ")
            else:
                fout.write("inf ")
        else:
            fout.write("inf ")
    fout.write("\n\n")