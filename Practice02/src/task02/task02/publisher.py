import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')

        # Declare and get parameters
        self.declare_parameter('text', 'Hello, ROS2!')
        self.text = self.get_parameter('text').string_value

        # Load topic name from the config file
        self.declare_parameter('topic_name', '/spgc/receiver')
        topic_name = self.get_parameter('topic_name').string_value

        # Create publisher
        self.publisher_ = self.create_publisher(String, topic_name, 10)

        # Create a timer to publish the message every second (1 Hz)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = self.text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published message: "{msg.data}"')

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
