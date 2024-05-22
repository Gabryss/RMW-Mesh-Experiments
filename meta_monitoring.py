import subprocess
import multiprocessing as mp
import os
import argparse
from colorama import Fore, Style
from config import Config


class MetaMonitoring:

    def __init__(self, experiment_name_p, experiment_duration_p=30, experiment_timestep_p=0.1, is_robot_p=False, robot_name_p="bob", packet_size_p=None, target_p="", rmw_implementation_p="rmw_fastrtp_cpp") -> None:
        
        self.database_path = Config.DATASET_PATH.value
        
        self.is_robot = is_robot_p
        self.robot_name = robot_name_p
        self.target_name = target_p
        print(Fore.CYAN + f"Target name {self.target_name}, my name {self.robot_name}" + Style.RESET_ALL)
        self.is_target = (self.target_name == self.robot_name)
        if self.is_robot:
            self.experiment_name = experiment_name_p + f"_{self.robot_name}"
        else:
            self.experiment_name = experiment_name_p + "_local"
        self.zenoh = False
        self.ros_ws_path = Config.PROJECT_PATH.value + "/exp_ws"
        self.ros_distro = "iron"
        self.packet_size = packet_size_p
        self.experiment_duration = experiment_duration_p
        self.experiment_timestep = experiment_timestep_p
        self.rmw_implementation = rmw_implementation_p
        if self.rmw_implementation == "rmw_zenoh_cpp":
            self.zenoh = True
        
        self.process_number = 0
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

        print(Fore.CYAN + f"Execute called is robot {self.is_robot}, is_target {self.is_target}" + Style.RESET_ALL)
        self.processes = []
        self.create_process(self.global_monitoring)

        if self.is_robot and self.is_target:
            arguments = [self.robot_name]
            self.create_process(self.byte_sender, arguments[0])

        elif not self.is_robot:
            arguments = [Config.TARGET.value] # replace with target
            if self.zenoh:
                zenoh_process = mp.Process(target=self.zenoh_router, args=['2'])
                zenoh_process.daemon = True                                         # Tell the script to continue without waiting for zenoh result
                zenoh_process.start()

            self.create_process(self.byte_logger, arguments[0])

        self.get_results()


    def create_process(self, name_p, args_p=None):
        """
        Create and start the processes with the arguments:
        - name_p: Name of the function to execute in the process
        - arg_p: Arguments of the function
        """
        self.process_number += 1
        if args_p:
            process = mp.Process(target=name_p, args=args_p)
            self.processes.append(process)
            process.start()
        else:
            process = mp.Process(target=name_p)
            self.processes.append(process)
            process.start()


    def zenoh_router(self, *router_id_p):
        """
        Activate zenoh router
        """
        router_id = ''.join(router_id_p)
        home = os.path.expanduser('~')
        cmd = f"bash -c 'source /opt/ros/iron/setup.bash && source {home}/zenoh_ws/install/setup.bash && export ZENOH_ROUTER_CONFIG_URI={Config.PROJECT_PATH.value}/zenoh_config.json5 && ros2 run rmw_zenoh_cpp rmw_zenohd'"
        print(f"Zenoh router command: {cmd}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        self.queue.put(result)


    def global_monitoring(self):
        if self.is_target:
            is_tar = 1
        else:
            is_tar = 0
        result = subprocess.run(["python3", f"{Config.PROJECT_PATH.value}/monitoring.py", f"{self.experiment_name}", f"{self.experiment_duration}", f"{self.experiment_timestep}", f"{str(is_tar)}"], cwd=os.path.expanduser('~'), capture_output=True, text=True)
        self.queue.put(result)


    def byte_sender(self, *name_p):
        if type(name_p) == tuple:
            name = ''.join(name_p)
        else:
            name = name_p
        print(f"Byte sender called")
        home = os.path.expanduser('~')
        if self.zenoh:
            cmd = f"bash -c 'source {home}/zenoh_ws/install/local_setup.bash && source {self.ros_ws_path}/install/local_setup.bash && ROS_DOMAIN_ID=51 && export RMW_IMPLEMENTATION={self.rmw_implementation} && ros2 run mesh_exp byte_sender --ros-args -p robot_name:={name} -p size:={self.packet_size} -p exp_time:={int(self.experiment_duration)}'"
        else:
            cmd = f"bash -c 'source {self.ros_ws_path}/install/setup.bash && export CYCLONEDDS_URI={Config.PROJECT_PATH.value}/cyclone_config_leo.xml && ROS_DOMAIN_ID=51 && export RMW_IMPLEMENTATION={self.rmw_implementation} && ros2 run mesh_exp byte_sender --ros-args -p robot_name:={name} -p size:={self.packet_size} -p exp_time:={int(self.experiment_duration)}'"

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        self.queue.put(result)
    

    def byte_logger(self, *name_p):
        if type(name_p) == tuple:
            name = ''.join(name_p)
        else:
            name = name_p
        home = os.path.expanduser('~')
        if self.zenoh:
            cmd = f"bash -c 'source /opt/ros/{self.ros_distro}/setup.bash && source {self.ros_ws_path}/install/setup.bash && source {home}/zenoh_ws/install/setup.bash && export RMW_IMPLEMENTATION={self.rmw_implementation} && ROS_DOMAIN_ID=51 && ros2 run mesh_exp byte_logger --ros-args -p robot_name:={name} -p experiment_name:={self.experiment_name} -p exp_time:={int(self.experiment_duration)}'"
        else:
            cmd = f"bash -c 'source /opt/ros/{self.ros_distro}/setup.bash && source {self.ros_ws_path}/install/setup.bash && export CYCLONEDDS_URI={Config.PROJECT_PATH.value}/cyclone_config.xml && export RMW_IMPLEMENTATION={self.rmw_implementation} && ROS_DOMAIN_ID=51 && ros2 run mesh_exp byte_logger --ros-args -p robot_name:={name} -p experiment_name:={self.experiment_name} -p exp_time:={int(self.experiment_duration)}'"
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        self.queue.put(result)


    def display_result(self):
        """
        Print the output of the subprocess function
        """
        for result in self.results:
                print(f"Result of process {self.experiment_name}:")
                if result.stdout:
                    print(Fore.GREEN + str(result.stdout))
                    print(Style.RESET_ALL)
                if result.stderr:
                    print(Fore.RED + "Error:")
                    print(Fore.RED + str(result.stderr))
                    print(Style.RESET_ALL)


    def get_results(self):
        """
        Collect the results from the queue
        """
        self.results = []
        print("Number of results", self.process_number)
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
    parser.add_argument("-r", "--remote", action="store_true", help="If used, specify to the executed script that it is on a robot")
    parser.add_argument("-z",  "--zenoh", action="store_true", help="If used, use Zenoh")
    parser.add_argument("--robot_name", help="Name of the robot", type=str)
    parser.add_argument("--rmw_implementation", help="RMW implementation to use", type=str)

    parser.add_argument("-target", help="Name of the remote target device", type=str)
    parser.add_argument("-packet_size", help="Size of the sending packet for the corresponding monitoring script", type=str)


    args = parser.parse_args()
    config = vars(args)
    meta_monitoring = MetaMonitoring(experiment_name_p=config['name'], 
                                     experiment_duration_p=config['duration'], 
                                     experiment_timestep_p=config['step'],
                                     is_robot_p=config['remote'],
                                     robot_name_p=config['robot_name'],
                                     packet_size_p=config['packet_size'],
                                     rmw_implementation_p=config['rmw_implementation'],
                                     target_p=config['target'])