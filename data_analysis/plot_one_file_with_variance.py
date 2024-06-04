import pandas as pd
import matplotlib.pyplot as plt


RMW = "zenoh"
# Load the new CSV file to inspect its contents
file_path = f'/home/mechaick/mesh_exp/dataset/{RMW}_clean_test/_average.csv'
data_original = pd.read_csv(file_path)

file_path_variance = f'/home/mechaick/mesh_exp/dataset/{RMW}_clean_test/_variance.csv'
data_variance = pd.read_csv(file_path_variance)


# Extract the relevant columns from the original data
timestamps = data_original['Timestamp']
delay_local = data_original['Delay_local']
ping_target = data_original['Ping_target_local']

# Extract the variance columns from the variance data
delay_variance = data_variance['Delay_local']
ping_variance = data_variance['Ping_target_local']

# Interpolating the missing values in the relevant columns
delay_local_interpolated = delay_local.interpolate()
ping_target_interpolated = ping_target.interpolate()
ping_target_interpolated = ping_target_interpolated*10
delay_variance_interpolated = delay_variance.interpolate()
ping_variance_interpolated = ping_variance.interpolate()
ping_variance_interpolated = ping_variance_interpolated*10

# Convert pandas Series to numpy arrays for plotting
timestamps_np = timestamps.to_numpy()
delay_local_np = delay_local_interpolated.to_numpy()
ping_target_np = ping_target_interpolated.to_numpy()
delay_variance_np = delay_variance_interpolated.to_numpy()
ping_variance_np = ping_variance_interpolated.to_numpy()

# Plotting Delay Local and Ping Target Local with variance error bands
plt.figure(figsize=(12, 6))

# Plot Delay Local with variance
plt.plot(timestamps_np, delay_local_np, label='Delay Local')
plt.fill_between(timestamps_np, delay_local_np - delay_variance_np, delay_local_np + delay_variance_np, color='blue', alpha=0.2)

# Plot Ping Target Local with variance
plt.plot(timestamps_np, ping_target_np, label='Ping Target Local', color='orange')
plt.fill_between(timestamps_np, ping_target_np - ping_variance_np, ping_target_np + ping_variance_np, color='orange', alpha=0.2)

plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.title('Delay Local and Ping Target Local over Time with Variance')
plt.legend()

plt.tight_layout()
plt.show()
