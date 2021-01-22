#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
# length of msg.ranges = 720


class getScan(object):
    def __init__(self):
        self.ranges = []
        sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, self.callback)
    def callback(self,msg):
        self.ranges = msg.ranges
 
# rospy.init_node('scan_subscriber_node')
 
# rospy.spin()

 