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

experiment-results contains experiment results separately, instead of all results in one directory. If the reader wants to inspect the results for an experiment, they can simply copy the contents of the results into the res folder and run the script corresponding to that specific experiment. If multiple results to be inspected, user should use rsync as shown in commands.sh to sync multiple directories to one (res) directory.
The directory contains 9 sub-directories listed as follows:
* 2ka: 2K Analysis experiments
* csb1: Baseline without middleware experiments with one server
* csb2: Baseline without middleware experiments with two servers
* gmg: Gets and multi-gets experiments
* mwb1-ro: Baseline with middleware experiments with one middleware, read-only load
* mwb1-wo: Baseline with middleware experiments with one middleware, write-only load
* mwb2-ro: Baseline with middleware experiments with two middlewares, read-only load
* mwb2-wo: Baseline with middleware experiments with two middlewares, write-only load
* tpfw: Throughput for writes experiments
