#!/usr/bin/env python
#coding:utf-8
#time: 2017/1/7 12:33
#import win32api,win32con
#win32api.MessageBox(0, "这是一个测试消息", "消息框标题",win32con.MBOK)
import time,winsound
def play():
    print("播放声音")
    winsound.PlaySound('ALARM8',winsound.SND_ASYNC)
    while(True):
      time.sleep(0.2)
      winsound.PlaySound('ALARM8',winsound.SND_ASYNC)
      print "s"
def mp3_play():
    import mp3play
    filename = r'C:\a.mp3'
    mp3 = mp3play.load(filename)
    mp3.play()
    import time
    time.sleep(min(30, mp3.seconds()))
    mp3.stop()
if __name__ == '__main__':
    # play()
    mp3_play()