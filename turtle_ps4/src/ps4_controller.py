#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from m2_ps4.msg import Ps4Data
from turtlesim.srv import SetPen
from std_srvs.srv import Empty
# hint: some imports are missing

multi_pos = 0
old_data = Ps4Data()

def callback(data):
    global old_data
    global multi_pos
    
    speed_multi =[1,1.5,2,2.5,3]
    
    
    vel = Twist()
    
    vel.angular.z = speed_multi[multi_pos] * data.hat_rx
    vel.linear.x = speed_multi[multi_pos] * data.hat_ly
    
    # you should publish the velocity here!
    pub.publish(vel)
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # 
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...
    
    # ps button clears the trail
    if ((data.ps == True) and (old_data.ps == False)):
    	srv_clear()
    
    #shape buttons change color
    if ((data.cross == True) and (old_data.cross == False)):
    	srv_col(0,0,255,2,0)
    
    if ((data.circle == True) and (old_data.circle == False)):
    	srv_col(255,0,0,2,0)
    
    if ((data.triangle == True) and (old_data.triangle == False)):
    	srv_col(0,255,0,2,0)
    
    if ((data.square == True) and (old_data.square == False)):
    	srv_col(128,0,128,2,0)
    
    
    #change multiplier levels
    if ((data.dpad_y == 1) and (old_data.dpad_y == 0)):
        multi_pos += 1
    	
    if ((data.dpad_y == -1) and (old_data.dpad_y == 0)):
        multi_pos -= 1
    
    if multi_pos>4:
    	multi_pos=4
    	
    if multi_pos<0:
    	multi_pos=0
    
    old_data = data

if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1) # publisher object goes here... hint: the topic type is Twist
    sub = rospy.Subscriber('/input/ps4_data', Ps4Data, callback) # subscriber object goes here
    
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy('/turtle1/set_pen', SetPen)# service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...
    srv_clear = rospy.ServiceProxy('/clear', Empty)
    rospy.spin()
