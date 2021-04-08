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
from virtual.msg import CaliInfo
from scipy.spatial.transform import Rotation as R


# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICTIONARY = aruco.Dictionary_get(aruco.DICT_4X4_1000)
ARUCO_SIZE_METER = 0.1

# Create vectors we'll be using for rotations and translations for postures
rvec, tvec = None, None

# distortion coefficients from camera calibration
'''
matrix_coefficients = np.array([np.array([886.491632, 0.000000, 511.684838]),
                                np.array([0.000000, 886.695241, 511.899479]),
                                np.array([0.0,      0.0,        1.0])])
                                '''
matrix_coefficients = np.array([np.array([886.8100134752652, 0.000000, 512.000]),
                                np.array([0.000000,886.8100134752652, 512.000]),
                                np.array([0.0,      0.0,        1.0])])

matrix_coefficients = np.array([np.array([1662.768775266122, 0.000000, 960.000]),
                                np.array([0.000000, 1662.768775266122, 540.000]),
                                np.array([0.0,      0.0,        1.0])])

#distortion_coefficients = np.array([0.001557, -0.003481, 0.000230, 0.000175, 0.000000])
distortion_coefficients = np.array([0.00, 0.000, 0.00, 0.00, 0.000000])

pub_info = np.array([np.array([0.0000]),
                    np.array([0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]),
                    np.array([0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]),
                    np.array([0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]),
                    np.array([0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]),
                    np.array([0.0000,0.0000,0.0000,0.0000,0.0000,0.0000])])

