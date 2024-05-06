import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from mesh_interfaces.msg import PcData
import os
 
class PcSubPub(Node):
 
    def __init__(self):
        super().__init__('pointcloud_data')

        self.declare_parameter('robot_name', 'leo02')
        self.robot_namespace =  self.get_parameter('robot_name').get_parameter_value().string_value + '/'

        self.name  = os.environ.get('ROS_NAMESPACE')


        self.my_subscriber = self.create_subscription(
            PointCloud2,
            self.name+'/cloud_map',
            self.listener_callback,
            10)
        # prevent warning that self.my_subscriber is not used
        self.my_subscriber
        self.publisher_ = self.create_publisher(PcData, self.name+'/pc_delay', 10)
 
    def listener_callback(self, msg):
        pub_msg = PcData()
        pub_msg.sec = msg.header.stamp.sec
        pub_msg.nanosec = msg.header.stamp.nanosec
        #pub_msg.size = msg.row_step * msg.height
        point_step = msg.point_step  # size of each point in bytes
        num_points = len(msg.data) / point_step  # number of points
        pub_msg.size = int(num_points * point_step)  # total size
        self.publisher_.publish(pub_msg)
 
 
def main(args=None):
    rclpy.init(args=args)
 
    my_simple_subscriber = PcSubPub()
    rclpy.spin(my_simple_subscriber)
 
     # destroy the node when it is not used anymore
    my_simple_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == '__main__':
    main()