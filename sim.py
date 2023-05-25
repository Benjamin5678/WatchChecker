#This is a modified version of a tool I made to simulate a stock price

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#Watch Information - These are in seconds/day
drift = -0.15
variance = 0.94

deviation = variance / 2 #This program uses 1 standard devation instead of the 2 that the main program returns

#Graphing Setup
total_time = 30
name = "Tide"
time_units = "Days"

error = np.zeros(total_time + 1) #[0,0,0...]
time = np.arange(0, total_time + 1) #[0,1,2...]

def increment_error(start_error, drift, deviation):
    random_number = np.random.normal(0, 1)

    #The change will equal the drift plus the deviation times a standard normal number
    change_error = drift + deviation * random_number

    new_error = start_error + change_error

    return new_error

#Simulate Watch
for i in range (1, total_time + 1):
    error[i] = increment_error(error[i - 1], drift, deviation)

#Make comined accuracy things
combined_upper = []
combined_lower = []

for i in range(0, total_time + 1):
    current_drift = drift * i
    current_variation = variance * sqrt(i)

    combined_upper.append(current_drift + current_variation)
    combined_lower.append(current_drift - current_variation)

#Make Plot
plt.plot(time, error, color = "black")
plt.plot(time, combined_upper, color = "blue", ls = "-.")
plt.plot(time, combined_lower, color = "blue", ls = "-.")

x_label = "Time " + time_units
plt.xlabel(x_label)
plt.ylabel('Error')
title = name + " Simulation"
plt.title(title)

plt.show()

# #Convert for testing in main
# convert = []

# for i in range(0, total_time + 1):
#     convert.append({"timestamp" : time[i] * 86400, "error": error[i]})

# print(convert)

#Make plot