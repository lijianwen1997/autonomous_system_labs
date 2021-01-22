#! /usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerRequest # import the service message python classes 
import actionlib
 
from std_srvs.srv import Empty
from my_turtlebot_actions.msg import record_odomFeedback, record_odomResult, record_odomAction, record_odomGoal
 
class CmdVelPub(object):
    def __init__(self):
        self._cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._twist_object = Twist()
        self.linearspeed = 0.2
        self.angularspeed = 0.5
        
    def move_robot(self, direction):
        rospy.loginfo(direction)
        if direction == "Go_Left":
            self._twist_object.linear.x = 0.3
            self._twist_object.angular.z = 0.35
        elif direction == "Go_Right":
            self._twist_object.linear.x = 0.3
            self._twist_object.angular.z = -0.35
        elif direction == "Rotate_Right":
            self._twist_object.linear.x = 0.0
            self._twist_object.angular.z = -0.25
        elif direction == "Rotate_Left":
            self._twist_object.linear.x = 0
            self._twist_object.angular.z = 0.25
        elif direction == "Turn_Right":
            self._twist_object.linear.x = 0.25
            self._twist_object.angular.z = -0.65
        elif direction == "Turn_Left":
            self._twist_object.linear.x = 0.25
            self._twist_object.angular.z = 0.65
        elif direction == "Forward":
            self._twist_object.linear.x = 0.55
            self._twist_object.angular.z = 0
        elif direction == "Back":
            self._twist_object.linear.x = -0.3
            self._twist_object.angular.z = -0.3
        else:
            pass
        
        self._cmd_vel_pub.publish(self._twist_object)

rospy.init_node('controller')
pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
#sub = rospy.Subscriber('odom', Odometry, getOdom)
rospy.wait_for_service('/my_service')
my_service_client = rospy.ServiceProxy('/my_service', Trigger)
# Create an object of type EmptyRequest
my_service_object = TriggerRequest()
# Send through the connection the name of the trajectory to be executed by the robot


# create the connection to the action server
client = actionlib.SimpleActionClient('/rec_odom_as', record_odomAction)
# waits until the action server is up and running
client.wait_for_server()
client.send_goal(Empty())
#client.wait_for_result()

#print (result)
Controller = CmdVelPub()
rate = rospy.Rate(5)

counter = 0
while not rospy.is_shutdown():
    state_result = client.get_state()
    if state_result==1:

        result = my_service_client(my_service_object)
        Controller.move_robot(result.message)
 
        rate.sleep()

    else:
        vel = Twist()
        vel.linear.x = 0
        vel.angular.z = 0

        pub.publish(vel)
        time.sleep(0.1)
        Controller._cmd_vel_pub.publish(vel)
        counter+=1
        if counter>5:
            # reset gazebo
            rospy.wait_for_service('/gazebo/reset_world')
            reset_world = rospy.ServiceProxy('gazebo/reset_world',Empty)
            reset_world()
    