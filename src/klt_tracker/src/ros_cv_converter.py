#!/usr/bin/env python

from __future__ import print_function

# The hash followed by exclamation mark ' #!' is used to specify the interpreter to be used to make this script an executable
import roslib
roslib.load_manifest('klt_tracker')
import sys
import rospy


# Import opencv libraries:
import cv2


from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError




# Define the class that carries out the conversion:
class image_converter:

  

    # Constructor for the "image_converter class"
  def __init__(self):
      # Create a capture object to read in the video from the stream or video file:
    #cap = cv2.VideoCapture('/home/savio/Documents/Computer_Vision/Study/Template matching/Ch#3_GoPro_edited.mp4')

    cap = cv2.VideoCapture(0)

  # Create a publisher object:

  # Arg #1: Topic Name , Arg #2: Type of message being published:
    self.image_pub = rospy.Publisher("image_topic",Image,queue_size=10)

  # Create an object of the type CvBridge
    self.bridge = CvBridge()

  # Create an image subscriber object:

  # Arg #1: Topic Name , Arg #2: Type of message being subscribed to:

    self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)

    # This is a very dangerous loop:
    while (True):

        # Extract each frame from the stream:
        ret, image = cap.read()

        #print(ret)

        # ch= cv2.waitKey(-2)
        #
        # if ch == 27:
        #     cv2.destroyAllWindowsWindow()
        #     break

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(image, "bgr8"))

        except CvBridgeError, e:
            print(e)




  def callback(self,data):

    try:

        # Conver the image message to CV2 format: what is bgr8? Blue , Green Red 8- bit float?
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    except CvBridgeError as e:
      print(e)

    # Extract the shape of the image:
    (rows,cols,channels) = cv_image.shape

    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    cv2.imshow("Image window", cv_image)

    # What does waitkey (3) do?
    cv2.waitKey(1)

    # try:
    #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    # except CvBridgeError as e:
    #   print(e)

def main(args):

  rospy.init_node('image_converter', anonymous=True)

    # Instantiate an object of the class:
  ic = image_converter()


  try:

    rospy.spin()


  except KeyboardInterrupt:

    print("Shutting down")

  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)