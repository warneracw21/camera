from __future__ import print_function

import os
import sys

import RPi.GPIO as GPIO
import numpy as np
import functools
import hashlib
import glob
import shutil

import picamera.array
import picamera

import math
import time
import cv2

import config

IMAGE_NUM = 0
BOUNCE_ERR = False
def button(channel):
    """ Input:  GPIO Channel
        Output: None
        Global Variables:   BOUNCE_ERR, IMAGE_NUM
        Method: Instantiate image capture and sleep methodology
                Globally monitor for Bouncing Error
    """

    global BOUNCE_ERR, IMAGE_NUM

    if not(BOUNCE_ERR):
        image_path = os.path.join(config.ROOT, 'photos/img_%d.jpg' % IMAGE_NUM)
        __capture(image_path)
        IMAGE_NUM += 1
        BOUNCE_ERR = True
    else:
        time.sleep(2)
        BOUNCE_ERR = False

def __capture(path):
    """ Input:  Image Path
        Output: None
        Method: Take photo with PiCamera, assign to correct path
    """

    print("Taking Photo ... ", end=" ", flush=True)
    time.sleep(config.SLEEP_TIME)
    camera.capture(path)
    real_name = os.path.basename(os.path.normpath(path))
    print("Success [%s]" % real_name)
    

# Initialize Camera Thread
print("Initializing Camera Thread ... ", end=" ", flush=True)
camera = picamera.PiCamera()
camera.resolution = (640, 480)
print("Success\n")

print("Initializing GPIO Thread ... ", end=" ", flush=True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(config.CHANNEL, 
                    GPIO.BOTH, 
                    bouncetime=config.CLICK_LATENCY)

# Set up Partial Function for interfacing unique camera
GPIO.add_event_callback(config.CHANNEL, callback=button)
print("Success\n")



if __name__ == '__main__':
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("\nClosing GPIO Connections")
        GPIO.cleanup()

        print("Closing Camera")
        cam.close()

        clean()