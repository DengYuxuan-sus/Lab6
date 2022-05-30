#! /usr/bin/env python

import rospy
import time
from geometry_msgs.msg import PoseStamped

if __name__ == '__main__':
    rospy.init_node('pubpose')
    turtle_vel_pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=1)
    
    mypose=PoseStamped()
    turtle_vel_pub.publish(mypose) 
    time.sleep(1)
    
    # mypose=PoseStamped()
    # mypose.header.frame_id='map'
    # mypose.pose.position.x=3.89705848694
    # mypose.pose.position.y= 1.79976141453
    # mypose.pose.position.z=0.0
    # mypose.pose.orientation.x=0
    # mypose.pose.orientation.y=0
    # mypose.pose.orientation.z=0.630159199169
    # mypose.pose.orientation.w=0.776465957852

    mypose=PoseStamped()
    mypose.header.frame_id='map'
    mypose.pose.position.x=0.356288671494
    mypose.pose.position.y= -0.126959264278
    mypose.pose.position.z=0.0
    mypose.pose.orientation.x=0
    mypose.pose.orientation.y=0
    mypose.pose.orientation.z=0
    mypose.pose.orientation.w=1

    # mypose=PoseStamped()
    # mypose.header.frame_id='map'
    # mypose.pose.position.x=2.26973342896
    # mypose.pose.position.y=-3.71048784256
    # mypose.pose.position.z=0.0
    # mypose.pose.orientation.x=0
    # mypose.pose.orientation.y=0
    # mypose.pose.orientation.z=0.351069806366
    # mypose.pose.orientation.w=0.936349289025

    
    turtle_vel_pub.publish(mypose)

    time.sleep(5)
