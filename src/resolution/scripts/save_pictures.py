#!/usr/bin/env python2.7
# finished
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import threading
import logging
import time
filename1 = 'Image'
filename2 = '.jpg'
count = 0
hdr = None
class Node():
    def __init__(self):
        self.bridge = CvBridge()
        while not rospy.is_shutdown():
            sub_image = rospy.Subscriber("/image", Image, self.image_callback,queue_size= 5)
            rospy.spin()
            
    def image_callback(self,img_msg):
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        cv2.namedWindow("Original Image Window", cv2.WINDOW_NORMAL)
        
        lock = threading.Lock()
        with lock:
            r = raw_input()
        with lock:
            if r == "save" or r == "s":
                global count
                count = count + 1
                print "succeeded to save new camera pose, pose number: ", count
                filename = filename1 + str(count) + filename2
                cv2.imwrite(filename, cv_image)
                cv2.imshow("Original Image Window", cv_image)
            else:
                cv2.imshow("Original Image Window", cv_image)   
        cv2.waitKey(3)
if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    my_node = Node()
#    my_node.start()
