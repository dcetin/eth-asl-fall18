Files in this directory is listed as this:
* build.xml: Build file for the Java codebase.
* commands.sh: Contains all commands used to setup the remote environment, run each experiment, copy their results to the local machine and sync them to one directory. Reader should change the absolute paths in some commands accordingly to their own directory structure.
* MyManifest: Manifest file for the Java codebase.
* runner.sh: Runner script used for each machine in every experiment. Parameters are explained in the report appendix and parameter values for each experiment are also provided in the corresponding section of commands.sh.

Directory hierarchy is given as follows:
* auxiliary: Contains extra material used or mentioned in the report. Explained in detail below.
* build: Contains Java class files.
* dist: Output directory for the .jar file.
* experiment-results: Raw client, middleware and dstat outputs for each experiment. Explained in detail below.
* lib: Contains the log4j files, which are unused.
* plot: Contains plotting (aggregating/summarizing) scripts for different experimental setups.
* report: Contains the source code and images for the project report.
* res: Should contain results to be summarized and plotted by the appropriate scripts. Desired set of results should be syncd from experiment-results to this folder.
* src: Contains the source codes.

experiment-results contains experiment results separately, instead of all results in one directory. If the reader wants to inspect the results for an experiment, they can simply copy the contents of the results into the res folder and run the script corresponding to that specific experiment. If multiple results to be inspected, user should use rsync as shown in commands.sh to sync multiple directories to one (res) directory. Directory structure for each experiment is constructed accorindgly to the parameter notation explained in the appendix part of th report. **Note that results directories contain colon (:) character in their names, which is problematic for Windows environments.**
The directory contains 9 sub-directories listed as follows:
* 2ka: 2K analysis experiments
* csb1: Baseline without middleware experiments with one server
* csb2: Baseline without middleware experiments with two servers
* gmg: Gets and multi-gets experiments
* mwb1-ro: Baseline with middleware experiments with one middleware, read-only load
* mwb1-wo: Baseline with middleware experiments with one middleware, write-only load
* mwb2-ro: Baseline with middleware experiments with two middlewares, read-only load
* mwb2-wo: Baseline with middleware experiments with two middlewares, write-only load
* tpfw: Throughput for writes experiments

auxiliary directory contains the summmaries and plots for the experiments and also additional material and helpful scripts.
Files and folders in this directory is as follows:
* all-plots: Plots for all experiments.
* all-summaries: Aggregation summaries for all experiments.
* auxiliary for mwb2-tmw64: Raw data and plots for the auxiliary experiment which compared mwb2 and tpfw experiments.
* auxiliary for mwb2-tmw64/auxiliary-2-plotter.py: Plotting script for the aforementioned experiment.
* gmg_with-percDict: Gets and multi-gets summaries along with average percentile values.
* hist-diffs: Plots containing the differences of the histograms of 6 key case in gets and multi-gets experiments.
* iperf3: Results of iperf3 analyses on different pairs of machines.
* queueing-models/own-models: M/M/1 and M/M/m model results constructed for each configuration, constructed using the service rates obtained from their own results.
* queueing-models/64-models: M/M/1 and M/M/m model results constructed for each configuration, constructed using the service rates obtained from the results of the 64 thread configuration.
* all-mmms.py: Script that outputs the M/M/m model results formatted accordingly to the tex tabular environment.
* misses.py: Cache miss calculator for the misses in baseline with middleware experiments.
* mmm-results-tables.txt: All M/M/m results outputted accodingly to tex tabular formatting.
* mm-queueing.py: Model construction and testing script for M/M/1 and M/M/m queues.
* network_of_queues.m: Model construction and testing script for network of queues models.
* new-equal-load-plotter.py: Plotting script for the equal load experiments.
* rtt.py: Mean round-trip time calculator for the middleware baseline experiments, used in the network of queues models.
* saturation-csb.py: Reasoning for the choice of saturation points in two of the baseline without middleware experiments.
* tpfw-short-summary.txt: Throughput for writes summary excluding the interactive law results, which is helpful when comparing network of queues model results with the actual experiment outputs.
