#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from Ps4Data.msg import Ps4Data
from turtlesim.srv import SetPen
from std_srvs.srv import Empty
# hint: some imports are missing


old_data = Ps4Data()

def callback(data):
    global old_data
    
    speed_multi =[1,1.5,2,2.5,3]
    int multi_pos = 0
    
    vel = Twist()
    
    vel.angular.z = speed_multi[multi_pos] * data.hat_rx
    vel.linear.x = speed_multi[multi_pos] * data.hat_lx
    
    # you should publish the velocity here!
    pub.publish(vel)
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # 
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...
    
    # ps button clears the trail
    if ((data.ps == true) and (old_data.ps == false)):
    	srv_clear()
    
    #shape buttons change color
    if ((data.cross == true) and (old_data.cross == false)):
    srv_col((0,0,255))
    
    if ((data.circle == true) and (old_data.circle == false)):
    srv_col((255,0,0))
    
    if ((data.triangle == true) and (old_data.triangle == false)):
    srv_col((0,255,0))
    
    if ((data.square == true) and (old_data.square == false)):
    srv_col((255,0,255))
    
    
    #change multiplier levels
    if ((data.dpad_y == 1) and (old_data.dpad_y == 0)):
    multi_pos += 1
    	
    if ((data.dpad_x == 1) and (old_data.dpad_x == 0)):
    multi_pos -= 1
    
    if multi_pos>5:
    	multi_pos=5
    	
    if multi_pos<0:
    	multi_pos=0
    
    old_data = data

if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1) # publisher object goes here... hint: the topic type is Twist
    sub = rospy.Subscriber('/input/ps4_data', Ps4Data, queue_size=1) # subscriber object goes here
    
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy('/turtle1/set_pen', SetPen)# service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...
    srv_clear = rospy.ServiceProxy('/clear', Empty)
    rospy.spin()
