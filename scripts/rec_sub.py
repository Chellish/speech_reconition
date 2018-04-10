#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import re
from std_msgs.msg import Int32
from time import sleep

def callback(msg):
    print msg.data
    sleep(300)


rospy.init_node('subscriber')

sub = rospy.Subscriber('recognition',Int32,callback)

rospy.spin()

