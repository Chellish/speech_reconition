#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
#import serial
import numpy as np
from time import sleep
from std_msgs.msg import Int32
from struct import pack

whill_Power = False
setSpeed_com = []
setJoy_com = [0xAF,0x05,0x03,0x00,0,0,0]
#ser = serial.Serial()
sJ_com_len = len(setJoy_com)

class send_command(object):
    def __init__(self):
        global whill_Power
        #シリアル通信の設定
        #ser = serial.Serial("/dev/ttyACM1",
        #                    baudrate=9600,
        #                    parity=serial.PARITY_NONE,
        #                    bytesize=serial.EIGHTBITS,
        #                    stopbits=serial.STOPBITS_TWO)
        #print ser.portstr
        #起動時にWhillの電源を入れる
        if whill_Power == False:
        #    ser.write(setPower_com)
            setPower_com = pack('BBBBB',0xAF,0x03,0x02,0x01,0xB5)
            print(setPower_com)
            whill_Power = True       

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
        global setJoy_com
        #停止
        if msg.data == 0:
            self.setJoy(0x80,0x80)
            command = pack('B'*sJ_com_len,*setJoy_com)
        #前進
        if msg.data == 1:
            self.setJoy( 0xB2,0x80)
            command = pack('B'*sJ_com_len,*setJoy_com)
        #後退
        if msg.data == 2:
            self.setJoy(0x4E,0x80)
            command = pack('B'*sJ_com_len,*setJoy_com)
        #右
        if msg.data == 3:
            self.setJoy(0x80,0x4E)
            command = pack('B'*sJ_com_len,*setJoy_com)
        #左
        if msg.data == 4:
            self.setJoy(0x80,0xB2)
            command = pack('B'*sJ_com_len,*setJoy_com)
        #ser.write(command)
        print msg.data
        time=0
        while time > 11 :
            #ser.write(command)
            print(command)
            time += 1
            sleep(190)
            
    def run(self):
        rospy.init_node('subscriber')
        rospy.Subscriber('recognition',Int32,self.com_sender)
        rospy.spin()

if __name__ == '__main__':
    try:
        node = send_command()
        node.run()       
        
    #エラー処理 何かあれば終了させる
    except rospy.ROSInterruptException:
        pass
