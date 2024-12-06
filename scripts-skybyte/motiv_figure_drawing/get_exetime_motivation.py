import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


output_dir = "../../output-ap10/"

workloads = ["bc-large", "bfs-dense-4-200M-baseType3", "dlrm-small", "radix-large", "srad-4-large", "ycsb-parsed", "tpcc-parsed"]

workload_names = [ "bc", "bfs-dense", "dlrm", "radix", "srad", "ycsb", "tpcc"]

# designtypes = ["baseType3", "flatflash", "assd-W", "assd-WP", "assd-Full"]
# designtypes = ["baseType3", "flatflash", "assd-W", "assd-WP"]

output_file = f"exetime.txt"
fout = open(output_file, 'w')

# fout.write("BaseType3 | FlatFlash-CXL | SkyByte-W | SkyByte-WP | SkyByte-Full\n\n")
fout.write("DRAM Memory | Baseline CXL-SSD\n\n")

for i in range(len(workloads)):
    fout.write(workload_names[i]+"\n")
    # for j in range(len(designtypes)):
    data_file = output_dir + workloads[i]
    longest_exe_time = 0
    time1 = 0
    time2 = 0
    # print(data_file)
    if os.path.exists(data_file):
        f = open(data_file, "r")
        lines = f.read()
        # print(lines)
        lines = lines.strip().split("\n")
        find1 = False
        find2 = False
        count = 0
        meet = False
        for line in lines:
            terms = line.split("Core")
            if terms[0]=="**":
                # avg_ltc = terms[1].strip()
                print(terms[2].strip())
                s_terms = terms[2].strip().split()
                for s_term in s_terms:
                    if s_term.startswith("cycles:"):
                        print(s_term.split(":")[1].strip())
                        longest_exe_time = max(int(s_term.split(":")[1].strip()),longest_exe_time)
                meet = True
                if count == 0:
                    find1 = True
                if count == 1:
                    find2 = True
            else:
                if meet:
                    print(longest_exe_time)
                    count += 1
                    if count == 1:
                        time1 = longest_exe_time
                    if count == 2:
                        time2 = longest_exe_time
                    longest_exe_time = 0
                    meet = False
        if find1:
            fout.write(str(time1)+" ")
        else:
            fout.write("inf ")
        if find2:
            fout.write(str(time2)+" ")
        else:
            fout.write("inf ")
    else:
        fout.write("inf ")
    fout.write("\n\n")