import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from mesh_interfaces.msg import FixedData
import csv
import os
import time


class ByteLogger(Node):
    """
    Only log data if a message is received
    """
    def __init__(self):
        super().__init__('minimal_subscriber')

        self.declare_parameter('robot_name', 'leo02')
        self.robot_namespace =  self.get_parameter('robot_name').get_parameter_value().string_value + '/'
        self.declare_parameter('experiment_name', 'test')
        self.experiment_name = self.get_parameter('experiment_name').get_parameter_value().string_value + "_delay"
        self.initial_time = int(round(time.time() * 1000))
        self.declare_parameter('exp_time', 60)  # Default to 60 seconds
        self.exp_time = self.get_parameter('exp_time').get_parameter_value().integer_value
        self.get_logger().info(f'{self.exp_time}')
        self.stop_timer = self.create_timer(self.exp_time, self.stop_callback)
        self.should_continue = True
        self.my_subscriber = self.create_subscription(
            FixedData,
            self.robot_namespace+'fixed_size_data',
            self.listener_callback,
            10)
        # prevent warning that self.my_subscriber is not used
        self.my_subscriber

        self.path = os.path.expanduser('~/mesh_exp/dataset')
        self.create_csv()

    def check_dataset_directory(self):
        """
        Check if the dataset directory exist
        If not, create it
        """
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def stop_callback(self):
        self.get_logger().info('Experiment time over, shutting down...')
        self.should_continue = False


    def create_csv(self):
        """
        Create the csv file with the correct fields for the given experiment (name_p)
        """
        self.check_dataset_directory()
        with open(f"{self.path}/{self.experiment_name}.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['TimeStamp', 'Delay', 'Size'])


    def write_csv(self,data, force_p=False):
        """
        Add data to the already created csv file
        Return an error if the file was not created
        """

        #Checks
        self.check_dataset_directory()
        path = f"{self.path}/{self.experiment_name}.csv"

        if os.path.isfile(path) or force_p:
            with open(path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        else:
            raise Exception('The csv file was not created, please create it first')


    def listener_callback(self, msg):
        """
        Every time a message is received, fill the CSV file with it
        """
        now = self.get_clock().now()
        current_time_float = now.nanoseconds * 1e-9
        print(f"Current time: {current_time_float}")
        sent_time_float = msg.millisec * 1e-3
        print(f"Sent time: {sent_time_float}")
        delay = current_time_float - sent_time_float
        size = len(msg.data)
        timestamp = int(round(time.time() * 1000)) - self.initial_time 
        print(f"Timestamp: {timestamp}")
        print(f"Second Timestamp: {float(timestamp)/1000}")
        print(f"Delay: {delay}")
        self.write_csv([timestamp,delay, size])
        
 
 
def main(args=None):
    rclpy.init(args=args)
 
    my_simple_subscriber = ByteLogger()
    while rclpy.ok() and my_simple_subscriber.should_continue:
        rclpy.spin_once(my_simple_subscriber)

    # destroy the node when it is not used anymore
    my_simple_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()