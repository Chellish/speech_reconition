#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import serial
import numpy as np

from std_msgs.msg import Int32
from struct import pack

setPower_com = pack('5B',0xAF,0x03,0x02,0x01,0xB5)

flag = 0
setSpeed_com = []
setJoy_com = [0xAF,0x05,0x03,0x00,0,0,0]

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


class send_command(object):
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

    def run(self,msg):
        rospy.init_node('subscriber')
        #flagが0なら電源ONのコマンドを送る
        if flag == 0:
            global flag
            flag += 1
            command = setPower_com
        #停止
        if msg.data == 0:
            #joy_paramater: fb is max 0x64, min  
            self.setJoy(0x00,0x00)
            command = pack("{0:d}B",*setJoy_com)
        #前進
        if msg.data == 1:
            self.setJoy( 0x32,0x00)
            command = pack("{0:d}B",*setJoy_com)
        #後退
        if msg.data == 2:
            #パラメーターの負の値ってどうすんだろ？？
            self.setJoy(0x00,0x00)
            command = pack("{0:d}B",*setJoy_com)
        #右
        if msg.data == 3:
            self.setJoy(0x32,0x00)
            #パラメーターの負の値ってどうすんだろ？？
            command = pack("{0:d}B",*setJoy_com)
        #左
        if msg.data == 4:
            self.setJoy(0x00,0x32)
            command = pack("{0:d}B",*setJoy_com)
        ser.write(command)    
        rospy.spin()

if __name__ == '__main__':
    try:
        node = send_command()
        sub = rospy.Subscriber('recognition',Int32,node.run)
        
    #エラー処理 何かあれば終了させる
    except rospy.ROSInterruptException:
        pass
