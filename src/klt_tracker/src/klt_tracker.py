#!/usr/bin/env python
import roslib

# Dont know what this line does:
roslib.load_manifest('klt_tracker')

import sys
import rospy
import cv2 as cv
import cv as cv1
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):

    # Create a capture object to read in the video:
    cap= cv.VideoCapture('/home/savio/Documents/Computer_Vision/Study/Template matching/Ch#3_GoPro_edited.mp4')

    # Create a publisher object:
    # Arg #1: Topic Name , Arg #2: Type of message being published:
    self.image_pub = rospy.Publisher("image_topic",Image,queue_size=10)
    #
    # # Create a window for displaying the image:
    # cv.NamedWindow("Image window", 1)

    # Create a cv_bridge object:
    self.bridge = CvBridge()

    # Create an image sunscriber object:
    self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)

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

    (cols,rows) = cv1.GetSize(cv_image)
    if cols > 60 and rows > 60 :
      cv2.Circle(cv_image, (50,50), 10, 255)

    cv.ShowImage("Image window", cv_image)
    cv.WaitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError, e:
      print e

def main(args):

  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
