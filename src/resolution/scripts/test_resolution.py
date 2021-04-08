#!/usr/bin/env python2.7
import rospy
import thread
import numpy as np
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
import math
from scipy.spatial.transform import Rotation as R
import tf
import message_filters
import geometry_msgs.msg
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge, CvBridgeError
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import Image
import matplotlib.pyplot as plt
count = 0
# 1080p: 1920*1080
matrix_coefficients1080 = np.array([np.array([1662.768775266122, 0.000000, 960.000]),
                                np.array([0.000000, 1662.768775266122, 540.000]),
                                np.array([0.0,      0.0,        1.0])])
# 720p: 1080*720
matrix_coefficients720 = np.array([np.array([935.3074360871934, 0.000000, 540.000]),
                                np.array([0.000000, 935.3074360871934, 360.000]),
                                np.array([0.0,      0.0,        1.0])])
# 720p: 1080*720 this is the parameter from camera calibration by 100 pictures
matrix_coefficients720a = np.array([np.array([934.02430997,   0.0,   539.62017522]),
                                np.array([0.000000, 933.91838666, 359.43540621]),
                                np.array([0.0,      0.0,        1.0])])

# 480p: 640*480
matrix_coefficients480 = np.array([np.array([554.2563326236818, 0.000000, 320.000]),
                                np.array([0.000000, 554.2563326236818, 240.000]),
                                np.array([0.0,      0.0,        1.0])])
# 360p: 480*360
matrix_coefficients360 = np.array([np.array([415.6921938165304, 0.000000, 240.000]),
                                np.array([0.000000, 415.6921938165304, 180.000]),
                                np.array([0.0,      0.0,        1.0])])

distortion_coefficients = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
distortion_coefficientsa = np.array([[ 0.00289286, -0.03636814, -0.00004366, -0.00004104,  0.07443653]])
# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICTIONARY = aruco.Dictionary_get(aruco.DICT_4X4_1000)
ARUCO_SIZE_METER = 0.1
# Create vectors we'll be using for rotations and translations for postures
rvec, tvec = None, None
f = open("test_resolution.txt", "w")
f.write("Test 1080p and 720p\n")
f.close()

