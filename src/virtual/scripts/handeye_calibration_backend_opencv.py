#!/usr/bin/env python3
import cv2
import numpy as np
import transforms3d as tfs
#from rospy import logerr, logwarn, loginfo
from scipy.spatial.transform import Rotation as R
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
filename = "cali.txt"
# from easy_handeye.handeye_calibration import HandeyeCalibration

##Minimum samples required for a successful calibration."""
MIN_SAMPLES = 2  

AVAILABLE_ALGORITHMS = {
        'Tsai-Lenz': cv2.CALIB_HAND_EYE_TSAI,
        'Park': cv2.CALIB_HAND_EYE_PARK,
        'Horaud': cv2.CALIB_HAND_EYE_HORAUD,
        'Andreff': cv2.CALIB_HAND_EYE_ANDREFF,
        'Daniilidis': cv2.CALIB_HAND_EYE_DANIILIDIS,
    }

def _msg_to_opencv(transform_msg):
    cmt = transform_msg.translation
    tr = np.array((cmt.x, cmt.y, cmt.z))
    cmq = transform_msg.rotation
    rot = tfs.quaternions.quat2mat((cmq.w, cmq.x, cmq.y, cmq.z))
    return rot, tr

def to_matrix(quat,trans):
    rotation_matrix = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 1]],
                                    dtype=float)
    r = R.from_quat(quat)
    # rotation_matrix[:3,:3] = r.as_dcm()
    return r.as_dcm(), trans

def _get_opencv_samples(samples):
    """
    Returns the sample list as a rotation matrix and a translation vector.
    :rtype: (np.array, np.array)
    """
    hand_base_rot = []
    hand_base_tr = []
    marker_camera_rot = []
    marker_camera_tr = []

    for s in samples:
        ##TODO
        mcquat = s["markerINcam quat"]
        mctrans = s["markerINcam trans"]
        (mcr, mct) = to_matrix(mcquat,mctrans)
        marker_camera_rot.append(mcr)
        marker_camera_tr.append(mct)

        hbquat = s["eeINbase quat"]
        hbtrans =  s["eeINbase trans"]
        (hbr, hbt) = to_matrix(hbquat,hbtrans)
        hand_base_rot.append(hbr)
        hand_base_tr.append(hbt)


        '''
        ########### ???
        mcquat = s["markerINcam quat"]
        mctrans = s["markerINcam trans"]
        (hbr, hbt) = to_matrix(mcquat,mctrans)
        hbquat = s["eeINbase quat"]
        hbtrans =  s["eeINbase trans"]
        (mcr, mct) = to_matrix(hbquat,hbtrans)
        marker_camera_rot.append(mcr)
        marker_camera_tr.append(mct)
        hand_base_rot.append(hbr)
        hand_base_tr.append(hbt)
        '''
    return (hand_base_rot, hand_base_tr), (marker_camera_rot, marker_camera_tr)

#def compute_calibration(handeye_parameters, samples, algorithm=None):
def compute_calibration(samples, algorithm=None):

    if algorithm is None:
        algorithm = 'Tsai-Lenz'

    # Update data
    opencv_samples = _get_opencv_samples(samples)
    (b_rot, b_tr), (a_rot, a_tr) = opencv_samples

    method = AVAILABLE_ALGORITHMS[algorithm]
    x_rot, x_tr = cv2.calibrateHandEye(a_rot, a_tr, b_rot, b_tr, method=method)
    result = tfs.affines.compose(np.squeeze(x_tr), x_rot, [1, 1, 1])
 #   print("Computed calibration: {}".format(str(result)))
   
    (hcqw, hcqx, hcqy, hcqz) = [float(i) for i in tfs.quaternions.mat2quat(x_rot)]
    (hctx, hcty, hctz) = [float(i) for i in x_tr]
    result_tuple = ((hctx, hcty, hctz), (hcqx, hcqy, hcqz, hcqw))
    return result_tuple

# calculate marker2gripper
def compute_calibration2(samples, algorithm=None):
    """
    Computes the calibration through the OpenCV library and returns it.
    :rtype: easy_handeye.handeye_calibration.HandeyeCalibration
    """
    if algorithm is None:
        algorithm = 'Tsai-Lenz'

    # Update data
    opencv_samples = _get_opencv_samples(samples)
    (a_rot, a_tr), (b_rot, b_tr) = opencv_samples

    method = AVAILABLE_ALGORITHMS[algorithm]
    x_rot, x_tr = cv2.calibrateHandEye(a_rot, a_tr, b_rot, b_tr, method=method)
    result = tfs.affines.compose(np.squeeze(x_tr), x_rot, [1, 1, 1])
 #   print("Computed calibration: {}".format(str(result)))
   
    (hcqw, hcqx, hcqy, hcqz) = [float(i) for i in tfs.quaternions.mat2quat(x_rot)]
    (hctx, hcty, hctz) = [float(i) for i in x_tr]
    result_tuple = ((hctx, hcty, hctz), (hcqx, hcqy, hcqz, hcqw))
    return result_tuple
result = []
with open(filename, "r") as f:
    f.readline()
    for i, line in enumerate(f):
        if i % 5 == 0:
            tmp_dict = dict()
        if i % 5 == 4:
            result.append(tmp_dict)
            continue
        row = line.split()

        p = np.array([float(x) for x in row[2:]], dtype=float)
        tmp_dict[row[0] + " " + row[1][:-1]] = p

sample = tuple(result)
'''
for item in result:
    print(item)
'''
print('#01. Tsai-Lenz:')
a1,b1 = compute_calibration(sample,'Tsai-Lenz')
a2,b2 = compute_calibration2(sample,'Tsai-Lenz')

print("c2b trans: ", np.asarray(a1))
print("c2b quat: ", np.asarray(b1))
print("t2g trans: ", np.asarray(a2))
print("t2g quat: ", np.asarray(b2))

print('#02. Park:  ')
a1,b1 = compute_calibration(sample,'Park')
a2,b2 = compute_calibration2(sample,'Park')

print("c2b trans: ", np.asarray(a1))
print("c2b quat: ", np.asarray(b1))
print("t2g trans: ", np.asarray(a2))
print("t2g quat: ", np.asarray(b2))

print('#03. Horaud: ')
a1,b1 = compute_calibration(sample,'Horaud')
a2,b2 = compute_calibration2(sample,'Horaud')

print("c2b trans: ", np.asarray(a1))
print("c2b quat: ", np.asarray(b1))
print("t2g trans: ", np.asarray(a2))
print("t2g quat: ", np.asarray(b2))

print('#04. Andreff: ')
a1,b1 = compute_calibration(sample,'Andreff')
a2,b2 = compute_calibration2(sample,'Andreff')

print("c2b trans: ", np.asarray(a1))
print("c2b quat: ", np.asarray(b1))
print("t2g trans: ", np.asarray(a2))
print("t2g quat: ", np.asarray(b2))

print('#05. Daniilidis: ')
a1,b1 = compute_calibration(sample,'Daniilidis')
a2,b2 = compute_calibration2(sample,'Daniilidis')

print("c2b trans: ", np.asarray(a1))
print("c2b quat: ", np.asarray(b1))
print("t2g trans: ", np.asarray(a2))
print("t2g quat: ", np.asarray(b2))

