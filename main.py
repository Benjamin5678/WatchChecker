import time
import ast
import math
import statistics

def measure():
    target_unix = math.ceil(time.time() / 60) * 60
    target_minutes = math.trunc(target_unix / 60 % 60)

    #The program will find whatever the next minute is to make an error measurement.
    #In case the watch is too far off or for any other reason the user misses the target time they can change it.
    print(f"The current target minute is {target_minutes}, would you like to change this?")
    if input("Type 'change' to change target -> ") == "change": #I prefer if/else instead of option1/option2/exception. Maybe theres a better way I'm not familiar with.
        add_minutes = float(input("How many minutes would you like to change by? (Use negative time to decrease) -> "))
        target_unix += add_minutes * 60
        target_minutes += add_minutes
    
    print(f"When the watch strikes exactly minute {target_minutes}")
    input("Press Enter...")

    timestamp = time.time()
    error = timestamp - target_unix

    print(f"Measured Error: {round(error, 2)} seconds")

    return {"error": error, "timestamp": timestamp}

def save_value(input_value, filename):
    with open(filename, 'w') as f:
        f.write(str(input_value))

def load_value(filename):
    with open(filename, 'r') as f:
        read = f.read()
    return read

#I dont know if I did my statistical analysis in a proper manner. I never took a class about this stuff so this is combination of me asking ChatGPT about statistics and other stuff I pulled out of my ass.
#I define drift as the average change in the watch error / time
#Variance is two standard deviations of the change in error / sqrt(time) (Theoretically the watch will land in this range 95% of the time)
#The change in error needs to be scaled by the change in time. Otherwise the user needs to measure exactly every 24 hours.
#The average drift should scale linearly. Variance should scale with the root of time since random changes can undo themselves. (Research brownian motion or ask ChatGPT to explain why this is the case)
#Combined accuracy is the range the watch will end up with 95% certainty. It is the drift plus or minus the variance.
def analyze(input_value):
    n = len(input_value) - 1
    
    error_differences = []
    time_differences = []

    for i in range(n):
        error_difference = input_value[i + 1]["error"] - input_value[i]["error"]
        error_differences.append(error_difference)
        
        time_difference = input_value[i + 1]["timestamp"] - input_value[i]["timestamp"]
        time_difference /= 60 * 60 *24
        time_differences.append(time_difference)
    
    linear_adjusted = []
    root_adjusted = []

    for i in range(n):
        linear_adjusted.append(error_differences[i]/time_differences[i])
        root_adjusted.append(error_differences[i]/math.sqrt(time_differences[i]))
    
    mean_drift = statistics.mean(linear_adjusted)

    std_deviation = statistics.stdev(root_adjusted)
    variance = 2 * std_deviation

    combined_accuracy = [round(mean_drift + variance, 2), round(mean_drift - variance, 2)]

    daily_stats = {"drift" : round(mean_drift, 2), "variance" : round(variance, 2), "combined" : combined_accuracy}
    
    monthly_drift = mean_drift * 30
    monthly_variance = variance * math.sqrt(30)
    monthly_combined = [round(monthly_drift + monthly_variance, 2), round(monthly_drift - monthly_variance, 2)]
    
    monthly_stats = {"drift" : round(monthly_drift, 2), "variance" : round(monthly_variance, 2), "combined" : monthly_combined}
    
    return {"daily" : daily_stats, "monthly" : monthly_stats}

def show_stats(input_value):
    if len(input_value) >= 3:
        analysis = analyze(input_value)
        
        drift = analysis["daily"]["drift"]
        variance = analysis["daily"]["variance"]
        combined = analysis["daily"]["combined"]

        print("\nDaily:")
        print(f"Drift: {drift} s/d")
        print(f"Variance: {variance} s/d @ 95% confidence")
        print(f"Combined: {combined[0]} to {combined[1]} s/d")

        drift = analysis["monthly"]["drift"]
        variance = analysis["monthly"]["variance"]
        combined = analysis["monthly"]["combined"]
    
        print("\nMonthly:")
        print(f"Drift: {drift} s/m")
        print(f"Variance: {variance} s/m @ 95% confidence")
        print(f"Combined: {combined[0]} to {combined[1]} s/m")
    else:
        print("Analysis could not be obtained. Minimum of 3 data points required.")
        #It should be able to display the drift with 2. 3 is needed for variance and consequently combined accuracy.
        #However, I couldn't be bothered to make this logic work right.


#Main program:

file_name = input("Enter watch name -> ") + ".txt"

try:
    saved_measurements = ast.literal_eval(load_value(file_name))
except:
    print(f"No file name {file_name} found. Creating...")
    saved_measurements = []
    save_value(saved_measurements, file_name)

show_stats(saved_measurements)

print("\nMeasuring procedure will now begin...")

new_measurement = measure()

try: #Cant measure how long ago the last measurement was if there is only one
    time_since_last = (new_measurement["timestamp"] - saved_measurements[len(saved_measurements) - 1]["timestamp"]) / 3600
    if time_since_last < 12:
        print("Warning! This measurement is less than 12 hours since your last one. This could lead to innacurate analysis.")
except:
    pass

if input("Type 'confirm' to save data -> ") == "confirm": #See my previous blurb about this in measure()
    saved_measurements.append(new_measurement)
    save_value(saved_measurements, file_name)
    show_stats(saved_measurements)
else:
    print("Discarding Measurement")