#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from enum import Enum
import time
import os
from gpiozero import LED
from gpiozero import Button
from time import sleep
from threading import Timer
import pygame
from signal import pause
import subprocess
#IO configure




#timer configure
OPENNING_TIME_PERIOD=3
OPENED_TIME_PERIOD=8
CLOSING_TIME_PERIOD=3

#pygame.display.set_mode([300,300])


class State(Enum):
    IDLE=0,
    OPENNING=1,
    OPENED=2,
    CLOSING=3


class Event(Enum):
    EVENT_NONE=5,
    HAND_TRIGGER=0,
    OPENNING_TIMER_DONE=1,
    OPENED_TIMER_DONE=2,
    CLOSING_TIMER_DONE=3


class Rubbish(object):
    rubbish_count=0
    def __init__(self,id,name,hand_sensor_io,full_sensor_io,motor_ctrl_io):
        self.id=id
        self.name=name

        self.hand_sensor_ctrl=Button(pin=hand_sensor_io,pull_up=True,bounce_time=0.1)
        self.hand_sensor_ctrl.when_pressed=self.HandTriggerEvent

        self.full_sensor_ctrl=Button(full_sensor_io)
        self.motor_ctrl=LED(motor_ctrl_io)
        self.event=Event.EVENT_NONE
        self.state=State.IDLE
        #self.state=State.OPENNING

        self.OpenningTimer=Timer(OPENNING_TIME_PERIOD,self.OpenningTimerEvent)
        self.OpenedTimer=Timer(OPENED_TIME_PERIOD,self.OpenedTimerEvent)
        self.ClosingTimer=Timer(CLOSING_TIME_PERIOD,self.ClosingTimerEvent)

        #self.HandTriggerEvent()

        Rubbish.rubbish_count+=1

    def GetID(self):
        return self.id

    def GetName(self):
        return self.name
    
    def GateOpen(self):
        self.motor_ctrl.on()
    
    def GateClose(self):
        self.motor_ctrl.off()
    
    def RubbishStateProcess(self):
        pass
    
    def HandTriggerEvent(self):
        print('########################################################################################')
        print('########################################################################################')
        print('hand triggered##########################################################################')
        if((self.state==State.IDLE) or (self.state==State.CLOSING) ):
            self.state=State.OPENNING
            self.GateOpen()
            self.CapturePicture()
            self.PlayAudio_2()
            self.OpenningTimer.cancel()
            self.OpenningTimer=Timer(OPENNING_TIME_PERIOD,self.OpenningTimerEvent)
            self.OpenningTimer.start()
        else:
             print('hand trigered ,but it is the right time,ignored..')

    def Reset(self):
        print('something is wrong,the system is resetting...')
        self.state=State.IDLE
        self.OpenningTimer.cancel()
        self.OpenedTimer.cancel()
        self.ClosingTimer.cancel()

    def OpenningTimerEvent(self):
        print('openning timer done#####################################################################')
        self.OpenningTimer.cancel()
        if(self.state==State.OPENNING):
            self.state=State.OPENED
            self.OpenedTimer.cancel()
            self.OpenedTimer=Timer(OPENED_TIME_PERIOD,self.OpenedTimerEvent)
            self.OpenedTimer.start()
        else:
             self.Reset()

    def OpenedTimerEvent(self):
        print('opened timer done########################################################################')
        self.OpenedTimer.cancel()
        if(self.state==State.OPENED):
            self.state=State.CLOSING
            self.GateClose()
            self.ClosingTimer=Timer(CLOSING_TIME_PERIOD,self.ClosingTimerEvent)
            self.ClosingTimer.start()
        else:
             self.Reset()
    
    def ClosingTimerEvent(self):
        print('closing timer done,the gate has been closed go to idle state###################################3')
        self.ClosingTimer.cancel()
        if(self.state==State.CLOSING):
            self.state=State.IDLE
        elif(self.state==State.OPENNING):
            pass
        else:
            self.Reset()

    def PlayAudio(self):
        pygame.mixer.init()
       # pygame.display.set_mode([300,300])
        pygame.mixer.music.load('/home/pi/rubbish/rubbish_video.wav')
        print('audio start..................................................')
        pygame.mixer.music.play()
       
        #while 1:
        #    for event in pygame.event.get():
        #        if event.type==pygame.QUIT:
        #            sys.exit()

    def PlayAudio_1(self):
        return_code=subprocess.call("afplay","/home/pi/rubbish/rubbish_video.wav")
    def PlayAudio_2(self):
        result=os.system('mplayer /home/pi/rubbish/rubbish_video.mp3')
    def CapturePicture(self):
        os.environ['nowtime']=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        result=os.system('fswebcam --no-banner -r 640x480 -S 5  /home/pi/rubbish/picture/$nowtime.jpg')


####   (self,id,name,hand_sensor_io,full_sensor_io,motor_ctrl_io):
rubbish_chuyu=Rubbish(111,'chuyu',18,17,24)


pause()




""" while(1):
    val_push=os.system('ffmpeg -re -i "/Users/admin/Denny/learning/live_video/video_test.mp4" -vcodec libx264 -vprofile baseline -acodec aac   -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 rtmp://localhost:1935/ZedLive/test1')
    #al_pull=os.system('ffplay rtmp://localhost:1935/ZedLive/test1')
    print(val_push)
    #print(val_pull)
    time.sleep(15)
    count_num+=1
    if(count_num>3):
        break

 """


""" rubbish_1=Rubbish(1,'chuyu')
rubbish_2=Rubbish(2,'qita')
rubbish_3=Rubbish(3,'qita2')

print('the name of rubbish1 is',rubbish_1.GetName())
print('the name of rubbish2 is',rubbish_2.GetName())
print('totoal rubbishes number is ',Rubbish.rubbish_count)
 """


