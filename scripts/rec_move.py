#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import re
import serial
from std_msgs.msg import Int32

def callback(msg):
    #COMポートの設定
    ser = serial.Serial(0,9600,serial.PARITY_NONE,serial.EIGHTBITS,serial.STOPBITS_ONE,1)
    print ser.portstr
    ser.write
    print msg.dat

rospy.init_node('subscriber')

sub = rospy.Subscriber('recognition',Int32,callback)

rospy.spin()

