import subprocess
import multiprocessing as mp
import os
import argparse
from colorama import Fore, Style


class MetaMonitoring:

    def __init__(self, experiment_name_p, experiment_duration_p=30, experiment_timestep_p=0.1, is_robot_p=False, robot_name_p="leo02", monitoring_path_p="", database_path_p="", process_number_p=1) -> None:
        if monitoring_path_p == None:
            self.monitoring_path = os.getcwd()
        else:
            self.monitoring_path = monitoring_path_p
        
        if database_path_p == None or database_path_p == '':
            self.database_path = os.getcwd() + "/dataset"
        else:
            self.database_path = database_path_p
        
        self.is_robot = is_robot_p
        self.robot_name = robot_name_p
        if self.is_robot:
            self.experiment_name = experiment_name_p + f"_{self.robot_name}"
        else:
            self.experiment_name = experiment_name_p + "_local"
        self.experiment_duration = experiment_duration_p
        self.experiment_timestep = experiment_timestep_p
        self.process_number = process_number_p
        self.function_name = [self.global_monitoring, self.point_cloud_data_monitoring, self.point_cloud_logger_monitoring]
        self.results = []
        self.queue = mp.Queue()
        self.execute()
        self.cleanup()
        self.display_result()
        exit()
        
    
    def execute(self):
        """
        Execute in parallel the monitoring 
        """
        self.processes = []
        if self.is_robot:
            arguments = [self.robot_name]
            
            for proc_index in range(self.process_number):
                if proc_index != 2:
                    self.create_process(self.function_name[proc_index]) # Global and data point cloud monitoring
                else:
                    self.create_process(self.function_name[proc_index], arguments[0]) # Logger point cloud monitoring
            
        else:
            arguments = ['leo02', 'leo03']

            for proc_index in range(self.process_number):
                if proc_index > 0:
                    pass
                    self.create_process(self.function_name[2], str(arguments[proc_index-1])) # Point cloud monitoring
                else:
                    self.create_process(self.function_name[proc_index]) # Global monitoring

        self.get_results()


    def create_process(self, name_p, args_p=None):
        """
        Create and start the processes with the arguments:
        - name_p: Name of the function to execute in the process
        - arg_p: Arguments of the function
        """
        if args_p:
            process = mp.Process(target=name_p, args=args_p)
            self.processes.append(process)
            process.start()
        else:
            process = mp.Process(target=name_p)
            self.processes.append(process)
            process.start()
    

    def global_monitoring(self):
        result = subprocess.run(["python3", f"{self.monitoring_path}/monitoring.py", f"{self.experiment_name}", f"{self.experiment_duration}", f"{self.experiment_timestep}", "-database_path", f"{self.database_path}"], cwd=os.path.expanduser('~'), capture_output=True, text=True)
        self.queue.put(result)


    def point_cloud_data_monitoring(self):
        result = self.result_script_2 = subprocess.run(["ros2", "run", "mesh", "exp", "pc_data"])
        self.queue.put(result)
    

    def point_cloud_logger_monitoring(self, *name_p):
        if type(name_p) == tuple:
            name = ''.join(name_p)
        else:
            name = name_p
        result = subprocess.run(["ros2", "run", "mesh", "exp", "pc_logger", "--ros-args", "-p", f"robot_name:={name}", "-p", f"experiment_name:={self.experiment_name}"])
        self.queue.put(result)


    def display_result(self):
        """
        Print the output of the subprocess function
        """
        for result in self.results:
                print(f"Result of process {self.experiment_name}:")
                if not result.stderr:
                    print(Fore.GREEN + str(result.stdout))
                    print(Style.RESET_ALL)
                else:
                    print(Fore.RED + "Error:")
                    print(Fore.RED + str(result.stderr))
                    print(Style.RESET_ALL)


    def get_results(self):
        """
        Collect the results from the queue
        """
        self.results = []
        for _ in range(self.process_number):
            result = self.queue.get()
            self.results.append(result)


    def cleanup(self):
        """
        Wait for all processes to finish
        """
        for process in self.processes:
            process.join()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                                description="Meta monitoring class. Used as an intermediate node to manage 'Monitoring' class",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("name", help="Experiment's name", type=str)
    parser.add_argument("duration", help="Experiment's duration", type=float)
    parser.add_argument("step", help="Experiment's timestep measure", type=float)
    parser.add_argument("-r", "--remote", action="store_true", help="If used, specify the remote status of the script")

    parser.add_argument("-target", help="Name of the remote target device", type=str)
    parser.add_argument("-monitoring_script_path", help="Path of the monitoring script to run", type=str)
    parser.add_argument("-database_path", help="Path of the database location", type=str)
    parser.add_argument("-process_number", help="Number of process (monitoring scripts) per robot", default=1, type=int)
    
    args = parser.parse_args()
    config = vars(args)
    meta_monitoring = MetaMonitoring(experiment_name_p=config['name'], 
                                     experiment_duration_p=config['duration'], 
                                     experiment_timestep_p=config['step'],
                                     is_robot_p=config['remote'],
                                     robot_name_p=config['target'],
                                     monitoring_path_p=config['monitoring_script_path'],
                                     database_path_p=config['database_path'],
                                     process_number_p=config['process_number'])