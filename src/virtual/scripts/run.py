#!/usr/bin/env python2.7
import rospy
import numpy as np
import math
import tf
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge, CvBridgeError
import message_filters
import geometry_msgs.msg
from sensor_msgs.msg import Image
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import PoseStamped

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

def quaternion_to_euler(q):
        x,y,z,w = q
        import math
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.degrees(math.atan2(t3, t4))

        return X, Y, Z
class Node():

    def __init__(self):
        self.bridge = CvBridge()

        image_sub = message_filters.Subscriber("/image", Image)
        tf_sub = message_filters.Subscriber("/tf", TFMessage)
        ts = message_filters.ApproximateTimeSynchronizer([image_sub, tf_sub], 10,0.1, allow_headerless=True)
        ts.registerCallback(self.image_callback)

        while not rospy.is_shutdown():
            rospy.spin()

    def image_callback(self, img_msg, tf_msg):
        # log some info about the image topic
      #  rospy.loginfo(img_msg.header)
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
        pic_ori = cv_image

        
        # tf part
        t = tf.Transformer(True, rospy.Duration(10.0))
        for i in range(0, len(tf_msg.transforms)):
            m = tf_msg.transforms[i]
            t.setTransform(m)
        
        # lists of ids and the corners beloning to each id
        corners, ids, rejected_img_points = aruco.detectMarkers(pic_ori,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)

        if np.all(ids is not None):  # If there are markers found by detector
            res = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE_METER, (matrix_coefficients), (distortion_coefficients))
            rvec=res[0]
            tvec=res[1]
          #  markerPoints=res[2]
        #     (rvec - tvec).any() # get rid of that nasty numpy value array error
            for i in range(0, ids.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficientss
                rotation_matrix = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix[:3, :3], _ = cv2.Rodrigues(rvec[i][0])
                rotation_matrix[0][3] = tvec[i][0][0]
                rotation_matrix[1][3] = tvec[i][0][1]
                rotation_matrix[2][3] = tvec[i][0][2]
                
                # convert the matrix to a quaternion
                quaternion = tf.transformations.quaternion_from_matrix(rotation_matrix)
                euler1 = quaternion_to_euler(quaternion)
                euler2 = (euler1[0],-euler1[1],euler1[2]+180)
                print("-------------------------------------")
                print("marker number: ",ids[i][0])
                # estimate from picture
                print("trans 0: ", rotation_matrix[0][3], rotation_matrix[1][3],rotation_matrix[2][3])
                print("trans 1: ", -rotation_matrix[0][3], rotation_matrix[1][3],rotation_matrix[2][3])
                quaternion = tf.transformations.quaternion_from_euler(euler1[0],-euler1[1],euler1[2]+180, axes='sxyz')
                print("euler angle 0: ", quaternion_to_euler(quaternion))
                print("euler angle 1: ", euler2)
                # Ground truth
                
                marker_name = "marker"+str(ids[i][0])
                print marker_name
                try:
                    (trans, quat) = t.lookupTransform(marker_name, 'calibration_camera', rospy.Time(0))
                    print("trans 2: ", trans)
                    
                except: 
                    print("no marker")
                
                aruco.drawAxis(pic_ori, matrix_coefficients, distortion_coefficients, rvec[i], tvec[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori, corners)  # Draw A square around the markers
        #aruco.drawAxis(pic_rsz, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  # Draw Axis
        pub1 = rospy.Publisher('/camera_frame', PoseStamped,queue_size = 5)
        pub2 = rospy.Publisher('/marker23_frame', PoseStamped,queue_size = 5)
        pub3 = rospy.Publisher('/base_frame', PoseStamped,queue_size = 5)
        pub4 = rospy.Publisher('/link6_frame', PoseStamped,queue_size = 5)

        pub1.publish(camera_frame)
        pub2.publish(marker23_frame)
        pub3.publish(base_frame)
        pub4.publish(link6_frame)
    #    cv2.imshow("Original Image Window", pic_ori)
        cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    

    my_node = Node()
#    my_node.start()

