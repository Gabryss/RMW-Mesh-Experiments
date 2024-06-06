import pandas as pd
import glob
import os

class RMWAverageVar:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.folder_name = os.path.basename(folder_path)
        self.average_output_file_path = os.path.join(folder_path, f'{self.folder_name}_average.csv')
        self.variance_output_file_path = os.path.join(folder_path, f'{self.folder_name}_variance.csv')
    
    def create_simple_average_and_variance_csv(self):
        # Get all *_merged.csv files in the folder
        csv_files = glob.glob(os.path.join(self.folder_path, '**/*_resampled.csv'),recursive=True)

        # Load all dataframes and convert timestamps from milliseconds to seconds
        dataframes = [pd.read_csv(file) for file in csv_files]

        # Concatenate all dataframes
        concatenated_df = pd.concat(dataframes)

        # Group by the rounded timestamps and compute the average and variance
        average_df = concatenated_df.groupby('Timestamp').mean().reset_index()
        variance_df = concatenated_df.groupby('Timestamp').var().reset_index()

        # Save the results to CSV files
        average_df.to_csv(self.average_output_file_path, index=False)
        variance_df.to_csv(self.variance_output_file_path, index=False)
        print(f'Simple average data saved to {self.average_output_file_path}')
        print(f'Variance data saved to {self.variance_output_file_path}')
