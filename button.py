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

	# Referencing Global Variable (shared across threads)
	global image_num
	image_num += 1

	# Build Image Write Path
	image_name = os.path.join(config.ROOT, 'pic_%d.jpg' % image_num)

	# Set Lighting (takes 3 seconds)
	time.sleep(3)
	camera.capture(image_name)
	print("Image Taken:", image_name)

# Define Callback lambda and assign event handler
callback = lambda x: take_picture()
GPIO.add_event_detect(config.CHANNEL, 
					  GPIO.RISING, 
					  callback=callback, 
					  bouncetime=200)

image_num = 0
while True:
	GPIO.event_detected(config.CHANNEL)

