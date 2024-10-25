import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')
        self.cb_group = ReentrantCallbackGroup()
        
        # Declare and get parameters
        self.declare_parameter('service_name', '/trigger_service')
        self.declare_parameter('default_string', 'No service available')
        
        self.service_name = self.get_parameter('service_name').value
        self.default_string = self.get_parameter('default_string').value
        
        # Store the returned string value
        self.stored_string = self.default_string
        
        # Create a client for the /spgc/trigger service
        self.client = self.create_client(Trigger, '/spgc/trigger', callback_group=self.cb_group)
        
        # Create a service
        self.srv = self.create_service(Trigger, self.service_name, self.trigger_callback, callback_group=self.cb_group)
        
        # Call the /spgc/trigger service
        self.call_trigger_service()

    def call_trigger_service(self):
        if not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Service /spgc/trigger not available')
            return
        
        request = Trigger.Request()
        future = self.client.call_async(request)
        future.add_done_callback(self.trigger_response_callback)

    def trigger_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.stored_string = response.message
                self.get_logger().info(f'Received message: {self.stored_string}')
            else:
                self.get_logger().warn('Service call was not successful')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {str(e)}')

    def trigger_callback(self, request, response):
        response.success = True
        response.message = self.stored_string
        return response

def main(args=None):
    rclpy.init(args=args)
    service_node = ServiceNode()
    executor = MultiThreadedExecutor()
    executor.add_node(service_node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        service_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
