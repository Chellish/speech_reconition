#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import array
import serial

from std_msgs.msg import Int32

#シリアル通信の設定
ser = serial.Serial(
    port = 0,
    boundrate = 9600,
    bytesize = 8,
    parity = None,
    stopbits = 1,
    timeout = 0
    )
print ser.portstr




def callback(msg):
    byte data[8]
    data[0] = byte(0xAF)

rospy.init_node('subscriber')

sub = rospy.Subscriber('recognition',Int32,callback)

rospy.spin()


