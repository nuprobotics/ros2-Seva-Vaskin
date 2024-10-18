import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')

        # Declare and get parameters
        self.declare_parameter('text', 'Hello, ROS2!')
        text = self.get_parameter('text').value

        # Load topic name from the config file
        self.declare_parameter('topic_name', '/spgc/receiver')
        topic_name = self.get_parameter('topic_name').value

        # Create publisher
        self.publisher_ = self.create_publisher(String, topic_name, 10)

        # Publish the message
        msg = String()
        msg.data = text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published message: "{msg.data}" to topic: "{topic_name}"')

def main(args=None):
    rclpy.init(args=args)
    publisher = Publisher()

    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        pass
    finally:
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
