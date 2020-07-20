#!/usr/bin/python




import os
import time


print('system starts')

nowtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

os.environ['nowtime']=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))


result=os.system('fswebcam --no-banner -r 640x480  /home/pi/rubbish/picture/$nowtime.jpg')

print(result)
