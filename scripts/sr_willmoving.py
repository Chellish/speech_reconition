#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import serial
import numpy as np
from time import sleep
from std_msgs.msg import Int32
from struct import pack

setPower_com = pack('5B',0xAF,0x03,0x02,0x01,0xB5)

whill_Power = False
setSpeed_com = []
setJoy_com = [0xAF,0x05,0x03,0x00,0,0,0]
ser = serial.Serial()
command = []

class send_command(object):
    def __init__(self):
        global ser,whill_Power
        #起動時にWhillの電源を入れる
        if whill_Power == False:
            ser.write(setPower_com)
            whill_Power = True
        #シリアル通信の設定
        ser = serial.Serial("/dev/ttyACM0",
                            baudrate=38400,
                            parity=serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_TWO)
        print ser.portstr
    
    def timer_callback(self,event):
        global command
        ser.write(command)  

    #Checksumの計算
    #今回はXORを用いる
    def checksum(self,buf):
        csum = 0
        for i in range(len(buf)-1):
            csum = csum ^buf[i]
        temp = csum
        if (temp ^ csum) == 0:
            return csum
        else:  
            print ("Error CheckSum!!")
            return 
  
    #速度制御に関するコマンド
    #def setSpeed(self,FM1,FA1,FD1,RM1,RA1,RD1,TM1,TA1,TD1):
    #    global setSpeed_com
    #    setSpeed_com += [0xAF,0x0C,0x04,FM1,FA1,FD1,RM1,RA1,RD1,TM1,TA1,TD1]

    def setJoy(self,fb_para,lr_para):
        global setJoy_com
        setJoy_com[4] = fb_para
        setJoy_com[5] = lr_para       
        setJoy_com[6] = self.checksum(setJoy_com)

    def com_sender(self,msg):
        global ser,setJoy_com,command
        #停止
        if msg.data == 0:
            self.setJoy(0x80,0x80)
            command = pack("{0:d}B",*setJoy_com)
        #前進
        if msg.data == 1:
            self.setJoy( 0xB2,0x80)
            command = pack("{0:d}B",*setJoy_com)
        #後退
        if msg.data == 2:
            self.setJoy(0x4E,0x80)
            command = pack("{0:d}B",*setJoy_com)
        #右
        if msg.data == 3:
            self.setJoy(0x80,0x4E)
            command = pack("{0:d}B",*setJoy_com)
        #左
        if msg.data == 4:
            self.setJoy(0x80,0xB2)
            command = pack("{0:d}B",*setJoy_com)
        print msg.data
            
    def run(self):
        rospy.init_node('subscriber')
        rospy.Subscriber('recognition',Int32,self.com_sender)
        #ループ処理用コールバック関数
        rospy.Timer(rospy.Duration(200),self.timer_callback)
        rospy.spin()

if __name__ == '__main__':
    try:
        node = send_command()
        node.run()       
        
    #エラー処理 何かあれば終了させる
    except rospy.ROSInterruptException:
        pass
