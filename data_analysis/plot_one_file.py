import pandas as pd
import matplotlib.pyplot as plt

# Load the new CSV files to inspect their contents
file_paths = ['/home/mechaick/mesh_exp/dataset/zenoh_clean_test/zenoh_KILO32/zenoh_KILO32_exp_1_merged.csv',
              '/home/mechaick/mesh_exp/dataset/zenoh_clean_test/zenoh_KILO32/zenoh_KILO32_exp_2_merged.csv',
              '/home/mechaick/mesh_exp/dataset/zenoh_clean_test/zenoh_KILO32/zenoh_KILO32_exp_3_merged.csv']

# Create an empty list to store the dataframes
dataframes = []

# Read each CSV file and append the dataframe to the list
for file_path in file_paths:
    data = pd.read_csv(file_path)
    dataframes.append(data)

# Extract the relevant columns from each dataframe
timestamps = []
delay_local = []
ping_target = []

for data in dataframes:
    timestamps.append(data['Timestamp'])
    delay_local.append(data['Delay_local'])
    ping_target.append(data['Ping_target_local'])

# Interpolate the missing values in the relevant columns for each dataframe
delay_local_interpolated = []
ping_target_interpolated = []

for i in range(len(dataframes)):
    delay_local_interpolated.append(delay_local[i].interpolate())
    ping_target_interpolated.append(ping_target[i].interpolate())

# Convert pandas Series to numpy arrays for plotting
timestamps_np = [timestamps[i].to_numpy() for i in range(len(dataframes))]
delay_local_np = [delay_local_interpolated[i].to_numpy() for i in range(len(dataframes))]
ping_target_np = [ping_target_interpolated[i].to_numpy() for i in range(len(dataframes))]

# Plotting Delay Local and Ping Target Local on the same graph over time using timestamps
plt.figure(figsize=(12, 6))

for i in range(len(dataframes)):
    color = plt.rcParams['axes.prop_cycle'].by_key()['color'][i]
    plt.plot(timestamps_np[i], delay_local_np[i], label=f'Delay {i+1}', color=color)
    plt.plot(timestamps_np[i], ping_target_np[i], label=f'Ping Target {i+1}', color=color)

plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.title('Delay Local and Ping Target Local over Time')
plt.legend()

plt.tight_layout()
plt.show()
