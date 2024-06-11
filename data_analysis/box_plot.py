import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import os

class Bar_Plot_Col():
    """
    Plotting bar diagram class. Can be used for other projects
    """
    def __init__(self, data_p, title_p, xy_labels_p, nb_bar_p=1, used_columns_p=None, legend_p=None, x_order_p=None) -> None:
        """
        Args:
        - data: raw data <panda.read_csv> format.
        - nb_bar: number of bars to plot <int>.
        - used_columns : list or tuple. Each element of the list represent the set of columns used for the bar figure.
        - legend : list of string that represent legend of each bar.
        """
        self.data = data_p
        self.data_fast = []
        self.data_cyclone = []
        self.data_zenoh = []

        self.columns = self.data.columns.tolist()
        self.nb_bar = nb_bar_p
        self.legend = legend_p
        self.title = title_p
        self.xy_labels = xy_labels_p
        self.x_order = x_order_p
        # Used columns
        if used_columns_p == None:
            print("Please select which columns to compare. Two first columns selected")
            self.used_column = self.columns
        else:
            self.used_column = used_columns_p

        # Execute plot
        # self.data = self.pre_cleaning(self.data)
        
        self.formated_data = self.seaborn_preformating(self.data)
        self.plot_data_seaborn(self.formated_data)

        # Display the plot
        if self.title:
            plt.title(self.title)
        plt.tight_layout()
        plt.show()
    

    def read_csv(self, folder_path):
        """
        Read CSV from path
        """
        csv_files = glob.glob(os.path.join(folder_path, '**/*_resampled.csv'),recursive=True)
        return csv_files


    def pre_cleaning(self, data_p):
        """
        Convert columns to numerical types, coercing errors to NaN
        """
        data = data_p
        for col in self.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Show the first few rows of the data Frame to confirm changes
        data.head(), data.dtypes
        return data


    def seaborn_preformating(self, data_p):
        """
        Prepare the data for plotting by melting it into a long format suitable for Seaborn's boxplot function
        """
        data = data_p

        if self.nb_bar == 1:
            seaborn_df = pd.melt(data, id_vars=[self.used_column[0]], 
                             value_vars=[self.used_column[1]], 
                             var_name='Metric', value_name='Value')
            seaborn_df['Legend'] = self.legend[0]
            return seaborn_df
        
        else:
            seaborn_df_list = []
            for indx in range(self.nb_bar):
                seaborn_df_list.append(pd.melt(data, id_vars=[self.used_column[0]], 
                             value_vars=[self.used_column[indx+1]],
                             var_name='Metric', value_name='Value'))
                if indx != 0:
                    # Rename the metric column in order to seaborn to interpret it as the same thing
                    seaborn_df_list[indx]['Metric'] = seaborn_df_list[indx]['Metric'].str.replace(self.used_column[indx+1], self.used_column[1])

                seaborn_df_list[indx]['Legend'] = self.legend[indx]


            seaborn_df = pd.concat(seaborn_df_list)
            return seaborn_df
    

    def plot_data_seaborn(self, data_p):
        """
        Plot data using seaborn
        """
        data_p.index = [i for i in range(data_p.shape[0])]
        # data_p = data_p[~data_p.index.duplicated()]
        print(data_p)


        sns.boxplot(x=self.used_column[0], y='Value', hue='Legend',
                    data=data_p[data_p['Metric'] == self.used_column[1]],
                    order=self.x_order)
        plt.xlabel(self.xy_labels[0])
        plt.ylabel(self.xy_labels[1])



"""
Example
"""

# Load the data from the CSV file into a Pandas DataFrame
# df = pd.read_csv('comparative_run.csv')

# Use the class to plot a diagram
# plot = Bar_Plot_Col(data_p=df, 
#                     title_p="test", 
#                     xy_labels_p=("Nb of tasks","Total Time"), 
#                     nb_bar_p=3, 
#                     used_columns_p=['Nb of tasks','Tot Distance','Tot Distance.1', 'Tot time'], 
#                     legend_p=["test1","test2", "test3"])