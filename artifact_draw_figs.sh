cd figure_drawing


# Draw figure 14
cd e2e_perf

python3 run.py  # figure 14 is OverallPerf.pdf
cd ..

# Draw figure 15
cd nthreads

python3 run.py  # figure 15 is throughput_threads.pdf
cd ..

# Draw figure 16
cd pancake

python3 run.py  # figure 16 is output.pdf
cd ..

# Draw figure 17
cd mem_latency

python3 run_a.py  # figure 17.(a) is mem_latency_breakdown_Base-CSSD.pdf
python3 run_b.py  # figure 17.(b) is mem_latency_breakdown_respective.pdf
cd ..

# Draw figure 18
cd nwrites

python3 run.py  # figure 18 is nwrites.pdf
cd ..

# Draw figure 23
cd alter_e2e_perf

python3 run.py  # figure 23 is OverallPerf.pdf
cd ..



cd ..
cd scripts-skybyte/motiv_figure_drawing

# Draw figure 2
python3 get_exetime_motivation.py
python3 overallExetime.py   # figure 2 is output/Exetime.pdf

# Draw figure 3
python3 LatencyCDF_motivation.py   # figure 3 is output/LatencyCDF.pdf

# Draw figure 4
python3 get_cpu_breakdown_motivation.py   # figure 4 is output/Breakdown.pdf
python3 CPUBreakdown.py





