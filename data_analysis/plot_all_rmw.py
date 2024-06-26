import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
import os

class DataPlotter:
    def __init__(self, display_columns, base_path='/mesh_exp/dataset/', use_run=False, run_size="KILO8", run_number="3", plot_variances=True, prefix=""):
        self.display_columns = display_columns
        self.base_path = os.path.expanduser("~") + base_path
        self.prefix = prefix
        self.plot_variances = plot_variances
        self.use_run = use_run
        self.run_size = run_size
        self.run_number = run_number
        self.fast_data_original = None
        self.fast_data_variance = None
        self.cyclone_data_original = None
        self.cyclone_data_variance = None
        self.zenoh_data_original = None
        self.zenoh_data_variance = None
        self.timestamps = None
        if len(self.display_columns) == 1:
            if self.display_columns[0] == 'Ping_target_local':
                self.y_legend = 'Reachability'
                self.folder = 'reachability'
            elif self.display_columns[0] == 'Delay_local':
                self.y_legend = 'Delay[s]'
                self.folder = 'delay'
            elif self.display_columns[0] == 'Bytes_Send_leo02':
                self.y_legend = 'Bytes[KB]'
                self.folder = 'bandwidth'
            else:
                self.y_legend = self.display_columns[0]
                self.folder = ''

    def load_data(self):
        if not self.use_run:
            if self.prefix == '':
                file_path = f'./data/Cleaned/fast/fast_average.csv'
                self.fast_data_original = pd.read_csv(file_path)

                file_path_variance = f'./data/Cleaned/fast/fast_variance.csv'
                self.fast_data_variance = pd.read_csv(file_path_variance)

                file_path = f'./data/Cleaned/cyclone/cyclone_average.csv'
                self.cyclone_data_original = pd.read_csv(file_path)

                file_path_variance = f'./data/Cleaned/cyclone/cyclone_variance.csv'
                self.cyclone_data_variance = pd.read_csv(file_path_variance)

                file_path = f'./data/Cleaned/zenoh/zenoh_average.csv'
                self.zenoh_data_original = pd.read_csv(file_path)

                file_path_variance = f'./data/Cleaned/zenoh/zenoh_variance.csv'
                self.zenoh_data_variance = pd.read_csv(file_path_variance)
            else:
                file_path = f'./data/Cleaned/fast/{self.prefix}_average.csv'
                self.fast_data_original = pd.read_csv(file_path)

                file_path_variance = f'./data/Cleaned/fast/{self.prefix}_variance.csv'
                self.fast_data_variance = pd.read_csv(file_path_variance)

                file_path = f'./data/Cleaned/cyclone/{self.prefix}_average.csv'
                self.cyclone_data_original = pd.read_csv(file_path)

                file_path_variance = f'./data/Cleaned/cyclone/{self.prefix}_variance.csv'
                self.cyclone_data_variance = pd.read_csv(file_path_variance)

                file_path = f'./data/Cleaned/zenoh/{self.prefix}_average.csv'
                self.zenoh_data_original = pd.read_csv(file_path)

                file_path_variance = f'./data/Cleaned/zenoh/{self.prefix}_variance.csv'
                self.zenoh_data_variance = pd.read_csv(file_path_variance)

        else:
            file_path = f'./data/Cleaned/fast/fast_{self.run_size}/fast_{self.run_size}_exp_{self.run_number}_resampled.csv'
            self.fast_data_original = pd.read_csv(file_path)

            file_path = f'./data/Cleaned/cyclone/cyclone_{self.run_size}/cyclone_{self.run_size}_exp_{self.run_number}_resampled.csv'
            self.cyclone_data_original = pd.read_csv(file_path)

            file_path = f'./data/Cleaned/zenoh/zenoh_{self.run_size}/zenoh_{self.run_size}_exp_{self.run_number}_resampled.csv'
            self.zenoh_data_original = pd.read_csv(file_path)

    def extract_and_interpolate(self):
        self.timestamps_fast = self.fast_data_original['Timestamp']
        self.timestamps_cyclone = self.cyclone_data_original['Timestamp']
        self.timestamps_zenoh = self.zenoh_data_original['Timestamp']


    def plot_data(self):
        # Convert timestamps to numpy array
        timestamps_np_fast = self.timestamps_fast.to_numpy()
        timestamps_np_cyclone = self.timestamps_cyclone.to_numpy()
        timestamps_np_zenoh = self.timestamps_zenoh.to_numpy()

        # Initialize subplots
        num_plots = len(self.display_columns)
        fig, axs = plt.subplots(num_plots, 1, figsize=(20, 5 * num_plots))

        if not isinstance(axs, np.ndarray):
            axs = [axs]

        # Plot each selected column
        for i, column in enumerate(self.display_columns):
            if self.display_columns[0] == 'Bytes_Send_leo02':
                fast_data_np = self.fast_data_original[column].to_numpy() / 1024
                cyclone_data_np = self.cyclone_data_original[column].to_numpy() / 1024
                zenoh_data_np = self.zenoh_data_original[column].to_numpy() / 1024
            else:
                fast_data_np = self.fast_data_original[column].to_numpy()
                cyclone_data_np = self.cyclone_data_original[column].to_numpy()
                zenoh_data_np = self.zenoh_data_original[column].to_numpy()

            if self.plot_variances:
                fast_variance_np = self.fast_data_variance[column].to_numpy()
                cyclone_variance_np = self.cyclone_data_variance[column].to_numpy()
                zenoh_variance_np = self.zenoh_data_variance[column].to_numpy()

            axs[i].plot(timestamps_np_fast, fast_data_np, 'b', label="Fast")
            axs[i].plot(timestamps_np_cyclone, cyclone_data_np, 'r', label="Cyclone")
            axs[i].plot(timestamps_np_zenoh, zenoh_data_np, 'g', label="Zenoh")


            if self.plot_variances:
                axs[i].fill_between(timestamps_np_fast, fast_data_np - fast_variance_np, fast_data_np + fast_variance_np, alpha=0.2)
                axs[i].fill_between(timestamps_np_cyclone, cyclone_data_np - cyclone_variance_np, cyclone_data_np + cyclone_variance_np, alpha=0.2)
                axs[i].fill_between(timestamps_np_zenoh, zenoh_data_np - zenoh_variance_np, zenoh_data_np + zenoh_variance_np, alpha=0.2)
            if len(self.display_columns) == 1:
                axs[i].set_ylabel(self.y_legend)
            else:
                axs[i].set_ylabel(column)
            axs[i].legend()
            axs[i].grid(True,linestyle='--', alpha=0.7)


        plt.xlabel('Timestamp[s]')
        plt.tight_layout()
        path = f"../docs/plots/{self.folder}/"
        if self.prefix == '':
            path = path+f"Average_{self.folder}"
        else:
            path = path+f"Average_{self.folder}_{self.prefix}"
        if self.plot_variances:
            path = path+"_variances"
        path = path+".png"
        plt.savefig(path,bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')

    parser.add_argument('display_columns', nargs='+', help='List of columns to display')
    parser.add_argument('--use_run', action='store_true', help='Use run data instead of averaged data')
    parser.add_argument('--run_size', type=str, default="KILO8", help='Size of the run')
    parser.add_argument('--run_number', type=str, default="3", help='Run number')
    parser.add_argument('--plot_variances', action='store_true', help='Plot variances')
    parser.add_argument('--prefix', type=str, default='', help='Prefix for the CSV files')

    args = parser.parse_args()

    plotter = DataPlotter(args.display_columns, use_run=args.use_run, run_size=args.run_size, run_number=args.run_number, plot_variances=args.plot_variances, prefix=args.prefix)
    plotter.load_data()
    plotter.extract_and_interpolate()
    plotter.plot_data()
