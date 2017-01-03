#!/usr/bin/env python

# The hash followed by exclamation mark ' #!' is used to specify the interpreter to be used to make this script an executable

import roslib

# This line is for Bootstrapping reasons:
roslib.load_manifest('klt_tracker')

# Allows Python developers to use ROS functionality:
import rospy

import sys


# Import OpenCV libraries:
import cv2 as cv

#I don't have cv1 so can't import it:
#import cv as cv1



from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



# Define the class that converts:
class image_converter:

    # This is a constructor for the class image converter:
  def __init__(self):

    # Create a capture object to read in the video from the stream or video file:
    cap= cv.VideoCapture('/home/savio/Documents/Computer_Vision/Study/Template matching/Ch#3_GoPro_edited.mp4')

    # Create a publisher object:

    # Arg #1: Topic Name , Arg #2: Type of message being published:

    self.image_pub = rospy.Publisher("image_topic",Image,queue_size=10)
    #
    # # Create a window for displaying the image:
    # cv.NamedWindow("Image window", 1)

    # Create a cv_bridge object:
    self.bridge = CvBridge()

    # Create an image subscriber object:

    # Arg #1: Topic Name , Arg #2: Type of message being subscribed to:
    self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)


    # This is a very dangerous loop:
    while(True):

        # Extract each frame from the stream:
        ret, image = cap.read()

        print(ret)

        if (cv.waitKey(25)>0):
            break

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(image, "bgr8"))

        except CvBridgeError, e:
          print e



  def callback(self,data):

    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    except CvBridgeError, e:

      print e

    (cols,rows) = cv.GetSize(cv_image)
    if cols > 60 and rows > 60 :
      cv.Circle(cv_image, (50,50), 10, 255)

    cv.ShowImage("Image window", cv_image)
    cv.WaitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError, e:
      print e



def main(args):

    # Initialize a ROS node:
  rospy.init_node('KLT_Tracker', anonymous=True)

  # Instantiate an 'image_converter' object:
  ic = image_converter()


  # Keep looping on until the user presses a key:
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
