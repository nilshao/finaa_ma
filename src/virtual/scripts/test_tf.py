#!/usr/bin/env python2.7
import rospy
import numpy as np
import tf
import roslib
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_listener')

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/camera', '/marker', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        print("transformation: ", trans)
        print("rotation: ", rot)

        rate.sleep()

