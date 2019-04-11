from picamera import PiCamera
import RPi.GPIO as GPIO
import time

import os

from camera import take_picture
import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()

def take_picture():
	global i
	i += 1
	image_name = os.path.join(config.ROOT, 'pic_%d.jpg' % i)

	time.sleep(3)
	camera.capture(image_name)
	print("Image Taken:", image_name)


GPIO.add_event_detect(config.CHANNEL, GPIO.RISING, callback=lambda x: take_picture(), bouncetime=200)

i = 0
while True:
	GPIO.event_detected(config.CHANNEL)

