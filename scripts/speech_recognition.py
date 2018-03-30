#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import re
from rospeex_if import ROSpeexInterface

class recognition(object):

    def __init__(self):
        self._interface = ROSpeexInterface()

    def sr_response(self,message):
        print 'rospeex replay : %s' % message


    def run(self):
        """ run ros node """
        rospy.init_node('speech_recognition')
        #初期化
        self._interface.init()
        #音声認識結果取得用コールバック関数
        self._interface.register_sr_response(self.sr_response)
        #音声認識エンジンの設定(言語,エンジン)
        self._interface.set_spi_config(language='ja', engine='nict')
        rospy.spin()

if __name__ == '__main__':
    try:
        node = recognition()
        node.run()
    except rospy.ROSInterruptException:
        pass

