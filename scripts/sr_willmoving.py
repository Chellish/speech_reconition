#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import serial
import numpy as np
from time import sleep
from std_msgs.msg import Int32
from struct import pack

setPower_com = [0xAF,0x03,0x02,0x01,0xB5]

whill_Power = False
setSpeed_com = []
setJoy_com = [0xAF,0x05,0x03,0x00,0,0,0]
ser = serial.Serial()
command = []
sJ_com_len = len(setJoy_com)

class send_command(object):
    def __init__(self):
        global ser,whill_Power,command,setJoy_com
        #シリアル通信の設定
        ser = serial.Serial("/dev/ttyACM2",
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_TWO)
        print ser.portstr
        #起動時にWhillの電源を入れる
        if whill_Power == False:
            for i in range(len(setPower_com)):
                com_data = chr(setPower_com[i])
                print(ord(com_data))
                ser.write(com_data)
        whill_Power = True
        print('\n')
        rospy.sleep(2)
        self.setJoy(0x80,0x80)
        command = setJoy_com
    
    def timer_callback(self,event):
        global ser,command
        send_command_ = command
        print('OK')
        for i in range(len(send_command_)):
            com_data = chr(send_command_[i])
            print(ord(com_data))
            ser.write(com_data) 
        print('\n') 

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
        global setJoy_com,command
        #停止
        if msg.data == 0:
            self.setJoy(0x80,0x80)
            command = setJoy_com
        #前進
        if msg.data == 1:
            self.setJoy( 0xB2,0x80)
        #後退
        if msg.data == 2:
            self.setJoy(0x4E,0x80)
        #右
        if msg.data == 3:
            self.setJoy(0x80,0x4E)
        #左
        if msg.data == 4:
            self.setJoy(0x80,0xB2)
        print msg.data
        command = setJoy_com
            
    def run(self):
        rospy.init_node('subscriber')
        rospy.Subscriber('recognition',Int32,self.com_sender)
        #ループ処理用コールバック関数
        rospy.Timer(rospy.Duration(0,200000),self.timer_callback)
        rospy.spin()

if __name__ == '__main__':
    try:
        node = send_command()
        node.run()       
        
    #エラー処理 何かあれば終了させる
    except rospy.ROSInterruptException:
        pass
