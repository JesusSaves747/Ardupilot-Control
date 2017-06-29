#!/usr/bin/env python

import numpy as np
import cv2
import rospy
import roslib
roslib.load_manifest('klt_tracker')



# Import cv_bridge stuff:
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import TwistStamped

## Begin here:


## STEP 0: Define the calback for the subscriber topic:
# Tasks:
# 1. Acquire the ROS image and convert to cv mat format:

# 2. Run an edge detection algorithm to detect the landing box:

# 3. Identify and extract co-ordinates of the center of the box:


# 4. Publish velocities on cmd_vel topic based on error in image frame:

# 5. Display the image in a CV window frame:



def PID_visual_servo(msg):

    global bridge
    global window
    global pub

    ex=0
    ey=0

    font = cv2.FONT_HERSHEY_SIMPLEX

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

    ################ ----------------------------------------------------   ########################
    ## Approach #2: Color masking followed by edge detection: 

    # # Loop over the boundaries
    # for (lower, upper) in boundaries:
    #     # create NumPy arrays from the boundaries
    #     lower = np.array(lower, dtype = "uint8")
    #     upper = np.array(upper, dtype = "uint8")
    
    #     # find the colors within the specified boundaries and apply
    #     # the mask
    #     mask = cv2.inRange(cv_mat_image, lower, upper)
    #     output = cv2.bitwise_and(cv_mat_image, cv_mat_image, mask = mask)
    
    # # Run a canny edge detector on the masked image: 
    # edges = cv2.Canny(mask, 120 , 150)

    # # Run a countour detector on the edged image: There should be only one contour now:
    # im2, contours , hier= cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for cnt in contours:
    #     area_cnt = cv2.contourArea(cnt)

    #     if area_cnt >50:
    #         M = cv2.moments(cnt)

    #         cx = int(M['m10']/M['m00'])
    #         cy = int(M['m01']/M['m00'])

    #         ex = (height/2) - cx
    #         ey = (width/2) - cy

    #         cv2.drawContours(cv_mat_image, [cnt], 0 , (255,0,0), 3)
    #         cv2.circle(cv_mat_image, (cx,cy), 10, (0,0,255), 2)
    #         cv2.putText(cv_mat_image,str([ex,ey]),(cx,cy), font, 1,(255,255,255),2,cv2.LINE_AA)


    ################ ----------------------------------------------------   ########################

    #Approach # 1: Task # 2:

    imgray = cv2.cvtColor(cv_mat_image, cv2.COLOR_BGR2GRAY)

    

    
  
    # Apply a Canny edge detector to find the edge points in the image frame: What are the thresholding parameters?
    edges = cv2.Canny(imgray, 100,200)

    # # Find contours in the detected image using algorithm by Suzuki 1985: 
    im2, contours , hier= cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        # # Take the first contour: 
        area_cnt = cv2.contourArea(cnt)

        perimeter = cv2.arcLength(cnt,True)


        if perimeter > 500:
        # I'm guessing this returns a dictionary: 
            M = cv2.moments(cnt)

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            ex = (height/2) - cx
            ey = (width/2) -cy

            cv2.drawContours(cv_mat_image, [cnt], 0 , (255,0,0), 3)
            cv2.circle(cv_mat_image, (cx,cy), 10, (0,0,255), 2)
            cv2.putText(cv_mat_image,str([ex,ey]),(cx,cy), font, 1,(255,255,255),2,cv2.LINE_AA)
    

    # Task #3: Publish a cmd_vel command based on the error in x and y co-ordinates: 

    velMsg = TwistStamped()

    # Simple proportional control:
    velMsg.twist.linear.x = -0.7*ex
    velMsg.twist.linear.y = -0.7*ey


    pub.publish(velMsg)



    

    # Task # 5:
    # Display the resulting frame
    


    
    # Use cv2.waitKey(3) : Somehow that worked: TO DO: Try waitkey(someOtherNumber)
    #cv2.imshow('Window',np.hstack([cv_mat_image, output]))
    cv2.imshow('Window',cv_mat_image)
    cv2.waitKey(1)


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
    pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)

    # Create subscriber:
    rospy.Subscriber('/mavros/camera1/image_raw',Image,PID_visual_servo)

    rospy.spin()
