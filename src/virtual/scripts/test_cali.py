#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped

marker23_frame = PoseStamped()
marker23_frame.header.frame_id = 'calibration_camera'
marker23_frame.pose.orientation.w = 1.0

camera_frame = PoseStamped()
camera_frame.header.frame_id = 'link1'
camera_frame.pose.orientation.w = 1.0

base_frame = PoseStamped()
base_frame.header.frame_id = 'link1'
base_frame.pose.orientation.w = 1.0

link6_frame = PoseStamped()
link6_frame.header.frame_id = 'camera_frame'
link6_frame.pose.orientation.w = 1.0

if __name__ == '__main__':
    rospy.init_node('vrep_tf_listener')

    listener = tf.TransformListener()

    turtle_vel = rospy.Publisher('turtle2/cmd_vel', PoseStamped,queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans1,rot1) = listener.lookupTransform('calibration_camera','marker23', rospy.Time(0))
            marker23_frame.pose.position.x = trans1[0]
            marker23_frame.pose.position.y = trans1[1]
            marker23_frame.pose.position.z = trans1[2]

            marker23_frame.pose.orientation.x = rot1[0]
            marker23_frame.pose.orientation.y = rot1[1]
            marker23_frame.pose.orientation.z = rot1[2]
            marker23_frame.pose.orientation.w = rot1[3]

       
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        

        turtle_vel.publish(marker23_frame)

        rate.sleep()