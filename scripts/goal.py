#! /usr/bin/env python

import rospy
import time
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalStatusArray
from move_base_msgs.msg import MoveBaseActionResult
from lane_following_part3 import turns
i=1
status=1
def result_cb(msg):
    global i ,status
    # print(msg)
    if(msg.status.status==3):
        rospy.loginfo("reach")
        i+=1
        status=1


if __name__ == '__main__':
    rospy.init_node('pubpose')
    turtle_vel_pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=1)
    result_sub=rospy.Subscriber('move_base/result',MoveBaseActionResult,result_cb)
    rate = rospy.Rate(100) 
    mypose=PoseStamped()


    while not rospy.is_shutdown():
        # rospy.loginfo(status)
        
        time.sleep(1)
        if status==1:
            if i ==1:
                 
                mypose=PoseStamped()
                mypose.header.frame_id='map'
                mypose.pose.position.x=3.89705848694
                mypose.pose.position.y= 1.79976141453
                mypose.pose.position.z=0.0
                mypose.pose.orientation.x=0
                mypose.pose.orientation.y=0
                mypose.pose.orientation.z=0.630159199169
                mypose.pose.orientation.w=0.776465957852
                status=0
            elif i==2:
                # mypose=PoseStamped()
                # turtle_vel_pub.publish(mypose) 
                mypose=PoseStamped()
                mypose.header.frame_id='map'
                mypose.pose.position.x=0.356288671494
                mypose.pose.position.y= -0.126959264278
                mypose.pose.position.z=0.0
                mypose.pose.orientation.x=0
                mypose.pose.orientation.y=0
                mypose.pose.orientation.z=0
                mypose.pose.orientation.w=1
                status=0

            elif i==3:
                # mypose=PoseStamped()
                # turtle_vel_pub.publish(mypose) 
                mypose=PoseStamped()
                mypose.header.frame_id='map'
                mypose.pose.position.x=2.26973342896
                mypose.pose.position.y=-3.71048784256
                mypose.pose.position.z=0.0
                mypose.pose.orientation.x=0
                mypose.pose.orientation.y=0
                mypose.pose.orientation.z=0
                mypose.pose.orientation.w=1
                status=0
            elif i==4:
                # mypose=PoseStamped()
                # turtle_vel_pub.publish(mypose) 
                mypose=PoseStamped()
                mypose.header.frame_id='map'
                mypose.pose.position.x=5.87116527557
                mypose.pose.position.y=-1.72441291809
                mypose.pose.position.z=0.0
                mypose.pose.orientation.x=0
                mypose.pose.orientation.y=0
                mypose.pose.orientation.z=0.999004570943
                mypose.pose.orientation.w=1
                status=0
                rospy.loginfo("navigation is over!")


        turtle_vel_pub.publish(mypose)  
        time.sleep(5)
        rate.sleep()

           
            





    


    


    
