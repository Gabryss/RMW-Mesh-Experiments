import pandas as pd
import glob
import os
import sys
import argparse

class RMWAverageVarSelect:
    def __init__(self, folder_path, size_select):
        self.folder_path = folder_path
        self.size_select = size_select
        
        self.folder_name = os.path.basename(folder_path)

        strSize = ""
        for size in self.size_select:
            strSize += size + "_"
        self.average_output_file_path = os.path.join(folder_path, f'{strSize}average.csv')
        self.variance_output_file_path = os.path.join(folder_path, f'{strSize}variance.csv')
    
    def create_simple_average_and_variance_csv(self):
        # Get all *_merged.csv files in the folder
        csv_files = []

        for size in self.size_select:
            pattern = os.path.join(self.folder_path, f'**/*_{size}_*_resampled.csv')
            csv_files.extend(glob.glob(pattern, recursive=True))

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing CSV files')
    parser.add_argument('size_select', nargs='+', help='List of sizes to select for the CSV files')

    args = parser.parse_args()

    if not args.folder_path or not args.size_select:
        print("Example: python3 rmw_average_variance_select.py /home/lchovet/mesh_exp/dataset/zenoh_clean KILO32 KILO64")
        sys.exit(1)

    rmw = RMWAverageVarSelect(args.folder_path, args.size_select)
    rmw.create_simple_average_and_variance_csv()