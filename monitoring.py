import psutil
import csv
import os
import time
import argparse


class Monitoring:

    def __init__(self, experiment_name_p, experiment_duration_p=30, experiment_timestep_p=0.1, database_path_p="~/dataset"):
        """
        Defaults attributes of the monitoring class are:
        - Experiment duration : 30 seconds
        - Experiment timestep : 10 Hz (0.1 second)
        """
        self.starting_time = int(round(time.time() * 1000))
        self.experiment_name = experiment_name_p+"_global_monitoring"
        self.experiment_duration = float(experiment_duration_p)
        self.experiment_timestep = float(experiment_timestep_p)
        self.data = []
        self.old_network_data = None
        self.new_network_data = None
        if database_path_p == None or database_path_p == '':
            self.path = os.getcwd()+"/dataset"
        else:
            self.path = os.path.expanduser(database_path_p)
        self.create_csv(self.experiment_name)
        self.get_data()
        exit()


    def check_dataset_directory(self):
        """
        Check if the dataset directory exist
        If not, create it
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def create_csv(self, experiment_name_p):
        """
        Create the csv file with the correct fields for the given experiment (name_p)
        """
        self.check_dataset_directory()
        with open(f"{self.path}/{experiment_name_p}.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Bytes_Send", "Bytes_Received", "Packets_Send", "Packets_Received", "Errors_Send", "Errors_Received", "Drop_Incoming", "Drop_total", "CPU_Usage"])


    def write_csv(self, force_p=False):
        """
        Add data to the already created csv file
        Return an error if the file was not created
        """
        #Checks
        self.check_dataset_directory()
        path = f"{self.path}/{self.experiment_name}.csv"

        if os.path.isfile(path) or force_p:
            with open(path, 'a',  encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.data)
        else:
            raise Exception('The csv file was not created, please create it first')
        

    def cpu_measure(self):
        """
        Measure the cpu usage (percentage)
        """
        cpu_usage = psutil.cpu_percent(interval=self.experiment_timestep)
        return cpu_usage
        

    def network_measure(self):
        """
        Measure the network usage
        """
        network_result = []

        self.new_network_data = psutil.net_io_counters()

        if self.old_network_data == None:
            self.old_network_data = self.new_network_data

        # Get sent bytes
        network_result.append(self.new_network_data.bytes_sent - self.old_network_data.bytes_sent)

        # Get received bytes
        network_result.append(self.new_network_data.bytes_recv - self.old_network_data.bytes_recv)

        # Get sent packets
        network_result.append(self.new_network_data.packets_sent - self.old_network_data.packets_sent)

        # Get received packets
        network_result.append(self.new_network_data.packets_recv - self.old_network_data.packets_recv)

        # Get errors while sending
        network_result.append(self.new_network_data.errout - self.old_network_data.errout)

        # Get errors while receiving
        network_result.append(self.new_network_data.errin - self.old_network_data.errin)

        # Get total number of incoming packets which were dropped
        network_result.append(self.new_network_data.dropin - self.old_network_data.dropin)

        # Get total number of outgoing packets which were dropped
        network_result.append(self.new_network_data.dropout - self.old_network_data.dropout)

        self.old_network_data = self.new_network_data

        return network_result


    def get_data(self):
        """
        Get the measurement
        """
        start_time = time.time()
        stop = False
        while not stop:
            self.data = []
            network_result = self.network_measure()
            self.data.append(int(round(time.time() * 1000)) - self.starting_time)
            self.data.append(network_result[0])
            self.data.append(network_result[1])
            self.data.append(network_result[2])
            self.data.append(network_result[3])
            self.data.append(network_result[4])
            self.data.append(network_result[5])
            self.data.append(network_result[6])
            self.data.append(network_result[7])
            self.data.append(self.cpu_measure())
            
            self.write_csv()
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.experiment_duration:
                stop=True
        
        print("Experiment concluded")
        self.write_csv()



if __name__ == "__main__":  
    parser = argparse.ArgumentParser(
                                description="Meta monitoring class. Used as an intermediate node to manage 'Monitoring' class",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("name", help="Experiment's name", type=str)
    parser.add_argument("duration", help="Experiment's duration", type=float)
    parser.add_argument("step", help="Experiment's timestep measure", type=float)
    parser.add_argument("-database_path", help="Path of the database location", default='~/dataset', type=str)
    
    args = parser.parse_args()
    config = vars(args)
    
    monitoring = Monitoring(config['name'], 
                            config['duration'], 
                            config['step'],
                            config['database_path'])
