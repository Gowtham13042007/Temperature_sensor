import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32,String
from my_robot_interfaces.srv import Setbool


class MonitorNode(Node):
     def __init__(self):
         super().__init__('Monitor_Node')
         self.declare_parameter('temp_threshold',28.0)
         self.temp_threshold=self.get_parameter('temp_threshold').value
         self.subscription_=self.create_subscription(Float32,'temperature',self.temperature_callback,20)
         self.alert_publisher=self.create_publisher(String,'alerts',10)
         self.alert_count=0
         self.threshold_service=self.create_service(Setbool,'set_threshold',self.handle_set_threshold)
         self.get_logger().info("Monitor Node Started....")

     def temperature_callback(self,msg):
         temp=msg.data
         
         if temp>self.temp_threshold:
             self.alert_count+=1
             alert_msg=String()
             alert_msg.data= (
                 f'#Alert  {self.alert_count}: Temperature {temp}'
                 f'exceeds threshold {self.temp_threshold}'
             )
             self.alert_publisher.publish(alert_msg)
             self.get_logger().warn(alert_msg.data)

         else:
             self.get_logger().info(f'Temperature OK : {round(temp,2)}(Threshold Temperature:{self.temp_threshold})')

     def handle_set_threshold(self,request,response):
         if request.data:
             self.temp_threshold+=5
             response.message=f'Threshold increased to {self.temp_threshold}'

         else:
             self.temp_threshold-=5
             response.message=f'Threshold decreased to {self.temp_threshold}'
            
         response.success=True
         self.get_logger().info(response.message)
         return response

         

def main(args=None):
    rclpy.init(args=args)
    node=MonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()
