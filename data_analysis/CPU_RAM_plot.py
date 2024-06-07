"""
Plot the CPU and RAM usage of the ROS 2 processes during the RMW mesh experiments
"""
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

PATH = str(pathlib.Path(__file__).parent.resolve()) + '/data/Cleaned/fast/fast_KILO8'
EXP = 2


class CPU_RAM_Plot:

    def __init__(self, path_p) -> None:
        self.path = path_p
        self.df_sender = pd.read_csv(self.path+f'/fastrtps_KILO8_exp_{str(EXP)}_leo02_global_monitoring.csv')
        self.df_receiver = pd.read_csv(self.path+f'/fastrtps_KILO8_exp_{str(EXP)}_local_global_monitoring.csv')
        self.format_data()


    def format_data(self):
        """
        Format the Dataframe object into a numpy array that can be ploted by Matplotlib
        """
        # Sender
        self.time_sender = self.df_sender["Timestamp"].to_numpy()
        self.cpu_p_sender = self.df_sender["CPU_percent"].to_numpy()
        self.cpu_t_sender = self.df_sender["CPU_time"].to_numpy()
        self.ram_p_sender = self.df_sender["RAM_percent"].to_numpy()
        self.ram_i_sender = self.df_sender["RAM_info"].to_numpy()        

        # Receiver
        self.time_receiver = self.df_receiver["Timestamp"].to_numpy()
        self.cpu_p_receiver = self.df_receiver["CPU_percent"].to_numpy()
        self.cpu_t_receiver = self.df_receiver["CPU_time"].to_numpy()
        self.ram_p_receiver = self.df_receiver["RAM_percent"].to_numpy()
        self.ram_i_receiver = self.df_receiver["RAM_info"].to_numpy()


    def plot_p_ram(self):
        """
        Plot the RAM usage of the sender and receiver during the experiment 
        """
        fig, ax = plt.subplots()
        ax.plot(self.time_sender,self.ram_p_sender, label='Sender')
        ax.plot(self.time_receiver, self.ram_p_receiver, label='Receiver')

        ax.set_title("RAM percentage usage")
        
        # Update layout
        ax.set_xlabel("Time")
        ax.set_ylabel("RAM(%)")
        ax.legend(loc='best')
    

    def plot_i_ram(self):
        """
        Plot the RAM usage of the sender and receiver during the experiment 
        """
        fig, ax = plt.subplots()
        ax.plot(self.time_sender,self.ram_i_sender, label='Sender')
        ax.plot(self.time_receiver, self.ram_i_receiver, label='Receiver')

        ax.set_title("RAM info usage")
        
        # Update layout
        ax.set_xlabel("Time")
        ax.set_ylabel("RAM(b)")
        ax.legend(loc='best')


    def plot_p_cpu(self):
        """
        Plot the CPU usage of the sender and receiver during the experiment
        """
        fig, ax = plt.subplots()
        ax.plot(self.time_sender,self.cpu_p_sender, label='Sender')
        ax.plot(self.time_receiver, self.cpu_p_receiver, label='Receiver')

        ax.set_title("CPU percentage usage")
        
        # Update layout
        ax.legend(loc='best')
        ax.set_xlabel("Time")
        ax.set_ylabel("CPU(%)")


    def plot_t_cpu(self):
        """
        Plot the CPU usage of the sender and receiver during the experiment
        """
        fig, ax = plt.subplots()
        ax.plot(self.time_sender,self.cpu_t_sender, label='Sender')
        ax.plot(self.time_receiver, self.cpu_t_receiver, label='Receiver')

        ax.set_title("CPU time usage")
        
        # Update layout
        ax.legend(loc='best')
        ax.set_xlabel("Time")
        ax.set_ylabel("CPU(s)")
    

    def plot_subgraph_all_cpu(self):
        """
        Plot together all data from the CPU
        """
        fig, ax = plt.subplots(2, sharex=True)
        fig.suptitle("CPU global usage")

        # Top graph
        ax[0].plot(self.time_sender,self.cpu_p_sender, label='Sender')
        ax[0].plot(self.time_receiver, self.cpu_p_receiver, label='Receiver')
        ax[0].set_ylabel("CPU percentage(%)")


        # Bottom graph
        ax[1].plot(self.time_sender,self.cpu_t_sender, label='Sender')
        ax[1].plot(self.time_receiver, self.cpu_t_receiver, label='Receiver')
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("CPU time(s)")


    def plot_subgraph_all_ram(self):
        """
        Plot together all data from the RAM
        """
        fig, ax = plt.subplots(2, sharex=True)
        fig.suptitle("RAM global usage")

        # Top graph
        ax[0].plot(self.time_sender,self.ram_p_sender, label='Sender')
        ax[0].plot(self.time_receiver, self.ram_p_receiver, label='Receiver')
        ax[0].set_ylabel("RAM(%)")


        # Bottom graph
        ax[1].plot(self.time_sender,self.ram_i_sender, label='Sender')
        ax[1].plot(self.time_receiver, self.ram_i_receiver, label='Receiver')
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("RAM(b)")

    
    def plot_subgraph_all_percentage(self):
        """
        Plot together all data related to percentage
        """
        fig, ax = plt.subplots(2, sharex=True)
        fig.suptitle("CPU and RAM percentage")

        # Top graph
        ax[0].plot(self.time_sender,self.cpu_p_sender, label='Sender')
        ax[0].plot(self.time_receiver, self.cpu_p_receiver, label='Receiver')
        ax[0].set_ylabel("CPU(%)")


        # Bottom graph
        ax[1].plot(self.time_sender,self.ram_p_sender, label='Sender')
        ax[1].plot(self.time_receiver, self.ram_p_receiver, label='Receiver')
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("RAM(%)")


    def plot_subgraph_all_other(self):
        """
        Plot together all data that are not related to percentage
        i.e RAM info and CPU time
        """
        fig, ax = plt.subplots(2, sharex=True)
        fig.suptitle("CPU time and RAM usage")

        # Top graph
        ax[0].plot(self.time_sender,self.cpu_t_sender, label='Sender')
        ax[0].plot(self.time_receiver, self.cpu_t_receiver, label='Receiver')
        ax[0].set_ylabel("CPU time(s)")


        # Bottom graph
        ax[1].plot(self.time_sender,self.ram_i_sender, label='Sender')
        ax[1].plot(self.time_receiver, self.ram_i_receiver, label='Receiver')
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("CPU time(s)")


if __name__ == "__main__":
    cpu_ram = CPU_RAM_Plot(path_p=PATH)
    cpu_ram.plot_i_ram()
    cpu_ram.plot_p_ram()
    cpu_ram.plot_p_cpu()
    cpu_ram.plot_t_cpu()
    cpu_ram.plot_subgraph_all_cpu()
    cpu_ram.plot_subgraph_all_ram()
    cpu_ram.plot_subgraph_all_percentage()
    cpu_ram.plot_subgraph_all_other()
    plt.show()

