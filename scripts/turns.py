#!/usr/bin/env python
from turtlebot3_msgs.msg import turns
import pygame
import roslib
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String



turns_pub = rospy.Publisher('/turns_num', turns, queue_size=1)


def keyboardLoop():

    rospy.init_node('teleop')
    rate = rospy.Rate(30)
    print(pygame.init())
    screen = pygame.display.set_mode((200, 10))
    pygame.display.set_caption("keep me on top")

    while not rospy.is_shutdown():
        key_list = pygame.key.get_pressed()
        msg = turns()
        if key_list[pygame.K_SPACE] : 
            msg.num=0
        elif key_list[pygame.K_1]:
            msg.num=1
        elif key_list[pygame.K_2]:
            msg.num=2
        elif key_list[pygame.K_3]:
            msg.num=3
        turns_pub.publish(msg)
        pygame.display.update()
        pygame.event.pump()
        rate.sleep()

if __name__ == '__main__':
    try:
        keyboardLoop()
    except rospy.ROSInterruptException:
        pass
