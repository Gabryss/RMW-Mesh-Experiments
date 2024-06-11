import pandas as pd

# Load the data
cyclone_avg = pd.read_csv('./data/Cleaned/cyclone/cyclone_average.csv')
fast_avg = pd.read_csv('./data/Cleaned/fast/fast_average.csv')
zenoh_avg = pd.read_csv('./data/Cleaned/zenoh/zenoh_average.csv')

# Function to calculate percentage improvement
def calculate_percentage_improvement(zenoh, other, higher_is_better=True):
    if higher_is_better:
        return ((zenoh - other) / other) * 100
    else:
        return ((other - zenoh) / other) * 100

# Get list of metrics
metrics = cyclone_avg.columns[1:]  # Assuming the first column is timestamp

results = []

# Analyze each metric
for metric in metrics:
    mean_fast = fast_avg[metric].mean()
    mean_cyclone = cyclone_avg[metric].mean()
    mean_zenoh = zenoh_avg[metric].mean()
    
    # Determine if higher is better for this metric
    higher_is_better = not ('delay' in metric.lower() or 'error' in metric.lower() or 'drop' in metric.lower())
    
    improvement_zenoh_vs_fast = calculate_percentage_improvement(mean_zenoh, mean_fast, higher_is_better)
    improvement_zenoh_vs_cyclone = calculate_percentage_improvement(mean_zenoh, mean_cyclone, higher_is_better)
    
    results.append({
        'Metric': metric,
        'Mean_Fast': mean_fast,
        'Mean_Cyclone': mean_cyclone,
        'Mean_Zenoh': mean_zenoh,
        'Improvement_Zenoh_vs_Fast (%)': improvement_zenoh_vs_fast,
        'Improvement_Zenoh_vs_Cyclone (%)': improvement_zenoh_vs_cyclone
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Display the results
print(results_df)

# Optionally, save the results to a CSV file
results_df.to_csv('results_analysis.csv', index=False)