import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from mesh_interfaces.msg import FixedData
import time
import psutil

KILO = 1024
KILO2 = 2048
KILO4 = 4096
KILO8 = 8192
KILO16 = 16384
KILO32 = 32768
KILO64 = 65536
KILO128 = 131072
KILO256 = 262144
KILO512 = 524288
MEGA = 1048576
MEGA2 = 2097152
MEGA4 = 4194304
MEGA8 = 8388608
MEGA16 = 16777216
MEGA32 = 33554432
MEGA64 = 67108864
MEGA128 = 134217728
MEGA256 = 268435456
MEGA512 = 536870912
GIGA = 1073741824

MAX_SIZE = MEGA  # Set a reasonable limit for maximum data size

class NetworkTestPublisher(Node):
    def __init__(self):
        super().__init__('network_test_publisher')

        self.declare_parameter('robot_name', 'leo02')
        self.robot_name = self.get_parameter('robot_name').get_parameter_value().string_value + '/'
        self.declare_parameter('size', 'KILO')
        self.data_size = self.get_parameter('size').get_parameter_value().string_value
        self.should_continue = True
        self.publisher_ = self.create_publisher(FixedData, self.robot_name + 'fixed_size_data', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.declare_parameter('exp_time', 20)  # Default to 60 seconds
        self.exp_time = self.get_parameter('exp_time').get_parameter_value().integer_value

        self.stop_timer = self.create_timer(self.exp_time, self.stop_callback)

        # Velocity publisher
        self.cmd_publisher_ = self.create_publisher(Twist, self.robot_name + 'cmd_vel', 10)

    def stop_callback(self):
        twist = Twist()
        twist.linear.x = 0.0
        self.cmd_publisher_.publish(twist)
        self.get_logger().info('Experiment time over, shutting down...')
        self.should_continue = False

    def timer_callback(self):
        try:
            size_in_bytes = self.get_global_var(self.data_size)

            # Send data
            msg = FixedData()
            self.get_logger().info(f'Publishing a message of size {size_in_bytes} bytes')
            msg.data = 'a' * (size_in_bytes - 8)  # create a string of the desired size minus the size of the header
            msg.millisec = int(round(time.time() * 1000))
            self.publisher_.publish(msg)

            # Send velocity commands
            twist = Twist()
            twist.linear.x = 0.5
            self.cmd_publisher_.publish(twist)

            # Log memory usage
            process = psutil.Process()
            mem_info = process.memory_info()
            self.get_logger().info(f'Memory usage: RSS={mem_info.rss} bytes, VMS={mem_info.vms} bytes')

        except Exception as e:
            self.get_logger().error(f'Error in timer_callback: {str(e)}')

    def get_global_var(self, name):
        return globals()[name]


def main(args=None):
    rclpy.init(args=args)

    network_test_publisher = NetworkTestPublisher()

    while rclpy.ok() and network_test_publisher.should_continue:
        rclpy.spin_once(network_test_publisher)

    network_test_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
