import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
import os

class DataPlotter:
    def __init__(self, display_columns, base_path='/mesh_exp/dataset/'):
        self.display_columns = display_columns
        self.base_path = os.path.expanduser("~") + base_path
        self.plot_variances = True 
        self.use_run= False
        self.run_size = "KILO8"
        self.run_number = "3"
        self.fast_data_original = None
        self.fast_data_variance = None
        self.cyclone_data_original = None
        self.cyclone_data_variance = None
        self.zenoh_data_original = None
        self.zenoh_data_variance = None
        self.timestamps = None

    def load_data(self):
        if not self.use_run:
            file_path = f'{self.base_path}fast_clean/fast_clean_average.csv'
            self.fast_data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}fast_clean/fast_clean_variance.csv'
            self.fast_data_variance = pd.read_csv(file_path_variance)

            file_path = f'{self.base_path}cyclone_clean/cyclone_clean_average.csv'
            self.cyclone_data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}cyclone_clean/cyclone_clean_variance.csv'
            self.cyclone_data_variance = pd.read_csv(file_path_variance)

            file_path = f'{self.base_path}zenoh_clean/zenoh_clean_average.csv'
            self.zenoh_data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}zenoh_clean/zenoh_clean_variance.csv'
            self.zenoh_data_variance = pd.read_csv(file_path_variance)
        else:
            self.plot_variances = False
            file_path = f'{self.base_path}fast_clean/fast_{self.run_size}/fastrtps_{self.run_size}_exp_{self.run_number}_merged.csv'
            self.fast_data_original = pd.read_csv(file_path)

            file_path = f'{self.base_path}cyclone_clean/cyclone_{self.run_size}/cyclonedds_{self.run_size}_exp_{self.run_number}_merged.csv'
            self.cyclone_data_original = pd.read_csv(file_path)

            file_path = f'{self.base_path}zenoh_clean/zenoh_{self.run_size}/zenoh_{self.run_size}_exp_{self.run_number}_merged.csv'
            self.zenoh_data_original = pd.read_csv(file_path)




    def extract_and_interpolate(self):
        self.timestamps_fast = self.fast_data_original['Timestamp']
        self.timestamps_cyclone = self.cyclone_data_original['Timestamp']
        self.timestamps_zenoh = self.zenoh_data_original['Timestamp']

        # for column in self.display_columns:
        #     self.fast_data_original[column] = self.fast_data_original[column].interpolate()
            
        #     self.cyclone_data_original[column] = self.cyclone_data_original[column].interpolate()
            
        #     self.zenoh_data_original[column] = self.zenoh_data_original[column].interpolate()
            
        #     if self.plot_variances:
        #         self.zenoh_data_variance[column] = self.zenoh_data_variance[column].interpolate()
        #         self.cyclone_data_variance[column] = self.cyclone_data_variance[column].interpolate()
        #         self.fast_data_variance[column] = self.fast_data_variance[column].interpolate()
            

    def plot_data(self):
        # Convert timestamps to numpy array
        timestamps_np_fast = self.timestamps_fast.to_numpy()
        timestamps_np_cyclone = self.timestamps_cyclone.to_numpy()
        timestamps_np_zenoh = self.timestamps_zenoh.to_numpy()


        # Initialize subplots
        num_plots = len(self.display_columns)
        fig, axs = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots))

        if not isinstance(axs, np.ndarray):
            axs = [axs]

        # Plot each selected column
        for i, column in enumerate(self.display_columns):
            fast_data_np = self.fast_data_original[column].to_numpy()
            
            cyclone_data_np = self.cyclone_data_original[column].to_numpy()
            
            zenoh_data_np = self.zenoh_data_original[column].to_numpy()
            

            if self.plot_variances:
                fast_variance_np = self.fast_data_variance[column].to_numpy()
                cyclone_variance_np = self.cyclone_data_variance[column].to_numpy()
                zenoh_variance_np = self.zenoh_data_variance[column].to_numpy()

            axs[i].plot(timestamps_np_fast, fast_data_np,'b', label="Fast")
            axs[i].plot(timestamps_np_cyclone, cyclone_data_np,'r', label="Cyclone")
            axs[i].plot(timestamps_np_zenoh, zenoh_data_np,'g', label="Zenoh")

            if self.plot_variances:
                axs[i].fill_between(timestamps_np_fast, fast_data_np - fast_variance_np, fast_data_np + fast_variance_np, alpha=0.2)
                axs[i].fill_between(timestamps_np_cyclone, cyclone_data_np - cyclone_variance_np, cyclone_data_np + cyclone_variance_np, alpha=0.2)
                axs[i].fill_between(timestamps_np_zenoh, zenoh_data_np - zenoh_variance_np, zenoh_data_np + zenoh_variance_np, alpha=0.2)
            axs[i].set_ylabel(column)
            axs[i].legend()

        plt.xlabel('Timestamp')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')

    parser.add_argument('display_columns', nargs='+', help='List of columns to display')

    args = parser.parse_args()

    if not args.display_columns:
        print("Usage: python your_script_name.py <RMW> <Prefix> <Display_Columns>")
        print("Example: python3 plot_all_rmw.py zenoh zenoh_clean Delay_local Ping_target_local Bytes_Send_leo02 RAM_percent_leo02")
        sys.exit(1)

    plotter = DataPlotter(args.display_columns)
    plotter.load_data()
    plotter.extract_and_interpolate()
    plotter.plot_data()
