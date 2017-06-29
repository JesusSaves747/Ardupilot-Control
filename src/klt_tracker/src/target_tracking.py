## Import all modules and packages here: 

import numpy as np
import cv2
import rospy
import roslib

roslib.load_manifest('klt_tracker')


# Import cv_bridge stuff:
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import TwistStamped   # To obtain the pose of the UAV: 


## Define parameters for the Detector and Tracker:

# 1.  params for ShiTomasi corner detector
feature_params = dict(maxCorners=20,
                      qualityLevel=0.5,
                      minDistance=2,
                      blockSize=2)

# 2. Params for ORB feature detector: TO DO:



# Initialize Parameters for Lucas Kanade optical flow tracker:
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


# Create some random colors
color = np.random.randint(0, 255, (100, 3))




## Define the callback functions here: 

# 1. Feature based target tracker: 
def feature_tracker(image_msg):

    global feature_params , lk_params

    


# 2. Color based Target Tracker: 
def 


# 3. Pose recovery callback: 
def pose_recover(pose_msg):


## Define the Main function here: 

if __name__ == '__main__':

    global bridge
    global window
    global pub

    bridge = CvBridge()


    # STEP 1: Create a ROS node that subscribes/publishes to the following topics: 
    # 1. image_front - Front Camera feed: 
    # 2. mavros_pose - Pose of the UAV: 
    # 3. mavros_setposition/local - The reference position for the UAV: 


    # Initialize node:
    rospy.init_node("TARGET TRACKER")

    print "TARGET TRACKING NODE Initialized"

    # Create a publisher for the setpoint_position topic: Verify the topic name
    pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)

    # Create subscriber that subscribes to the Front camera feed: 
    rospy.Subscriber('/mavros/camera1/image_raw',Image,feature_target_track)

    # Create a subscriber that subscribes to the Pose topic of the UAV: need to get the name: 
    rospy.Subscriber('/mavros/pose',Image,pose_recover)

    rospy.spin()