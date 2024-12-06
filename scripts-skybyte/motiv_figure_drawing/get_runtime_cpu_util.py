import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


output_dir = "../../output/"

workloads = ["bfs-4", "bc-4", "dlrm-4", "fft-4", "radix-4", "ycsb-4", "tpcc-4"]

workload_names = ["bfs-twitter", "bc-twitter", "dlrm-inference", "fft", "radix", "ycsb-nstore", "tpcc-nstore"]

designtypes = ["baseType3", "flatflash", "assd-W", "assd-WP", "assd-Full"]
# designtypes = ["baseType3", "flatflash", "assd-W", "assd-WP"]

output_file = f"exetime_cpu_util.txt"
fout = open(output_file, 'w')

fout.write("BaseType3 | FlatFlash-CXL | SkyByte-W | SkyByte-WP | SkyByte-Full\n\n")
# fout.write("BaseType3 | FlatFlash-CXL | SkyByte-W | SkyByte-WP\n\n")

for i in range(len(workloads)):
    fout.write(workload_names[i]+"\n")
    for j in range(len(designtypes)):
        data_file = output_dir + workloads[i] + "-" + designtypes[j]
        # print(data_file)
        if os.path.exists(data_file):
            f = open(data_file, "r")
            lines = f.read()
            # print(lines)
            lines = lines.strip().split("\n")
            find = False
            for line in lines:
                terms = line.split(":")
                if terms[0]=="Program_Finish_Time(Real)":
                    avg_ltc = terms[1].strip()
                    find = True
            if find:
                fout.write(avg_ltc+" ")
            else:
                fout.write("inf ")
        else: 
            fout.write("inf ")

    find1 = False
    find2 = False
    fout.write("\n")
    for line in lines:
        terms = line.split(":")
        if terms[0]=="Total_Cores_Idle_Time":
            Idle_time = terms[1].strip()
            find1 = True
    for line in lines:
        terms = line.split(":")
        if terms[0]=="Total_Cores_Busy_Time":
            busy_time = terms[1].strip()
            find2 = True
    if find1 and find2:
        fout.write(f"{int(float(busy_time)*100/(float(busy_time) + float(Idle_time)))} ")
    else:
        fout.write("inf ")
    fout.write("\n\n")