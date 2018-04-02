#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import re
from std_msgs.msg import Int32

def callback(msg):
    print msg.data

rospy.init_node('subscriber')

sub = rospy.Subscriber('recognition',Int32,callback)

rospy.spin()

