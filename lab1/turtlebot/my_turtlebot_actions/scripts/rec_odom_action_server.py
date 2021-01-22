#! /usr/bin/env python
import rospy
import time
import actionlib

from my_turtlebot_actions.msg import record_odomFeedback, record_odomResult, record_odomAction
from std_srvs.srv import Empty
from odom_sub import getOdom
from geometry_msgs.msg import Twist


class Odom_server(object):
    
  # create messages that are used to publish feedback/result
  _feedback = record_odomFeedback()
  _result   = record_odomResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("/rec_odom_as", record_odomAction, self.goal_callback, False)
    self._as.start()
    self.rate = rospy.Rate(10)
    self.tic = time.time()
    self.tok = time.time()
    
    
  
    
  def goal_callback(self, goal):
    # this callback is called when the action server is called.
    # this is the function that computes the Fibonacci sequence
    # and returns the sequence to the node that called the action server

    # helper variables
    r = rospy.Rate(1)
 
    self.tic = time.time()
    self.tok = time.time()
    while self.tok - self.tic < 42:
        self.tok = time.time()
        #print(self.tok - self.tic)
        #print(OdomClass.data)
        self._result.result_odom_array.append(OdomClass.data)
        if OdomClass.data.pose.pose.position.y<-8.5:
            rospy.loginfo("Congradulation! exit maze!")
            break
        time.sleep(0.1)

    time.sleep(1)
    print('Mission time : %f' % (self.tok - self.tic))
    self._as.set_succeeded(self._result)


    

 


if __name__ == '__main__':
  rospy.init_node('record_odom_action_server_node')
  OdomClass = getOdom()
  Odom_server()
  rospy.spin()
 