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
        self.username_list = Config.ROBOTS_USERNAME_LIST.value
        self.password_list = Config.ROBOTS_PASSWORD_LIST.value
        self.robot_name_list = Config.ROBOTS_NAME_LIST.value
        self.arguments = [str(Config.EXPERIMENT_NAME.value).replace(' ','_'), str(Config.EXPERIMENT_TIME.value), str(Config.EXPERIMENT_TIMESTEP.value)]
        self.results = []
        # self.lock = threading.Event()
        self.lock_barrier = threading.Barrier(Config.REMOTE_ROBOT_NUMBER.value+1)
        self.start_threading()


    def start_threading(self):
        """
        Start the multi threading logic
        """
        print(Fore.CYAN + "Starting the overall monitoring")
        print(Style.RESET_ALL)
        self.threads = []

        # Remote robots
        if Config.USE_REMOTE.value:
            for thread_index in range(Config.REMOTE_ROBOT_NUMBER.value):
                thread = threading.Thread(target=self.run_remote_script, args=self.arguments+[self.robot_name_list[thread_index], Config.REMOTE_MONITORING_DIR.value, Config.REMOTE_DATASET_PATH.value, self.host_list[thread_index], self.username_list[thread_index], self.password_list[thread_index]])
                thread.start()
                self.threads.append(thread)

        # Local
        if Config.USE_LOCAL.value:
            thread = threading.Thread(target=self.run_local_script, args=self.arguments+[Config.LOCAL_MONITORING_DIR.value])         
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
        name = args_p[0]
        duration = args_p[1]
        step = args_p[2]
        target_name = args_p[3]
        remote_dir_path = args_p[4]
        database_path = args_p[5]
        host = str(args_p[6])
        username = str(args_p[7])
        password = str(args_p[8])
        try:
            # Connect to the remote host
            ssh.connect(host, username=username, password=password)
            
            # Wait for all scripts to be ready
            # self.lock_barrier.wait()

            # Signal that the connection with the remote script is established
            # self.lock.set()
            # print("Lock passed")


            stdin, stdout, stderr = ssh.exec_command(f"python3 {Config.REMOTE_MONITORING_DIR.value}/meta_monitoring.py {name} {duration} {step} -r -target {target_name} -monitoring_script_path {remote_dir_path} -database_path {database_path}")

            # Wait for script execution to complete
            exit_status = stdout.channel.recv_exit_status()

            # Process the output as needed
            output = stdout.read().decode()
            
            # Print the output
            print(Fore.LIGHTYELLOW_EX + "\n\n\n\n=================================")
            print(Style.RESET_ALL)
            print("Remote output of : " + target_name)
            print(Fore.GREEN + output)
            print(Style.RESET_ALL)
            print(f"Exit status: {exit_status}")


            # Print any errors
            error = stderr.read().decode().strip()
            if error:
                print(Fore.RED + "Error:")
                print(Fore.RED + error)
                print(Style.RESET_ALL)
            
            print(Fore.LIGHTYELLOW_EX + "=================================")
            print(Style.RESET_ALL)


            print(Fore.CYAN + "\nRetreive dataset...\n")
            print(Style.RESET_ALL)

            sftp = ssh.open_sftp()

            self.copy_directory(sftp_p=sftp, local_dir_p=os.path.expanduser(Config.LOCAL_DATASET_PATH.value), remote_dir_p=os.path.expanduser(Config.REMOTE_DATASET_PATH.value))            

        except Exception as e:
            print(Fore.RED + f"An error occurred during connection: {e}")
            print(Style.RESET_ALL)
            ssh.close()

        finally:
            ssh.close()


    def run_local_script(self, *arg_p):
        """
        Launch the meta_monitoring script that run on the local computer.
        """
        exp_name = arg_p[0]
        exp_duration = arg_p[1]
        exp_step = arg_p[2]
        exp_path = arg_p[3]
        if Config.USE_REMOTE.value:
            self.lock_barrier.wait()
        result = subprocess.run(["python3", f"{Config.LOCAL_MONITORING_DIR.value}/meta_monitoring.py", f"{exp_name}", f"{exp_duration}", f"{exp_step}", "-monitoring_script", f"{exp_path}", "-database_path", f"{Config.LOCAL_DATASET_PATH.value}"], cwd=os.path.expanduser('~'), capture_output=True, text=True)
        
        print(Fore.LIGHTYELLOW_EX + "\n\n\n\n=================================")
        print(Style.RESET_ALL)
        print("Local output:")
        print(result.stdout)

        # Print any errors
        error = result.stderr
        if error:
                print(Fore.RED + "Error:")
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
        os.makedirs(Config.REMOTE_DATASET_PATH.value, exist_ok=True)
        
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