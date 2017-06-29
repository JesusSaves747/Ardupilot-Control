#!/usr/bin/env python

# # doing execfile() on this file will alter the current interpreter's
# # environment so you can import libraries in the virtualenv
# activate_this_file = "/home/savio/.virtualenvs/cv/bin/activate_this.py"

# execfile(activate_this_file, dict(__file__=activate_this_file))

import numpy as np
import cv2
import rospy
import roslib
roslib.load_manifest('klt_tracker')



# Import cv_bridge stuff:
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import PoseStamped


def test_callback(msg):

    global bridge
    global window
    global pub

    # Create an MIL tracker:
    #trackerMIL = cv2.TrackerMIL_create()

    print(cv2.__version__)





    # Color boundaries for box:
    boundaries = [
	([45, 70, 90], [55, 80, 100])	
]

    #Task #1:
    
    try:
        cv_mat_image = bridge.imgmsg_to_cv2(msg, "bgr8")

        height, width , channels = cv_mat_image.shape

    except CvBridgeError as e:
      print(e)
    

    # Use cv2.waitKey(3) : Somehow that worked: TO DO: Try waitkey(someOtherNumber)
    #cv2.imshow('Window',np.hstack([cv_mat_image, output]))
    cv2.imshow('Window',cv_mat_image)
    cv2.waitKey(3)



if __name__ == '__main__':

    global bridge
    global window
    global pub

    bridge = CvBridge()

    #window = cv2.namedWindow('frame', cv2.WINDOW_NORMAL)





    # STEP 1: Create a ROS node that subscribes to the topic image_raw:
    # Initialize node:
    rospy.init_node("Visual_Servo")

    print "Vision Detection Node Initialized"

    # Create a publisher for the cmd_vel topic: 
    pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)

    # Create subscriber:
    rospy.Subscriber('/mavros/camera1/image_raw',Image,test_callback)

    rospy.spin()