#!/usr/bin/env python2.7
import rospy
import numpy as np
import tf
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICTIONARY = aruco.Dictionary_get(aruco.DICT_4X4_1000)
ARUCO_SIZE_METER = 0.1

# Create vectors we'll be using for rotations and translations for postures
rvec, tvec = None, None

# distortion coefficients from camera calibration
matrix_coefficients = np.array([np.array([886.491632, 0.000000, 511.684838]),
                                np.array([0.000000, 886.695241, 511.899479]),
                                np.array([0.0,      0.0,        1.0])])
distortion_coefficients = np.array([0.001557, -0.003481, 0.000230, 0.000175, 0.000000])
class Node():

    def __init__(self):
        self.bridge = CvBridge()
        sub_image = rospy.Subscriber("/image", Image, self.image_callback)
        self.pub = rospy.Publisher('imagetimer', Image,queue_size=10)
        cv2.namedWindow("Original Image Window", 1)
        while not rospy.is_shutdown():
            rospy.spin()

    def image_callback(self,img_msg):
        # log some info about the image topic
        rospy.loginfo(img_msg.header)
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
        pic_ori = cv_image

        # lists of ids and the corners beloning to each id
        corners, ids, rejected_img_points = aruco.detectMarkers(pic_ori,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)

        if np.all(ids is not None):  # If there are markers found by detector
            res = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE_METER, (matrix_coefficients), (distortion_coefficients))
            rvec=res[0]
            tvec=res[1]
          #  markerPoints=res[2]
        #     (rvec - tvec).any() # get rid of that nasty numpy value array error
            for i in range(0, ids.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
                print("marker number: ",ids[i][0])
#                print("rvec is: ",rvec[i][0])
                print("tvec is: ",tvec[i][0])
                rotation_matrix = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix[:3, :3], _ = cv2.Rodrigues(rvec[i][0])

                # convert the matrix to a quaternion
                quaternion = tf.transformations.quaternion_from_matrix(rotation_matrix)
                print("rotation is:", quaternion)
                
                aruco.drawAxis(pic_ori, matrix_coefficients, distortion_coefficients, rvec[i], tvec[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori, corners)  # Draw A square around the markers
        #aruco.drawAxis(pic_rsz, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  # Draw Axis
        cv2.imshow("Original Image Window", pic_ori)
        cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    my_node = Node()
#    my_node.start()

