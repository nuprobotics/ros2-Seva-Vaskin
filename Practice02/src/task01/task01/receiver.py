import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Receiver(Node):
    def __init__(self):
        super().__init__('receiver')
        self.subscription = self.create_subscription(
            String,
            '/spgc/sender',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received message: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    receiver = Receiver()

    try:
        rclpy.spin(receiver)
    except KeyboardInterrupt:
        pass
    finally:
        receiver.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