pub = rospy.Publisher('/vrep/calibration_info', CaliInfo ,queue_size=10)
filename = "info.txt"
with open(filename,"w") as file:
    file.write("records:\n")
    file.close()
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
def quaternion_to_euler1(quaternion):
    euler = tf.transformations.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    return roll,pitch,yaw
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
        # rospy.loginfo(img_msg.header)
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
        pic_ori = cv_image
     #   cv2.imshow("Ori", pic_ori)
        # set tf
        t = tf.Transformer(True, rospy.Duration(10.0))
        for i in range(0, len(tf_msg.transforms)):
            m = tf_msg.transforms[i]
            t.setTransform(m)
        
        # lists of ids and the corners beloning to each id
        corners, ids, rejected_img_points = aruco.detectMarkers(pic_ori,ARUCO_DICTIONARY,parameters = ARUCO_PARAMETERS)
        print(ids)
        
        if np.all(ids is not None):  # If there are markers found by detector
            res = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE_METER, (matrix_coefficients), (distortion_coefficients))
            rvec=res[0]
            tvec=res[1]

        #     (rvec - tvec).any() # get rid of that nasty numpy value array error
            for i in range(0, ids.size):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficientss
                rotation_matrix = np.array([[0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 1]],
                                           dtype=float)
                rotation_matrix[:3, :3], _ = cv2.Rodrigues(rvec[i][0])
                rotation_matrix[0][3] = -tvec[i][0][0]
                rotation_matrix[1][3] = -tvec[i][0][1]
                rotation_matrix[2][3] = tvec[i][0][2]
                rotation_matrix[0][0] = -rotation_matrix[0][0]
                rotation_matrix[0][1] = -rotation_matrix[0][1]
                rotation_matrix[0][2] = -rotation_matrix[0][2]
                rotation_matrix[1][0] = -rotation_matrix[1][0]
                rotation_matrix[1][1] = -rotation_matrix[1][1]
                rotation_matrix[1][2] = -rotation_matrix[1][2]
                
                # convert the matrix to a quaternion
                quaternion = tf.transformations.quaternion_from_matrix(rotation_matrix)
                euler1 = quaternion_to_euler1(quaternion)
                '''
                print("-------------------------------------")
                print("marker number: ",ids[i][0])

                # estimate from picture
                print("from picutre:")
                '''
              #  print("trans: ", rotation_matrix[0][3], rotation_matrix[1][3],rotation_matrix[2][3])
                '''
          #      print("quat",quaternion)
          '''
                euler_measure = quaternion_to_euler1(quaternion)
                '''
                print("euler angle: ", euler_measure)
                '''
                # Ground truth
                marker_name = "marker"+str(ids[i][0])
                
                try:
                    (trans, quat) = t.lookupTransform('calibration_camera', marker_name, rospy.Time(0))
                    '''
                    print("groud truth:")
                    
                    print("trans: ", trans)
                    print("quat: ", )
                    '''
                    euler_truth = quaternion_to_euler1(quat)
              #      print("euler angle 2: ", euler_truth)
                except: 
                    print("no marker here! ")
                if(ids[i][0] == 10 and trans):
                    try:
                        #markerid
                        pub_info[0] = ids[i][0]
                        print("-------------------------------------")
                        print("Take marker 10 as example:")
                        print("#01. Ground Truth of marker2cam")
                        print("t: ",(rotation_matrix[0][3], rotation_matrix[1][3],rotation_matrix[2][3]))
                        print("q: ", quaternion)
                        print("#02. Measurements of marker2cam")
                        print("t: ", trans)
                        print("q: ", quat)
                        # marker to camera measurement         ####################################
                        pub_info[1][0] = rotation_matrix[0][3]
                        pub_info[1][1] = rotation_matrix[1][3]
                        pub_info[1][2] = rotation_matrix[2][3]
                        pub_info[1][3] = euler_measure[0]
                        pub_info[1][4] = euler_measure[1]
                        pub_info[1][5] = euler_measure[2]
                        
                        #marker to camera ground truth
                        pub_info[2][0] = trans[0]
                        pub_info[2][1] = trans[1]
                        pub_info[2][2] = trans[2]
                        pub_info[2][3] = euler_truth[0]
                        pub_info[2][4] = euler_truth[1]
                        pub_info[2][5] = euler_truth[2]
                        
                        # link8 to link1 tf  measurement       ################################
                        (temp_trans,temp_quat) = t.lookupTransform('link8', 'link1', rospy.Time(0))
                        temp_euler = quaternion_to_euler1(temp_quat)
                        pub_info[3][0] = temp_trans[0]
                        pub_info[3][1] = temp_trans[1]
                        pub_info[3][2] = temp_trans[2]
                        pub_info[3][3] = temp_euler[0]
                        pub_info[3][4] = temp_euler[1]
                        pub_info[3][5] = temp_euler[2]
                        print("#03. tf of base2ee")
                        print("t: ", temp_trans)
                        print("q: ", temp_quat)
                   #     print(trans)
                        filename = "info.txt"
                        with open(filename,"a") as file:
                            
                            file.write("markerINcam trans: ")
                            file.writelines(["%s " % item  for item in trans])
                            file.write("\n")
                            file.write("markerINcam quat: ")
                            file.writelines(["%s " % item  for item in quat])
                            file.write("\n")

                            file.write("eeINbase trans: ")
                            file.writelines(["%s " % item  for item in temp_trans])
                            file.write("\n")
                            file.write("eeINbase quat: ")
                            file.writelines(["%s " % item  for item in temp_quat])
                            file.write("\n\n")
                            
                            file.close()   
                       
                        # robot base to camera loc ground truth ############hand-eye
                        (temp_trans,temp_quat) = t.lookupTransform('link1','calibration_camera', rospy.Time(0))
                        temp_euler = quaternion_to_euler1(temp_quat)
                        pub_info[4][0] = temp_trans[0]
                        pub_info[4][1] = temp_trans[1]
                        pub_info[4][2] = temp_trans[2]
                        pub_info[4][3] = temp_euler[0]
                        pub_info[4][4] = temp_euler[1]
                        pub_info[4][5] = temp_euler[2]
                        print("#04. ground truth of camera2base")
                        print("t: ", temp_trans)
                        print("q: ", temp_quat)
                 #       print("#######eye-base#######",temp_trans,temp_quat)
                        # marker 10 to link8 ground truth
                        (temp_trans,temp_quat) = t.lookupTransform( 'marker10', 'link8', rospy.Time(0))
                        temp_euler = quaternion_to_euler1(temp_quat)
                        pub_info[5][0] = temp_trans[0]
                        pub_info[5][1] = temp_trans[1]
                        pub_info[5][2] = temp_trans[2]
                        pub_info[5][3] = temp_euler[0]
                        pub_info[5][4] = temp_euler[1]
                        pub_info[5][5] = temp_euler[2]
                  #      print("#######marker-ee#######",temp_trans,temp_quat)
                   #     (temp_trans,temp_quat) = t.lookupTransform('link1', 'link1', rospy.Time(0))
                   #     print("***********", temp_trans)
                    except:
                        print("info error")
  #                  print("information", pub_info)

                    msg = CaliInfo()
                    msg.marker = ids[i][0]
                    
                    msg.markerincamera_measure = pub_info[1]
                    msg.markerincamera_truth  = pub_info[2]
                    msg.eeinbase = pub_info[3]
                    msg.baseincamera = pub_info[4]
                    msg.markerinee = pub_info[5]
                    
                    pub.publish(msg)



                aruco.drawAxis(pic_ori, matrix_coefficients, distortion_coefficients, rvec[i], tvec[i], 0.02)
            aruco.drawDetectedMarkers(pic_ori, corners)  # Draw A square around the markers
        #aruco.drawAxis(pic_rsz, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  # Draw Axis
     #   cv2.imshow("Original Image Window", pic_ori)
        cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node("Get_Pic", anonymous=True)
    my_node = Node()
#    my_node.start()

