import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

class DataVisualizer:
    def __init__(self, columns_p) -> None:
        """
        Initialize the DataVisualizer class.
        """
        self.colums = columns_p
        self.message_sizes = ['KILO', 'KILO2', 'KILO4', 'KILO8', 'KILO16', 'KILO32', 'KILO64']
        self.path = './data/Cleaned/'
        self.fast_data = self.get_all_dataframe(self.path + 'fast/', 'fast')
        self.cyclone_data = self.get_all_dataframe(self.path + 'cyclone/', 'cyclone')
        self.zenoh_data = self.get_all_dataframe(self.path + 'zenoh/', 'zenoh')

        # Combine all data into a single DataFrame
        self.all_data = pd.concat([self.fast_data, self.cyclone_data, self.zenoh_data], ignore_index=True)
        if self.colums == 'CPU_percent_leo02' or self.colums == 'CPU_percent_local':
            self.modify_column_values_core(self.colums)
        
        if self.colums == 'RAM_info_leo02' or self.colums == 'RAM_info_local':
            self.modify_column_ram_bytes(self.colums)
        
        if self.colums == 'Bytes_Send_leo02' or self.colums == 'Bytes_Received_local':
            self.modify_column_bw_bytes(self.colums)


    def get_all_dataframe(self, folder_path, rmw_type):
        # For a given RMW, span over each size
        data = []
        for size in self.message_sizes:
            df = self.get_dataframe_size(size, folder_path)
            if df is not None:
                df['Message_Size'] = size
                df['RMW'] = rmw_type
                data.append(df)
        if data:
            concatenated_data = pd.concat(data, ignore_index=True)  # Ignore index to avoid duplicate labels
            return concatenated_data
        else:
            return pd.DataFrame()


    def get_dataframe_size(self, size, folder_path):
        # For a given size, get the dataframe containing each run
        pattern = os.path.join(folder_path, f'**/*_{size}_*_resampled.csv')
        csv_files = glob.glob(pattern, recursive=True)
        if not csv_files:
            return None
        dataframes = [pd.read_csv(file) for file in csv_files]
        return pd.concat(dataframes, ignore_index=True)  # Ignore index to avoid duplicate labels


    def modify_column_values_core(self, column_name):
        if column_name in self.all_data.columns:
            self.all_data[column_name] = self.all_data[column_name] / 4


    def modify_column_bw_bytes(self, column_name):
        if column_name in self.all_data.columns:
            self.all_data[column_name] = self.all_data[column_name] / 1024

    def modify_column_ram_bytes(self, column_name):
        if column_name in self.all_data.columns:
            self.all_data[column_name] = self.all_data[column_name] / 1024**2


    def plot_boxplot(self, metric):
        if self.all_data.empty:
            print("No data available to plot.")
            return
        if metric not in self.all_data.columns:
            print(f"Metric '{metric}' not found in data.")
            return
        
        if metric == 'CPU_percent_leo02' or metric == 'CPU_percent_local':
            y_legend = 'CPU usage[%]'
        elif metric == 'CPU_time_leo02' or metric == 'CPU_time_local':
            y_legend = 'Time[s]'
        elif metric == 'RAM_percent_leo02' or metric == 'RAM_percent_local':
            y_legend = 'RAM usage[%]'
        elif metric == 'RAM_info_leo02' or metric == 'RAM_info_local':
            y_legend = 'RAM usage[MB]'
        elif metric == 'Bytes_Send_leo02' or metric == 'Bytes_Received_local':
            y_legend = 'Bytes[KB]'
        else:
            y_legend = metric
        


        # Define a color palette
        palette = {"fast": "blue", "cyclone": "red", "zenoh": "green"}
        
        plt.figure(figsize=(7, 5))
        box_plot = sns.boxplot(data=self.all_data, x='Message_Size', y=metric, hue='RMW', palette=palette, showfliers=False,linewidth=2.5)
        # plt.title(f'Boxplot of {metric} for Different RMWs and Message Sizes')
        box_plot.set_xticklabels([1,2,4,8,16,32,64])
        plt.xlabel('Message size[KB]')
        plt.ylabel(y_legend)
        plt.legend(title='RMW')
        plt.grid(True, linestyle='--', alpha=0.7)
        folder = 'RAM'                                # Available: bandwidth, CPU, RAM
        path = f'../docs/plots/{folder}/box_{metric}.png'
        plt.savefig(path,bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')
    parser.add_argument('column', type=str, help='Column to plot')

    args = parser.parse_args()

    # Example usage:
    visualizer = DataVisualizer(args.column)

    # Debug: print the structure of the combined DataFrame
    # print("Combined DataFrame head:")
    # print(visualizer.all_data.head())
    # print("\nCombined DataFrame columns:")
    # print(visualizer.all_data.columns)

    # Plot the boxplot
    visualizer.plot_boxplot(args.column)
