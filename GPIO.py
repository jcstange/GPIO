#!/usr/bin/python

from gpiozero import LED
from time import sleep 
from os import system
from subprocess import check_output
from datetime import datetime, timedelta
import time
import threading
from sys import argv

try:
    url=argv[1]
except:
    url="https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_700KB.mp3" 

def current_time():
    return int(round(time.time() * 1000))

def volume_up():
    system(f'amixer set PCM 100%+')

def volume_down():
    system(f'amixer set PCM 100%-')

def sound_thread():
    print("Music started")
    system(f'ffplay {url} -nodisp -hide_banner -loglevel panic -autoexit')
    print("Music ended")

def light_thread(duration):
    startTime = current_time()
    print('Light started')
    
    while current_time() - startTime < duration:
        to_end = duration - (current_time() - startTime)
        print(f'Ending in: {to_end}')
        led.on()
        print("Light is ON")
        sleep(0.5)
        led.off()
        print("Light is OFF")
        sleep(0.5)

    print("Light ended")

def airconditioning_thread(duration):
    startTime = current_time()
    print('Fan started')
    fan.on()
    while current_time() - startTime < duration:
        fan.off()
    
    print('Fan stopped') 
    
def volume_thread(duration):
    startTime = current_time()
    print('Volume started') 
    volume = 50
    raising = True
    lastChange = current_time()
    while current_time() - startTime < duration:
        if current_time() - lastChange > 3000:
            lastChange = current_time()
            print(f'Volume: {volume}')
            if raising:
                if volume < 100:
                    volume_up()
                    volume = volume + 10
                else:
                    raising = False 
            else:
                if volume > 50:
                    volume_down()
                    volume = volume - 10
                else:
                    raising = True

    print(f'Volume Stopped')


def getDuration():
    timeString = check_output(f'ffmpeg -i {url} 2>&1 | grep -o -P \"(?<=Duration: ).*?(?=,)\"', shell=True, text=True)
    timeDateTime = datetime.strptime(timeString.replace("\r","").replace("\n",""), "%H:%M:%S.%f")
    delta = timedelta(hours=timeDateTime.hour, minutes=timeDateTime.minute, seconds=timeDateTime.second, microseconds=timeDateTime.microsecond)
    millis = (delta.days * 3600 * 1000 / 24) + (delta.seconds * 1000) + (delta.microseconds/1000)
    print(millis)
    return millis

    

led = LED(17)
fan = LED(23)
z = threading.Thread(target=airconditioning_thread,args=(getDuration(),))
y = threading.Thread(target=light_thread,args=(getDuration(),))
x = threading.Thread(target=sound_thread)
m = threading.Thread(target=volume_thread,args=(getDuration(),))
z.start()
y.start()
x.start()
m.start()
