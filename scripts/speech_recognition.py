#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import re
from time import sleep
from std_msgs.msg import Int32
from rospeex_if import ROSpeexInterface

class recognition(object):

    def __init__(self):
        self._interface = ROSpeexInterface()

    def sr_response(self,message):
        #文字列検索
        #止まる
        stop = re.compile('(?P<stop>止ま|ストップ)').search(message)
        #前に関するもの
        front = re.compile('(?P<front>前|進め)').search(message)
        #後ろに関するもの
        back = re.compile('(?P<back>後|下が|バック)').search(message)
        #右に関するもの
        right = re.compile('(?P<right>右)').search(message)
        #左に関するもの
        left = re.compile('(?P<left>左)').search(message)
        #認識した音声を出力
        print 'rospeex replay : %s' % message 
       
        #検索した文字列に対して以下の数字を配信する
        #検索した文字列が何も一致しなかったら配信しない。
        if stop is not None:
            pub.publish(0)
        elif front is not None:
            pub.publish(1) 
        elif back is not None:
            pub.publish(2)  
        elif right is not None:
           pub.publish(3)   
        elif left is not None:
            pub.publish(4) 
        sleep(2)        

    def run(self):
        """ run ros node """
        #初期化
        rospy.init_node('speech_recognition')
        self._interface.init()
        #音声認識エンジンの設定(言語,エンジン)
        self._interface.set_spi_config(language='ja', engine='nict')  
        #音声認識結果取得用コールバック関数
        self._interface.register_sr_response(self.sr_response)
        rospy.spin()

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('recognition',Int32,queue_size=10)
        node = recognition()
        node.run()
        
    #エラー処理 何かあれば終了させる
    except rospy.ROSInterruptException:
        pass

