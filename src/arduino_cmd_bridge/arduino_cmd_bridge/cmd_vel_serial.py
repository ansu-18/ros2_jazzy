import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial


class CmdVelSerial(Node):
    def __init__(self):
        super().__init__('cmd_vel_serial')
        self.declare_parameter('port', '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
        self.declare_parameter('baud', 115200)

        port = self.get_parameter('port').value
        baud = self.get_parameter('baud').value

        self.ser = serial.Serial(port, baud, timeout=0.1)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        self.get_logger().info(f'Sending /cmd_vel to Arduino on {port} at {baud}')

    def cmd_callback(self, msg):
        line = f'{msg.linear.x:.3f},{msg.linear.y:.3f},{msg.angular.z:.3f}\n'
        self.ser.write(line.encode())


def main():
    rclpy.init()
    node = CmdVelSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()