#!/usr/bin/env python

## Import all modules and packages here: 

from collections import deque
import numpy as np
import cv2
import rospy
import roslib
roslib.load_manifest('klt_tracker')

import transforms3d as t3
import math
import tf
import sys





# Import cv_bridge stuff:
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import PoseStamped   # To obtain the pose of the UAV: 
from geometry_msgs.msg import TwistStamped   # To obtain the velocity of the UAV: 
from control_package.msg import target_coods    # To publish the co-ordinates of the target:

# Import the custom msg here: 
from control_package.msg import bBox


# Focal length of the camera: 
global f
global target_found



target_found = False
f = 320   # Needed in units of pixel dimensions. Verified in Gazbeo  # TO DO: Make this a ROS parameter that can be adjusted: 


# Class of UAV target trackers: Define a parameter that changes the type of Tracker: 
class Target_Tracker():

    # Define the constructor for this class: 
    # Initialize all parameters here: 
    def __init__(self, type ): 

        # 1.  params for ShiTomasi corner detector
        self.feature_params = dict(maxCorners=20,
                      qualityLevel=0.5,
                      minDistance=2,
                      blockSize=2)

        # 2.  Initialize Parameters for Lucas Kanade optical flow tracker:
        self.lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        #  Create some random colors
        self.color = np.random.randint(0, 255, (100, 3))

        # Initialize flags:
        self.pts = deque(maxlen=20)
        self.xTargetPts = deque(maxlen=15)
        self.yTargetPts = deque(maxlen=15)
        self.count = 0
        self.boxDone = False
        self.gotFeatures = False
        self.target_found = False
        self.lostCounter = 0

        # Initialize target co-ordinates in image and NED Frame: 
        self.xt_im = 0
        self.yt_im = 0
        self.xt_im_c =0
        self.yt_im_c =0

        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then
        self.greenLower = (39, 100, 60)
        self.greenUpper = (54, 200, 200)

        # Co-ordinates of the bounding box: 
        self.top_left_x = 0
        self.top_left_y = 0
        self.width = 0
        self.height = 0

        self.gotBox = False


        self.moving = False

        self.count = 0

        self.RefPose = PoseStamped()


        print(sys.executable)
        print(cv2.__version__)

        # Create an MIL tracker object: 
        #self.trackerMIL = cv2.TrackerMIL_create()



        # Create a publisher to the Set reference point topic: 

        self.pub = rospy.Publisher('/savio/Pose', PoseStamped, queue_size=10)

        #self.pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)

        # Create a publisher to the Set reference point topic: 
        self.pub_imag = rospy.Publisher('/mavros/camera1/image_proc', Image, queue_size=10)

        # Create a publisher to publish the target co-ordinates: 
        self.pub_target = rospy.Publisher('/ANRA/target', target_coods, queue_size=10)

        # Create a subscriber that subscribes to the Pose topic of the UAV: need to get the name: 
        # The type of msg on this topic is : geometry_msgs/PoseStamped
        rospy.Subscriber('/mavros/local_position/pose', PoseStamped ,self.pose_recover)

        # Subscriber to check whether the UAV is in motion:
        rospy.Subscriber('/mavros/local_position/velocity', TwistStamped ,self.motion_recover)



        # Create subscriber that subscribes to the Front camera feed: The call back to the subscriber depends on the type of tracker: 
        if (type == 'Color'):
            
            rospy.Subscriber('/mavros/camera1/image_rect_color',Image,self.color_tracker)

        elif (type == 'Feature'):
            rospy.Subscriber('/mavros/camera1/image_raw',Image,self.feature_target_track) # Learn how to assign additional arguments to the callback:
            rospy.Subscriber('savio/bBoxParams',bBox , self.defineBbox)




    ## Define the callback functions here: 

    # 1. Feature based target tracker: 
    def feature_tracker(self,image_msg):

        param_val = rospy.get_param('Start_Tracker')

        if (param_val ==1 ):

            # Setup the bounding box:
            bbox = (self.top_left_x , self.top_left_y ,self.width , self.height)  # Bounding box is specified as : ( x, y, w , h):

            # Convert the image message to OpenCV Mat format: 
            try:
                image = bridge.imgmsg_to_cv2(image_msg, "bgr8")

                height, width , channels = cv_mat_image.shape

            except CvBridgeError as e:
                print(e)

        
            # Initialize the MIL tracker: 
            okMIL = trackerMIL.init(image, bbox)

            # IF MIL tracker is working then draw a box and put the text in it:
            if okMIL:

                p1 = (int(newboxMIL[0]), int(newboxMIL[1]))
                p2 = (int(newboxMIL[0] + newboxMIL[2]), int(newboxMIL[1] + newboxMIL[3]))
                cv2.rectangle(image, p1, p2, (255,0,0))
                cv2.putText(image, " MIL Tracker ", (10 , 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0))

                cx = int(newboxMIL[0] + newboxMIL[2]/2)
                cy = int(newboxMIL[1] + newboxMIL[3]/2)

                center =(cx,cy)


                # update the points queue
                pts.appendleft(center)

                ## Section 5: Plot the trajectory of the Centers of the detected object:

                # loop over the set of tracked points
                for i in range(1, len(pts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if pts[i - 1] is None or pts[i] is None:
                        continue

                    # otherwise, compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(20/ float(i + 1)) * 1.5)
                    cv2.line(image, pts[i - 1], pts[i], (255, 0, 0), thickness)


                
                # Convert image back to ros_image_msg and publish of image_proc topic
                try:
                    self.pub_imag.publish(bridge.cv2_to_imgmsg(image, "bgr8"))

                except CvBridgeError as e:
                    print(e)
        


    # 2. Color based Target Tracker: 
    def color_tracker(self,image_msg): 

        # Get the parameter to indicate whether to start tracking:
        startTracking = rospy.get_param('Start_Tracker')


        if (startTracking ==1 ):

            # Convert the image message to OpenCV Mat format: 
            try:
                frame = bridge.imgmsg_to_cv2(image_msg, "bgr8")

                height, width , channels = frame.shape

            except CvBridgeError as e:
                print(e)

            # Apply a guassian blur to the image:
            blurred = cv2.GaussianBlur(frame, (5, 5), 0)


            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(blurred, (0, 90 , 0) ,( 5, 110 , 5)) #self.greenLower, self.greenUpper)
            mask = cv2.erode(mask, None, iterations=2)   # TO DO: Understand this operation
            mask = cv2.dilate(mask, None, iterations=2)  # TO DO: Understand this operation


            ## Section 4: Extract the centroid of the detected object:

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None


            # only proceed if at least one contour was found
            if len(cnts) > 0:

                # Zero the counter for lost target:
                self.lostCounter = 0

                # Update the flag that the target was found: 
                self.target_found = True

                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((self.xt_im, self.yt_im), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(self.xt_im), int(self.yt_im)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

                    cv2.putText(frame, " Target in Sight: ", (int(self.xt_im), int(self.yt_im)), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                                (0, 255, 0))

            else:

                
                # Increment the lost counter:
                self.lostCounter = self.lostCounter + 1

                # Change the target_found flag: 
                self.target_found = False

                #cv2.circle(frame, (int(self.xt_im), int(self.yt_im)), int(radius*lostCounter*0.05),
                    #   (0, 255, 255), 2)

                cv2.putText(frame," Target Lost: Last Seen",(int(self.xt_im), int(self.yt_im)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255))

            # Update the points double ended queue: 
            self.pts.appendleft(center)


            ## Section 5: Plot the trajectory of the Centers of the detected object:
            x_im=[]
            y_im=[]

            # loop over the set of tracked points
            for i in xrange(1, len(self.pts)):
                # if either of the tracked points are None, ignore
                # them
                if self.pts[i - 1] is None or self.pts[i] is None:
                    continue

                x_im.append((self.pts[i])[0])
                y_im.append((self.pts[i])[1])


                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(20 / float(i + 1)) * 1.5)
                cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)

            
            if x_im and y_im:
                ## 24th June 2017: Trying a moving average filter over the detected co-ordinates: 
                avg_x= sum(x_im)/len(x_im)
                avg_y = sum(y_im)/len(y_im)

                cv2.circle(frame, (avg_x, avg_y), 3, (255, 0, 0), -1)
                cv2.putText(frame," Average",(int(self.xt_im), int(self.yt_im)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0))



            # Convert image back to ros_image_msg and publish of image_proc topic
            try:
                self.pub_imag.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
            except CvBridgeError as e:
                print(e)


            

            # The co-ordinates found are in the image frame with origin at the top left. But we want the co-ordinates with the origin at the center: 
            self.xt_im_c = (self.xt_im - (width/2))
            self.yt_im_c = -1*(self.yt_im - (height/2))

            # print (" Image Pixel Center co-ods are:")
            # print(" x = ", self.xt_im_c)
            # print(" y = ", self.yt_im_c)



         
        


    # 3. Pose recover: callback to the UAV Pose topic 
    # Description: This function estimates the Position of the target in the global (NED) frame by using the pose of the UAV 
    # and the extracted image co-ordinates of the target. The assumption here is that the Target always remains on the ground plane. 
    # Thus, we know that its z-co-ordinate is always equal to zero. z_ned =0

    def pose_recover(self,pose_msg):

        # Get latest parameter values:
        tarHeight = rospy.get_param('Target_Height')
        follDist = rospy.get_param('Following_Distance')
        startFoll = rospy.get_param('Start_Following')

        # Extract the UAV pose from the message: The type of message is geometry_msgs/PoseStamped
        # 1. Extract the X,Y,Z, co-ods of UAV in NED frame
        x_uav = pose_msg.pose.position.x
        y_uav = pose_msg.pose.position.y
        z_uav = pose_msg.pose.position.z

        # Account for the camera pose w.r.t the UAV: 
        z_cam = z_uav - 0.2

        #print("UAV X-cod: " , x_uav)
        #print("UAV Y-cod: " , y_uav)

        

        if self.target_found: # and not self.moving:  


            # 2. Extract the quaternion describing orientation of UAV in NED frame: 
            # Confirm whether this is UAV -> NED or NED -> UAV: 
            q_uav = pose_msg.pose.orientation

            quat = [q_uav.x , q_uav.y , q_uav.z , q_uav.w]            

            # Convert the quaternion of UAV pose to the Rotation matrix/ Direction Cosine matrix: Verify this computation of Rotation matrix: 
            R_n_uav = tf.transformations.quaternion_matrix(quat)  # CHECK THIS ONE: Checked!


            R_uav_c= np.matrix('0 0 1 ; -1 0 0; 0 1 0')


            # Now compose this with the fixed rotation matrix from UAV to camera: 
            R = np.dot(R_n_uav[0:3,0:3], R_uav_c)

            # TO DO: Perform Intrinsic and Extrinsic calibration of a camera for practice. 

            
            # Compute lamda - Scaling parameter: Image co-ordinates need to be in units of meters I guess not pixels
            lam = (tarHeight - z_cam)/( R[2,0]*self.xt_im_c/f + R[2,1]*self.yt_im_c/f + R[2,2] )

            # print " Lamda : Depth of Target in Camera frame" # Should be 1.5
            print (" Lambda is: ")
            print lam



            # Compute the x and y co-ordinates of the target in the NED frame: 
            # 1. x - co-ordinate: 
            x_ned_curr = lam*(R[0,0]*(self.xt_im_c)/f  +  R[0,1]*self.yt_im_c/f  + R[0,2]) + x_uav

            # 2. y - co-ordinate: 
            y_ned_curr = lam*(R[1,0]*(self.xt_im_c)/f  +  R[1,1]*self.yt_im_c/f  + R[1,2]) + y_uav


            # Append the Target co-ods to the list of available points: 
            self.xTargetPts.appendleft(x_ned_curr)
            self.yTargetPts.appendleft(y_ned_curr)


            x_ned = sum(self.xTargetPts)/len(self.xTargetPts)
            y_ned = sum(self.yTargetPts)/len(self.yTargetPts)           
            



            # # Print out the target co-ods: Should be  x= 3 , y = 3
            # print "Estimated X-cod of target"
            # print x_ned
            # print "Estimated Y-cod of target"
            # print  y_ned


            # Compute the reference yaw/heading attitude of the UAV: 
            psi = math.atan2(  (y_ned -y_uav) ,(x_ned - x_uav)  )

            #print("Ref Angle is ", psi)

        
            
            # Compute the reference position for the UAV: 
            # 1. First compute the eucidean distance between UAV and target in X-Y Plane: 
            uav_target = math.sqrt ((x_ned - x_uav)**2 + (y_ned - y_uav) **2)

            #print("UAV target dist =" , uav_target)

            # 2. Compute the euclidean distance from reference point to UAV: 
            # We are given that specified distance between target and UAV is 2 meters: 
            uav_ref = uav_target - follDist  # TO DO : Get this in as a parameter from the user: DONE!

            # 3. Use trigonometry to get the x and y -cordinates of the reference position: 
            x_ref = x_uav + uav_ref*math.cos(psi)
            y_ref = y_uav + uav_ref*math.sin(psi)

            # print("Ref X-cod: " , x_ref)
            # print("Ref Y-cod: " , y_ref)


            # Compute the reference quaternion from the Euler angles: 
            # Set the reference pitch and roll to zero: 
            eul = [0 , 0 , psi]

            # Transform the euler angles to a quaternion: 
            q_ref = tf.transformations.quaternion_from_euler(0,0,psi)

            # Publish the Reference position and attitude to the specified topic: 
            if not self.moving:

                self.RefPose.pose.position.x = x_ref
                self.RefPose.pose.position.y = y_ref
                self.RefPose.pose.position.z = z_uav 
                self.RefPose.pose.orientation.x = q_ref[0]
                self.RefPose.pose.orientation.y = q_ref[1]
                self.RefPose.pose.orientation.z = q_ref[2]
                self.RefPose.pose.orientation.w = q_ref[3]




            # Publish the estimated Target co-ordinates:  
            Target = target_coods()

            Target.x = x_ned
            Target.y = y_ned

            self.pub_target.publish(Target)

            if (startFoll ==1):
            
                # Send the message to the publisher: 
                self.pub.publish(self.RefPose)


            # #Increment the counter:
            # self.count +=1

            # print(" Count is:",self.count)


        

    def motion_recover(self,vel_msg):

        x_vel = abs(vel_msg.twist.linear.x)
        y_vel = abs(vel_msg.twist.linear.y)

        ang_x = abs(vel_msg.twist.angular.x)
        ang_y = abs(vel_msg.twist.angular.y)
        ang_z = abs(vel_msg.twist.angular.z)

        if x_vel > 0.1 or y_vel > 0.1 or ang_x >0.08 or ang_y >0.08 or ang_z >0.08:
            self.moving = True
        else:
            self.moving = False
        
        

                
    
    ## 4. Define the Bounding Box co-cordinates: 
    def defineBbox(self,bBox_msg): 

        # Extract the top left co-ordinates: 
        self.top_left_x = bBox_msg.top_left_x
        self.top_left_y = bBox_msg.top_left_y

        # Extract the width and height of the box: 
        self.width  = bBox_msg.width
        self.height = bBox_msg.height

        # Set the flag that the bounding box has been acquired: 
        self.gotBox = True
        

        

    ##  Define the mouse callback function here:
    # Arguments to this function are:
    # 1. event - Which I think is the type of click that occured
    # 2. x , y - X and Y pixel locations of the point selected.
    # 3. flags
    # 4. params
    def click_and_crop(event,x ,y , flags, params):

        # Make the reference points global variables:
        global refPt, count, done

        # Create a if -else case to analyze the type of mouse click:
        if event == cv2.EVENT_LBUTTONDOWN:

            if not done:
                refPt.append((x,y))
                count = count + 1


        # Draw a line between the selected points:

        if event == cv2.EVENT_RBUTTONDOWN:

            done = True





## Define the Main function here: 

if __name__ == '__main__':

    global bridge
    global window
    global pub

    bridge = CvBridge()

    trackerType = sys.argv[1]


    # STEP 1: Create a ROS node that subscribes/publishes to the following topics: 
    # 1. image_front - Front Camera feed: 
    # 2. mavros_pose - Pose of the UAV: 
    # 3. mavros_setposition/local - The reference position for the UAV: 


    # Initialize node:
    rospy.init_node("Tracking")

    print "TARGET TRACKING NODE Initialized"


    TT = Target_Tracker(trackerType)


    rospy.spin()