#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import serial
import numpy as np

from std_msgs.msg import Int32
from struct import pack

com_Setpower = pack('5B',0xAF,0x03,0x02,0x01,0xB5)

flag = 0
setSpeed_com = []

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
    #電源ONのコマンドを送る
    def setPower(self):
        ser.write(com_Setpower)
        global flag
        flag += 1

    #Checksumの計算
    #今回はXORを用いる
    def checksum(self):
        global setSpeed_com
        csum = 0
        for i in range(len(setSpeed_com)):
            csum = csum ^ setSpeed_com[i]
        temp = csum
        if (temp ^ csum) == 0:
            setSpeed_com += [csum]
            return True
        else:  
            print ("Error CheckSum!!")
            return False

    
    #速度制御に関するコマンド
    def setSpeed(self,FM1,FA1,FD1,RM1,RA1,RD1,TM1,TA1,TD1):
        global setSpeed_com
        setSpeed_com += [0xAF,0x0C,0x04,FM1,FA1,FD1,RM1,RA1,RD1,TM1,TA1,TD1]


    def run(self,msg):
        rospy.init_node('subscriber')
        if flag == 0:
            self.setPower()
        if msg.data == 0:
            setSpeed_com(
                F_M1=0x08,
                F_A1=0x01,
                F_D1=0x01,
                R_M1=0x08,
                R_A1=0x01,
                R_D1=0x01,
                T_M1=0x08,
                T_A1=0x01,
                T_D1=0x01)
            command = pack("{0:d}B",*setSpeed_com)
            check_sum = self.checksum()
            if check_sum == True:
                ser.write(command)

        if msg.data == 1:
            setSpeed_com(
                F_M1=0x1E,
                F_A1=0x0A,
                F_D1=0x01,
                R_M1=0x08,
                R_A1=0x01,
                R_D1=0x01,
                T_M1=0x08,
                T_A1=0x01,
                T_D1=0x01)
            command = pack("{0:d}B",*setSpeed_com)
            check_sum = self.checksum()
            if check_sum == True:
                ser.write(command)
        rospy.spin()

if __name__ == '__main__':
    try:
        node = send_command()
        sub = rospy.Subscriber('recognition',Int32,node.run)
        
    #エラー処理 何かあれば終了させる
    except rospy.ROSInterruptException:
        pass