class Node():
    def square_error(self, vec1,vec2):
        sum = 0.0
        for i in range(0, len(vec1)):
            sum += (vec1[i]*1000-vec2[i]*1000)*(vec1[i]*1000-vec2[i]*1000)
        return sum

    def __init__(self):
        self.bridge = CvBridge()
        sub_image = message_filters.Subscriber("/image", Image)
        sub_image1080 = message_filters.Subscriber("/image1080", Image)
        sub_image480 = message_filters.Subscriber("/image480", Image)
        sub_image360 = message_filters.Subscriber("/image360", Image)
        sub_tf = message_filters.Subscriber("/tf", TFMessage)
        ts = message_filters.ApproximateTimeSynchronizer([sub_image, sub_tf, sub_image1080,sub_image360,sub_image480], 10,0.1, allow_headerless=True)
        ts.registerCallback(self.callback)
        while not rospy.is_shutdown():
            rospy.spin()
    
    def callback(self,img_msg, tf_msg, img_msg1080,img_msg360,img_msg480):
        # log header of img_msg
     #   rospy.loginfo(img_msg.header)
        pic_ori = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
        pic_ori720a = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
        pic_ori360 = self.bridge.imgmsg_to_cv2(img_msg360, "passthrough")
        pic_ori480 = self.bridge.imgmsg_to_cv2(img_msg480, "passthrough")
        pic_ori1080 = self.bridge.imgmsg_to_cv2(img_msg1080, "passthrough")
      
      # get tf
        t = tf.Transformer(True, rospy.Duration(10.0))
        for i in range(0, len(tf_msg.transforms)):
            m = tf_msg.transforms[i]
            t.setTransform(m)
      # deal with tf
   #     print("ground truth")
        
        corners, ids, rejected_img_points = aruco.detectMarkers(pic_ori,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)

        truth_dic = {}
        for i in range(0, ids.size):
          #  print("-----------------")
            marker_id = ids[i][0]            
            marker_name = "marker"+str(marker_id)
          #  print(marker_name)
            try:
                (trans, quat) = t.lookupTransform('calibration_camera', marker_name, rospy.Time(0))
                t1=np.asarray(trans)
                q1=np.asarray(quat)
                truth_dic[marker_id] = (t1,q1)

            except: 
                print("no marker here!")
        
        # deal with marker in 720p
        corners, ids, rejected_img_points = aruco.detectMarkers(pic_ori,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)
        if np.all(ids is not None):  # If there are markers found by detector
            res = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE_METER, (matrix_coefficients720), (distortion_coefficients))
            rvec=res[0]
            tvec=res[1]
            (rvec - tvec).any() # get rid of that nasty numpy value array error
            measurement_dic = {}
            for i in range(0, ids.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
   #             print("marker number: ",ids[i][0])
#                print("rvec is: ",rvec[i][0])
                
                rotation_matrix = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix[:3, :3], _ = cv2.Rodrigues(rvec[i][0])
                tvec[i][0][0] = -tvec[i][0][0]
                tvec[i][0][1] = -tvec[i][0][1]
                
                rotation_matrix[0][3] = -tvec[i][0][0]
                rotation_matrix[1][3] = -tvec[i][0][1]
                rotation_matrix[2][3] = tvec[i][0][2]
                rotation_matrix[0][0] = -rotation_matrix[0][0]
                rotation_matrix[0][1] = -rotation_matrix[0][1]
                rotation_matrix[0][2] = -rotation_matrix[0][2]
                rotation_matrix[1][0] = -rotation_matrix[1][0]
                rotation_matrix[1][1] = -rotation_matrix[1][1]
                rotation_matrix[1][2] = -rotation_matrix[1][2]
                
    #            print("tvec is: ",tvec[i][0])
                # convert the matrix to a quaternion
                quaternion = tf.transformations.quaternion_from_matrix(rotation_matrix)
    #            print("rotation is:", quaternion)
                marker_id = ids[i][0]
                t=np.asarray(tvec[i][0])
                q=np.asarray(quaternion)
                measurement_dic[marker_id] = (t,q)
                aruco.drawAxis(pic_ori, matrix_coefficients720, distortion_coefficients, rvec[i], tvec[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori, corners)  # Draw A square around the markers
        # TODO 
        # deal with marker in 720p from 15 pictures
        corners1, ids1, rejected_img_points1 = aruco.detectMarkers(pic_ori720a,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)
        if np.all(ids1 is not None):  # If there are markers found by detector
            res1 = aruco.estimatePoseSingleMarkers(corners1, ARUCO_SIZE_METER, (matrix_coefficients720a), (distortion_coefficientsa))
            rvec1=res1[0]
            tvec1=res1[1]
            (rvec1 - tvec1).any() # get rid of that nasty numpy value array error
            measurement_dic1 = {}
            for i in range(0, ids1.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
   #             print("marker number: ",ids[i][0])
#                print("rvec is: ",rvec[i][0])
                
                rotation_matrix1 = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix1[:3, :3], _ = cv2.Rodrigues(rvec1[i][0])
                tvec1[i][0][0] = -tvec1[i][0][0]
                tvec1[i][0][1] = -tvec1[i][0][1]
                
                rotation_matrix1[0][3] = -tvec1[i][0][0]
                rotation_matrix1[1][3] = -tvec1[i][0][1]
                rotation_matrix1[2][3] = tvec1[i][0][2]
                rotation_matrix1[0][0] = -rotation_matrix1[0][0]
                rotation_matrix1[0][1] = -rotation_matrix1[0][1]
                rotation_matrix1[0][2] = -rotation_matrix1[0][2]
                rotation_matrix1[1][0] = -rotation_matrix1[1][0]
                rotation_matrix1[1][1] = -rotation_matrix1[1][1]
                rotation_matrix1[1][2] = -rotation_matrix1[1][2]
                
    #            print("tvec is: ",tvec[i][0])
                # convert the matrix to a quaternion
                quaternion1 = tf.transformations.quaternion_from_matrix(rotation_matrix1)
    #            print("rotation is:", quaternion)
                marker_id = ids1[i][0]
                t1=np.asarray(tvec1[i][0])
                q1=np.asarray(quaternion1)
                measurement_dic1[marker_id] = (t1,q1)
                aruco.drawAxis(pic_ori720a, matrix_coefficients720a, distortion_coefficientsa, rvec[i], tvec[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori720a, corners1)  # Draw A square around the markers

        # deal with marker in 1080p
        corners1080, ids1080, rejected_img_points1080 = aruco.detectMarkers(pic_ori1080,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)
        if np.all(ids is not None):  # If there are markers found by detector
            res1080 = aruco.estimatePoseSingleMarkers(corners1080, ARUCO_SIZE_METER, (matrix_coefficients1080), (distortion_coefficients))
            rvec1080=res1080[0]
            tvec1080=res1080[1]
            (rvec1080 - tvec1080).any() # get rid of that nasty numpy value array error
            measurement_dic1080 = {}
            for i in range(0, ids1080.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
   #             print("marker number: ",ids[i][0])
#                print("rvec is: ",rvec[i][0])
                
                rotation_matrix1080 = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix1080[:3, :3], _ = cv2.Rodrigues(rvec1080[i][0])
                tvec1080[i][0][0] = -tvec1080[i][0][0]
                tvec1080[i][0][1] = -tvec1080[i][0][1]
                
                rotation_matrix1080[0][3] = -tvec1080[i][0][0]
                rotation_matrix1080[1][3] = -tvec1080[i][0][1]
                rotation_matrix1080[2][3] = tvec1080[i][0][2]
                rotation_matrix1080[0][0] = -rotation_matrix1080[0][0]
                rotation_matrix1080[0][1] = -rotation_matrix1080[0][1]
                rotation_matrix1080[0][2] = -rotation_matrix1080[0][2]
                rotation_matrix1080[1][0] = -rotation_matrix1080[1][0]
                rotation_matrix1080[1][1] = -rotation_matrix1080[1][1]
                rotation_matrix1080[1][2] = -rotation_matrix1080[1][2]
                
    #            print("tvec is: ",tvec[i][0])
                # convert the matrix to a quaternion
                quaternion1080 = tf.transformations.quaternion_from_matrix(rotation_matrix1080)
    #            print("rotation is:", quaternion)
                marker_id1080 = ids1080[i][0]
                t1080=np.asarray(tvec1080[i][0])
                q1080=np.asarray(quaternion1080)
                measurement_dic1080[marker_id1080] = (t1080,q1080)
                aruco.drawAxis(pic_ori1080, matrix_coefficients1080, distortion_coefficients, rvec1080[i], tvec1080[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori1080, corners1080)  # Draw A square around the markers
           # print measurement_dic

        # deal with marker in 480p
        corners480, ids480, rejected_img_points480 = aruco.detectMarkers(pic_ori480,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)
        if np.all(ids is not None):  # If there are markers found by detector
            res480 = aruco.estimatePoseSingleMarkers(corners480, ARUCO_SIZE_METER, (matrix_coefficients480), (distortion_coefficients))
            rvec480=res480[0]
            tvec480=res480[1]
            (rvec480 - tvec480).any() # get rid of that nasty numpy value array error
            measurement_dic480 = {}
            for i in range(0, ids480.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
   #             print("marker number: ",ids[i][0])
#                print("rvec is: ",rvec[i][0])
                
                rotation_matrix480 = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix480[:3, :3], _ = cv2.Rodrigues(rvec480[i][0])
                tvec480[i][0][0] = -tvec480[i][0][0]
                tvec480[i][0][1] = -tvec480[i][0][1]
                
                rotation_matrix480[0][3] = -tvec480[i][0][0]
                rotation_matrix480[1][3] = -tvec480[i][0][1]
                rotation_matrix480[2][3] = tvec480[i][0][2]
                rotation_matrix480[0][0] = -rotation_matrix480[0][0]
                rotation_matrix480[0][1] = -rotation_matrix480[0][1]
                rotation_matrix480[0][2] = -rotation_matrix480[0][2]
                rotation_matrix480[1][0] = -rotation_matrix480[1][0]
                rotation_matrix480[1][1] = -rotation_matrix480[1][1]
                rotation_matrix480[1][2] = -rotation_matrix480[1][2]
                
    #            print("tvec is: ",tvec[i][0])
                # convert the matrix to a quaternion
                quaternion480 = tf.transformations.quaternion_from_matrix(rotation_matrix480)
    #            print("rotation is:", quaternion)
                marker_id480 = ids480[i][0]
                t480=np.asarray(tvec480[i][0])
                q480=np.asarray(quaternion480)
                measurement_dic480[marker_id480] = (t480,q480)
                aruco.drawAxis(pic_ori480, matrix_coefficients480, distortion_coefficients, rvec480[i], tvec480[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori480, corners480)  # Draw A square around the markers
           # print measurement_dic

        # deal with marker in 360p
        corners360, ids360, rejected_img_points360 = aruco.detectMarkers(pic_ori360,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)
        if np.all(ids is not None):  # If there are markers found by detector
            res360 = aruco.estimatePoseSingleMarkers(corners360, ARUCO_SIZE_METER, (matrix_coefficients360), (distortion_coefficients))
            rvec360 =res360[0]
            tvec360 =res360[1]
            (rvec360 - tvec360).any() # get rid of that nasty numpy value array error
            measurement_dic360 = {}
            for i in range(0, ids360.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
   #             print("marker number: ",ids[i][0])
#                print("rvec is: ",rvec[i][0])
                
                rotation_matrix360 = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix360[:3, :3], _ = cv2.Rodrigues(rvec360[i][0])
                tvec360[i][0][0] = -tvec360[i][0][0]
                tvec360[i][0][1] = -tvec360[i][0][1]
                
                rotation_matrix360[0][3] = -tvec360[i][0][0]
                rotation_matrix360[1][3] = -tvec360[i][0][1]
                rotation_matrix360[2][3] = tvec360[i][0][2]
                rotation_matrix360[0][0] = -rotation_matrix360[0][0]
                rotation_matrix360[0][1] = -rotation_matrix360[0][1]
                rotation_matrix360[0][2] = -rotation_matrix360[0][2]
                rotation_matrix360[1][0] = -rotation_matrix360[1][0]
                rotation_matrix360[1][1] = -rotation_matrix360[1][1]
                rotation_matrix360[1][2] = -rotation_matrix360[1][2]
                
    #            print("tvec is: ",tvec[i][0])
                # convert the matrix to a quaternion
                quaternion360 = tf.transformations.quaternion_from_matrix(rotation_matrix360)
    #            print("rotation is:", quaternion)
                marker_id360 = ids360[i][0]
                t360 = np.asarray(tvec360[i][0])
                q360 = np.asarray(quaternion360)
                measurement_dic360[marker_id360] = (t360,q360)
                aruco.drawAxis(pic_ori360, matrix_coefficients360, distortion_coefficients, rvec360[i], tvec360[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori360, corners360)  # Draw A square around the markers
           # print measurement_dic
  #      
      # thread
        try:
            thread.start_new_thread(self.Record_thread, (truth_dic, measurement_dic, measurement_dic1080,measurement_dic360,measurement_dic480,measurement_dic1))
        except:
            print("Error: unable to start thread")
        cv2.waitKey(200)
    
    def Record_thread(self,tf_msg,img_msg720,img_msg1080,img_msg360,img_msg480,img_msg720a):
      # get keyboard input
        cmd_to_record = raw_input()
      # TODO: exit
        if(cmd_to_record =='exit'):
            print("exit")
      # print result and calculate error
        elif(cmd_to_record =='print'):
            global count
            count = count + 1
            
            f = open("test_resolution.txt", "a")
    #        print("-----------------------")
    #        print "result", count
            f.write("-----------------------\n")
         #   f.write("result %s\n" % count ) 
            f.write("result \n" ) 
            img_10_loc480 = img_msg480[10][0]
            img_10_quat480 = img_msg480[10][1]
            img_10_loc720 = img_msg720[10][0]
            img_10_quat720 = img_msg720[10][1]
            img_10_loc720a = img_msg720a[10][0]
            img_10_quat720a = img_msg720a[10][1]
            img_10_loc1080 = img_msg1080[10][0]
            img_10_quat1080 = img_msg1080[10][1]
            img_10_loc360 = img_msg360[10][0]
            img_10_quat360 = img_msg360[10][1]
            tf_10_loc = tf_msg[10][0]
            tf_10_quat = tf_msg[10][1]
            
            # tf
            print("----------tf----------")
            print "location from tf:",tf_10_loc
            euler1 = np.asarray(tf.transformations.euler_from_quaternion(tf_10_quat))*(180.0/3.1415926)
            print "rotation from tf:",euler1
            
            f.write("----------tf----------\n")
            f.write("location from tf: ")
            f.writelines(["%s " % item  for item in tf_10_loc] ) 
            f.write("\n")
            f.write("rotation from tf: ")
            f.writelines(["%s " % item  for item in euler1] )
            f.write("\n")

            # result of 360p
            
            print "----------360p----------"
            print "location by image: ",img_10_loc360
            euler4 = np.asarray(tf.transformations.euler_from_quaternion(img_10_quat360))*(180.0/3.1415926)
            print "rotation by image: ",euler4

            f.write("---------360p---------\n")
            f.write("location by image from 360p: ")
            f.writelines(["%s " % item  for item in img_10_loc360] ) 
            f.write("\n")
            f.write("rotation by image from 360p: ")
            f.writelines(["%s " % item  for item in euler4] )
            f.write("\n")
            
            # result of 480p
            print "----------480p----------"
            print "location by image: ",img_10_loc480
            euler5 = np.asarray(tf.transformations.euler_from_quaternion(img_10_quat480))*(180.0/3.1415926)
            print "rotation by image: ",euler5
            
            f.write("---------480p---------\n")
            f.write("location by image from 480p: ")
            f.writelines(["%s " % item  for item in img_10_loc480] ) 
            f.write("\n")
            f.write("rotation by image from 480p: ")
            f.writelines(["%s " % item  for item in euler5] )
            f.write("\n")
            
            # result of 720p
            print("----------720p theoretical parameters----------")
            print "location by image: ",img_10_loc720
            euler2 = np.asarray(tf.transformations.euler_from_quaternion(img_10_quat720))*(180.0/3.1415926)
            print "rotation by image: ",euler2

            '''
           
            # result of 720p with calibrated parameters
            print("----------720p calibrated parameters----------")
            print "location by image: ",img_10_loc720a
            euler6 = np.asarray(tf.transformations.euler_from_quaternion(img_10_quat720a))*(180.0/3.1415926)
            print "rotation by image: ",euler6
            '''

            f.write("---------720p---------\n")
            f.write("location by image from 720p: ")
            f.writelines(["%s " % item  for item in img_10_loc720] ) 
            f.write("\n")
            f.write("rotation by image from 720p: ")
            f.writelines(["%s " % item  for item in euler2] )
            f.write("\n")

            # result of 1080p
            print "----------1080p----------"
            print "location by image: ",img_10_loc1080
            euler3 = np.asarray(tf.transformations.euler_from_quaternion(img_10_quat1080))*(180.0/3.1415926)
            print "rotation by image: ",euler3
            
            f.write("---------1080p---------\n")
            f.write("location by image from 1080p: ")
            f.writelines(["%s " % item  for item in img_10_loc1080] ) 
            f.write("\n")
            f.write("rotation by image from 1080p: ")
            f.writelines(["%s " % item  for item in euler3] )
            f.write("\n")
            # compare
            print("----------compare----------")
            '''
            print "difference of translation 360p: ", img_10_loc360 - tf_10_loc
            print "RSE of translation 360p: ", self.square_error(img_10_loc360, tf_10_loc)
            print "difference of rotation 360p: ", euler1-euler4, "\n"
         #   print "RSE of rotation 360p: ", self.square_error(euler1, euler4)
            '''
            print "difference of translation 480p: ", img_10_loc480 - tf_10_loc
            print "RSE of translation 480p: ", self.square_error(img_10_loc480, tf_10_loc)
            print "difference of rotation 480p: ", euler1-euler5, "\n"
         #   print "RSE of rotation 480pp: ", self.square_error(euler1, euler5)
            print "difference of translation 720p: ", img_10_loc720 - tf_10_loc
            print "RSE of translation 720p: ", self.square_error(img_10_loc720, tf_10_loc)
            print "difference of rotation 720p: ", euler1-euler2, "\n"
         #   print "RSE of rotation 720p: ", self.square_error(euler1, euler2)
            '''

            print "difference of translation 720p with calibrated parameters: ", img_10_loc720a - tf_10_loc
            print "RSE of translation 720p with calibrated parameters: ", self.square_error(img_10_loc720a, tf_10_loc)
            print "difference of rotation 720p with calibrated parameters: ", euler1-euler6, "\n"
            '''

            print "difference of translation 1080p: ", img_10_loc1080 - tf_10_loc
            print "RSE of translation 1080p: ", self.square_error(img_10_loc1080, tf_10_loc)
            print "difference of rotation 1080p: ", euler1-euler3, "\n"
         #   print "RSE of rotation 1080p: ", self.square_error(euler1, euler3)
            
            f.write("--------compare--------\n")
            f.write("difference of translation 720p: %s" % np.linalg.norm(img_10_loc720-tf_10_loc))

            f.write("\n")
            f.write("difference of rotation 720p: " )
            f.writelines(["%s " % item  for item in euler1-euler2] )
            f.write("\n")
            f.write("difference of translation 1080p: %s" % np.linalg.norm(img_10_loc1080-tf_10_loc))

            f.write("\n")
            f.write("difference of rotation 1080p: ")
            f.writelines(["%s " % item  for item in euler1-euler3] )
            f.write("\n\n")
        else:
            print("Wrong Cmd")
if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    my_node = Node()
  #  my_node.start()
  