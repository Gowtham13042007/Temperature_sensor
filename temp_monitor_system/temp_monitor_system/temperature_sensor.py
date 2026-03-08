import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float32

class TemperatureSensor(Node):
    def __init__(self):
        super().__init__("Temperature_Sensor")
        self.declare_parameter("publish_rate",2.0)
        self.declare_parameter("base_temp",25.0)
        self.declare_parameter("temp_variation",5.0)

        rate=self.get_parameter("publish_rate").value
        self.base_temp=self.get_parameter("base_temp").value
        self.temp_variation=self.get_parameter("temp_variation").value

        self.publisher_=self.create_publisher(Float32,'temperature',20)
        timer_period=1.0/rate
        self.timer_=self.create_timer(timer_period,self.publish_temperature)
        self.get_logger().info("Temperature Sensor Started")

    def publish_temperature(self):
        temp=self.base_temp+random.uniform(-self.temp_variation,self.temp_variation)
        msg=Float32()
        msg.data=round(temp,2)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing:{msg.data} °C')


def main(args=None):
    rclpy.init(args=args)
    node=TemperatureSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()
