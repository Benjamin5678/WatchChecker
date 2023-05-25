# WatchChecker
A program that experimentally measures the accuracy of a watch.

#How to use
1. First run main.py
2. You will be asked to select a watch by name
  a. The data measured from the watch will be loaded from the text file with that name
  b. A new data file will be created if it does not yet exist
4. The statistics about the watch will then be displayed if available
  a. Three measurements must be taken to calculate statistics
  b. Drift: On average how much your watch changes time
  c. Variance: Within 2 standard deviations (95% certainty) how far your watch vary from the average drift
  d. Combined Accuracy: The upper and lower extremes your watch might be off by (again 95% certainty). This is calculated by drift plus or minus variance.
6. The measuring sequence will start
  a. Verify the target time. It should be the next closest minute your watch is about to strike. Otherwise you have the option to add or remove time. You can even use a decimal for convinience.
  b. When the watch strikes the target time press enter
  c. You will be asked to confirm you want to save your measurment. You will be warned if your last measurement was less than 12 hours ago as this can cause the analysis of the watch to be innacurate.
6. The updated statistics will now be displayed if available
