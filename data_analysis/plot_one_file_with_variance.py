import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
import os

class DataPlotter:
    def __init__(self, rmw, prefix, display_columns, base_path='/mesh_exp/dataset/', use_run=False, run_size="KILO8", run_number=3, plot_variances=True):
        self.display_columns = display_columns
        self.base_path = os.path.expanduser("~") + base_path
        self.plot_variances = plot_variances
        self.use_run = use_run
        self.run_size = run_size
        self.run_number = run_number
        self.data_original = None
        self.data_variance = None
        self.timestamps = None

    def load_data(self):
        if not self.use_run:
            file_path = f'{self.base_path}{self.rmw}_clean/{self.prefix}_average.csv'
            self.data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}{self.rmw}_clean/{self.prefix}_variance.csv'
            self.data_variance = pd.read_csv(file_path_variance)
        else:
            file_path = f'{self.base_path}{self.rmw}_clean/{self.rmw}_{self.run_size}/{self.rmw}_{self.run_size}_exp_{self.run_number}_resampled.csv'
            self.data_original = pd.read_csv(file_path)

    def extract_and_interpolate(self):
        self.timestamps = self.data_original['Timestamp']

    def plot_data(self):
        # Convert timestamps to numpy array
        timestamps_np = self.timestamps.to_numpy()

        # Initialize subplots
        num_plots = len(self.display_columns)
        fig, axs = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots))

        if not isinstance(axs, np.ndarray):
            axs = [axs]

        # Plot each selected column
        for i, column in enumerate(self.display_columns):
            data_np = self.data_original[column].to_numpy()
            variance_np = self.data_variance[column].to_numpy()

            axs[i].plot(timestamps_np, data_np, label=column)
            if self.plot_variances:
                axs[i].fill_between(timestamps_np, data_np - variance_np, data_np + variance_np, alpha=0.2)
            axs[i].set_ylabel(column)
            axs[i].legend()

        plt.xlabel('Timestamp')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')

    parser.add_argument('rmw', type=str, help='RMW to plot')
    parser.add_argument('prefix', type=str, help='Prefix for the CSV files')
    parser.add_argument('display_columns', nargs='+', help='List of columns to display')
    parser.add_argument('--use_run', action='store_true', help='Use run data instead of averaged data')
    parser.add_argument('--run_size', type=str, default="KILO8", help='Size of the run')
    parser.add_argument('--run_number', type=str, default="3", help='Run number')
    parser.add_argument('--plot_variances', action='store_true', help='Plot variances')

    args = parser.parse_args()

    plotter = DataPlotter(args.display_columns, use_run=args.use_run, run_size=args.run_size, run_number=args.run_number, plot_variances=args.plot_variances)
    plotter.load_data()
    plotter.extract_and_interpolate()
    plotter.plot_data()
