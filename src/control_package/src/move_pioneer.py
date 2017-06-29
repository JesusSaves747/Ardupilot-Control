#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

pi = 3.142


def move():
        
    #required to access ros. If this gives an error, make sure you are running roscore on your machine.
    rospy.init_node('Pioneer_move')

    twist= Twist()

    #advertise the topic we wish to publish. Roscore will connect us to the other processes that wish to read from this topic
    p = rospy.Publisher('/pioneer/cmd_vel', Twist, queue_size=10)



    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():

            param_move = rospy.get_param('Move_Pioneer')

            if (param_move ==1):

                # Try simple circular motion: 
                twist.linear.x =0.01
                twist.angular.z= 0 #pi/100

                # publish new velocity
                p.publish(twist)

                rate.sleep()




if __name__ == '__main__':


    try:
        move()

    except rospy.ROSInterruptException:
        pass


