#!/usr/bin/env python2.7

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

class Node():

    def __init__(self):
        self.bridge = CvBridge()
        sub_image = rospy.Subscriber("/image", Image, self.image_callback)
        self.pub = rospy.Publisher('imagetimer', Image,queue_size=10)

        while not rospy.is_shutdown():
            rospy.spin()

    def image_callback(self,img_msg):
        # log some info about the image topic
        rospy.loginfo(img_msg.header)
        cv2.namedWindow("Original Image Window", cv2.WINDOW_NORMAL)
        
        try:
          cv_image = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
        except CvBridgeError, e:
          rospy.logerr("CvBridge Error: {0}".format(e))

        
        cv2.imshow("Original Image Window", cv_image)
        
        cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    my_node = Node()
#    my_node.start()