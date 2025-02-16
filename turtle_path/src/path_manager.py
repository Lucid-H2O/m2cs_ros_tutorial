#!/usr/bin/env python
import rospy
from math import pi, fmod, sin, cos, sqrt
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_path.srv import *
# hint: some imports are missing

cur_pos = Pose()

def cb_pose(data): # get the current position from subscribing the turtle position
    global cur_pos
    cur_pos = data

def cb_walk(req):
    if (req.distance < 0):
        return False
        
    projected_x = cur_pos.x + req.distance*cos(cur_pos.theta)
    projected_y = cur_pos.y + req.distance*sin(cur_pos.theta)
    
    if projected_x > 11 or projected_x<0:
    	return False
    if projected_y> 11 or projected_y<0:
    	return False

    # hint: calculate the projected (x, y) after walking the distance,
    # and return false if it is outside the boundary

    rate = rospy.Rate(100) # 100Hz control loop

    while (abs(projected_x - cur_pos.x ) > 0.05): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: you need to use the formula for distance between two points
        velocity = Twist()
        dist = sqrt( (projected_x-cur_pos.x) ** 2  + (projected_y-cur_pos.y) ** 2 )
        velocity.linear.x = dist
        pub.publish(velocity)
        
        rate.sleep()
    
    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    pub.publish(vel)
    
    return True

def cb_orientation(req):

    rate = rospy.Rate(100) # 100Hz control loop
    
    while (abs(req.orientation - cur_pos.theta) >0.05): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: signed smallest distance between two angles: 
        # see https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        #     dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        vel = Twist()
        vel.angular.z = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        pub.publish(vel)
        rate.sleep()
    
    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    pub.publish(vel)

    return True

if __name__ == '__main__':
    rospy.init_node('path_manager')
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1) # publisher of the turtle velocity
    sub = rospy.Subscriber('/turtle1/pose', Pose, cb_pose) # subscriber of the turtle position, callback to cb_pose
    
    ## init each service server here:
    success = rospy.Service( 'set_orientation' ,SetOrientation, cb_orientation)
    success = rospy.Service( 'walk_distance',WalkDistance , cb_walk)	
    # rospy.Service( ... )		# callback to cb_orientation
    # rospy.Service( ... )		# callback to cb_walk
    
    rospy.spin()
