import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from datetime import datetime

class AlertLogger(Node):
    def __init__(self):
        super().__init__('Alert_Logger')
        self.subscription_=self.create_subscription(String,'alerts',self.alert_callback,10)
        self.alert_log=[]
        self.get_logger().info('Alert_Logger Started -montioring for alerts...')

    def alert_callback(self,msg):
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry=f'[{timestamp}] {msg.data}'
        self.alert_log.append(log_entry)
        self.get_logger().error(f'Logged: {msg.data}')
        self.get_logger().info(f'Total alerts logged:{len(self.alert_log)}')



def main(args=None):
    rclpy.init(args=args)
    node=AlertLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()