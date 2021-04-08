#!/usr/bin/env python2.7
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import thread
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
        sub_image = rospy.Subscriber("/image", Image, self.image_callback)
        
        while not rospy.is_shutdown():
            rospy.spin()
            
    def image_callback(self,img_msg):
        # log some info about the image topic
   #     rospy.loginfo(img_msg.header)
        cv_image = None
   #     cv2.namedWindow("Original Image Window", cv2.WINDOW_NORMAL)
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        
        # start the thread of recording 
        try:
            thread.start_new_thread(self.Record_thread, (cv_image,img_msg.header))
        except:
            print("Error: unable to start thread")
  #      cv2.imshow("Original Image Window", cv_image)    
        cv2.waitKey(10)
        
    def Record_thread(self,img,header):
        # get keyboard input
    #    rospy.loginfo(header)   
        cmd_to_record = raw_input()        
        if(cmd_to_record =='exit'):
            print("exit")
        # print result and calculate error
        elif(cmd_to_record =='save'):
            global count
            count = count + 1
            print "succeeded to save new camera pose, pose number: ", count
            # Using cv2.imwrite() method saving the image
            filename = filename1 + str(count) + filename2
            cv2.imwrite(filename, img)
        
if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    my_node = Node()
#    my_node.start()