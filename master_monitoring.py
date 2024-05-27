import paramiko
import sys
import threading
import subprocess
import os
from colorama import Fore, Style
from config import Config


class MasterMonitoring:

    def __init__(self) -> None:
        self.host_list = Config.ROBOTS_HOST_LIST.value
        self.robot_name_list = Config.ROBOTS_NAME_LIST.value
        self.rmw_implementation = Config.RMW_IMPLEMENTATION.value
        self.results = []
        self.nb_connection = len(Config.ROBOTS_HOST_LIST.value)
        self.start_threading()
        exit()


    def start_threading(self):
        """
        Start the multi threading logic
        """
        print(Fore.CYAN + "Starting the overall monitoring")
        print(Style.RESET_ALL)
        self.threads = []

        # Remote robots
        if Config.USE_REMOTE.value:
            for thread_index in range(self.nb_connection):
                thread = threading.Thread(target=self.run_remote_script, args=[self.robot_name_list[thread_index], self.host_list[thread_index]])
                thread.start()
                self.threads.append(thread)

        # Local
        if Config.USE_LOCAL.value:
            thread = threading.Thread(target=self.run_local_script)         
            thread.start()
            self.threads.append(thread)

        # Wait for all threads to complete
        for thread in self.threads:
            thread.join()
        
        print(Fore.CYAN + "\nAll scripts executed")
        print(Style.RESET_ALL)


    def run_remote_script(self, *args_p):
        """
        Execute scripts on the robots using ssh connection.
        This master monitoring will launch the meta_monitoring scripts on the given robots (see config file).
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        name = str(Config.EXPERIMENT_NAME.value).replace(' ','_')
        duration = Config.EXPERIMENT_TIME.value
        step = Config.EXPERIMENT_TIMESTEP.value
        remote_dir_path = Config.REMOTE_WS_PATH.value
        username = Config.REMOTE_USERNAME.value
        password = Config.REMOTE_PASSWORD.value
        robot_name = args_p[0]
        host = str(args_p[1])

        try:
            # Connect to the remote host
            ssh.connect(host, username=username, password=password, timeout=Config.REMOTE_SSH_TIMEOUT.value, auth_timeout=Config.REMOTE_SSH_TIMEOUT.value)
            print(Fore.MAGENTA + f"My name is {robot_name}")
            print(f"target is {Config.TARGET.value}")
            print(Style.RESET_ALL)
            stdin, stdout, stderr = ssh.exec_command(f"source /opt/ros/iron/setup.bash && export ROS_DOMAIN_ID=1 && python3 {remote_dir_path}/meta_monitoring.py {name} {duration} {step} -r -packet_size {Config.PACKET_SIZE.value} -target {Config.TARGET.value} --robot_name {robot_name} --rmw_implementation {self.rmw_implementation}")

            # Wait for script execution to complete
            exit_status = stdout.channel.recv_exit_status()

            # Process the output as needed
            output = stdout.read().decode()
            
            # Print the output
            print(Fore.LIGHTYELLOW_EX + "\n\n\n\n=================================")
            print(Style.RESET_ALL)
            print("Remote output of : " + robot_name)
            print(Fore.GREEN + output)
            print(Style.RESET_ALL)
            print(f"Exit status: {exit_status}")


            # Print any errors
            error = stderr.read().decode().strip()
            if error:
                print(Fore.RED + "Errors:")
                print(Fore.RED + error)
                print(Style.RESET_ALL)
            
            print(Fore.LIGHTYELLOW_EX + "=================================")
            print(Style.RESET_ALL)


            print(Fore.CYAN + "\nRetreive dataset...\n")
            print(Style.RESET_ALL)

            sftp = ssh.open_sftp()

            self.copy_directory(sftp_p=sftp, local_dir_p=os.path.expanduser(Config.DATASET_PATH.value), remote_dir_p=Config.REMOTE_DATASET_PATH.value)            

        except Exception as e:
            print(Fore.RED + f"An error occurred during connection: {e}")
            print(Style.RESET_ALL)
            ssh.close()

        finally:
            ssh.close()


    def run_local_script(self):
        """
        Launch the meta_monitoring script that run on the local computer.
        """
        exp_name = str(Config.EXPERIMENT_NAME.value).replace(' ','_')
        exp_duration = str(Config.EXPERIMENT_TIME.value)
        exp_step = str(Config.EXPERIMENT_TIMESTEP.value)
        
        try:
            result = subprocess.run(["python3", f"{Config.PROJECT_PATH.value}/meta_monitoring.py", f"{exp_name}", f"{exp_duration}", f"{exp_step}", "-packet_size", f"{Config.PACKET_SIZE.value}", "--robot_name", "local", "--rmw_implementation",  f"{self.rmw_implementation}"], cwd=os.path.expanduser('~'), capture_output=True, text=True)
        
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        
        print(Fore.LIGHTYELLOW_EX + "\n\n\n\n=================================")
        print(Style.RESET_ALL)
        print("Local output:")
        print(result.stdout)

        # Print any errors
        error = result.stderr
        if error:
                print(Fore.RED + "Errors:")
                print(Fore.RED + error)
                print(Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + "=================================")
        print(Style.RESET_ALL)


    def copy_directory(self, sftp_p, local_dir_p, remote_dir_p, file_count_p=0):
        """
        Copy everything included in a directory
        - sftp connexion
        - local directory
        - remote directory
        - file_count (optional, only used by the script)
        """
        sftp = sftp_p
        local_directory = local_dir_p
        remote_directory = remote_dir_p
        file_count = file_count_p
        error=False


        # Create the local directory for the database if it doesn't exist
        os.makedirs(local_directory, exist_ok=True)
        
        for item in sftp.listdir_attr(remote_directory):
            remote_item_path = remote_directory + "/" + item.filename
            local_item_path = os.path.join(local_directory, item.filename)

            if item.st_mode & 0o4000:  # Check if it's a directory
                
                os.makedirs(local_item_path, exist_ok=True)
                self.copy_directory(sftp_p=sftp, local_dir_p=local_item_path, remote_dir_p=remote_item_path, file_count_p=file_count)

            if not Config.GET_ENTIRE_DATABASE.value and os.path.isfile(local_item_path):
                continue
            
            else:  # It's a file
                try:
                    file_count+=1
                    sftp.get(remote_item_path, local_item_path)
                    
                except Exception as e:
                    error = True
                    print(Fore.RED + f"Error occurred while downloading the file: {str(e)}")
                    print(Style.RESET_ALL)
        
        # End message
        if not error:
            print(Fore.CYAN + f"End of dataset retreiving, {file_count} files downloaded")
            print(Style.RESET_ALL)
        else:
            print(Fore.CYAN + "A number of issues occured during file transfer")
            print(Style.RESET_ALL)



if __name__ == "__main__":  
    arguments = sys.argv
    num_arguments = len(arguments) - 1

    if num_arguments >= 1:
        print("Please take a look at the config file in order to change or add new configuration/behaviours")
    else:
        master = MasterMonitoring()