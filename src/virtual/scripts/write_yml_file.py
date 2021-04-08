#!/usr/bin/env python2.7
import rospy
import numpy as np
import math as m
import tf
import cv2
import cv2.aruco as aruco
import geometry_msgs.msg
from virtual.msg import CaliInfo
from scipy.spatial.transform import Rotation as R
import yaml
import collections as c
from numpy.linalg import inv
yml_filename = "TransformPairsInput.yml"
with open(yml_filename,"w") as file:
    documents = yaml.dump("frameCount: ", file)

count = 0

class Node():

    def __init__(self):
        sub_info = rospy.Subscriber("/vrep/calibration_info", CaliInfo, self.info_callback)
        while not rospy.is_shutdown():
            rospy.spin()

    def calculate_matrix(self,info):
        rotation_matrix = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 1]],
                                    dtype=float)
  #      print(rotation_matrix)         
        rotation_matrix[0][3] = info[0]
        rotation_matrix[1][3] = info[1]
        rotation_matrix[2][3] = info[2]
        a = info[3]
        b = info[4]
        c = info[5]
        r = R.from_euler('xyz', [a,b,c], degrees=False)
        rotation_matrix[:3,:3] = r.as_dcm()
    
        return rotation_matrix     
        
    def info_callback(self,cali_msg):
        # log some info about the image topic
        rospy.loginfo(cali_msg.marker)
        eeinbase_transform = self.calculate_matrix(cali_msg.eeinbase)
        markerincamera_transform = self.calculate_matrix(cali_msg.markerincamera_measure)
        baseincamera_transform = self.calculate_matrix(cali_msg.baseincamera)
        markerinee_transform = self.calculate_matrix(cali_msg.baseincamera)
        t1 = eeinbase_transform 
        t2 = markerincamera_transform 

        print("----------------------------------")
      #  print(t1*t4*inv(t2)*t3)
        print ("t1   ",t1[0][0],t1[0][1],t1[0][2],t1[0][3],
                        t1[1][0],t1[1][1],t1[1][2],t1[1][3],
                        t1[2][0],t1[2][1],t1[2][2],t1[2][3],
                        t1[3][0],t1[3][1],t1[3][2],t1[3][3])
        print ("t2   ",t2[0][0],t2[0][1],t2[0][2],t2[0][3],
                        t2[1][0],t2[1][1],t2[1][2],t2[1][3],
                        t2[2][0],t2[2][1],t2[2][2],t2[2][3],
                        t2[3][0],t2[3][1],t2[3][2],t2[3][3])
   #     print np.matmul(t1,t4)
    #    print np.matmul(t4,t1)
   #     print np.matmul(np.matmul(np.matmul(t1,t4),inv(t5)),t3)
        print("----------------------------------")

        cv2.waitKey(3)




if __name__ == '__main__':
    rospy.init_node("Get_Info", anonymous=True)
    my_node = Node()
#    my_node.start()
