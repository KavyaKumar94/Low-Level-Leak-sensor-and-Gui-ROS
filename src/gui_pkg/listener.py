#!/usr/bin/env python

import rospy
from std_msgs.msg import String

#define the display text
def callback(data):
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

#define the subscriber
def listener():
	# In ROS, nodes are uniquely named. If two nodes with the same
	# node are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'listener' node so that multiple listeners can
	# run simultaneously.
	rospy.init_node('Leak_status_listener', anonymous=True)
	rospy.Subscriber('Battery_Leak_sensor', String, callback)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
	listener()
