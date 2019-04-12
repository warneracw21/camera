from __future__ import print_function

import os
import sys

from picamera import PiCamera
from zipfile import ZipFile
from send_package import send_zip
import RPi.GPIO as GPIO

import time
import math
import glob

import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()

fall = math.inf
def take_picture(channel):

	global fall, image_num

	if not(GPIO.input(channel)):
		fall = time.time()

	else:
		if(math.fabs(time.time() - fall) > 1.0):
			print("Zipping File ...", end=" ", flush=True)
			files = list(glob.glob(os.path.join(config.ROOT, '*')))
			if files:
				with ZipFile(config.ZIP_NAME, 'w') as zp:
					for f in files:
						zp.write(os.path.relpath(f))
			print("Success")
			print("Sending Zip ...", end=" ", flush=True)
			response = send_zip()
			if response.ok:
				print("Success")
				for f in files:
					os.remove(f)
				os.remove(os.path.join(os.getcwd(), config.ZIP_NAME))
			else:
				print(response)


		else:
			
			image_path = os.path.join(config.ROOT, 'pic_%d.jpg' % image_num)
			print("Taking Photo ... ", end=" ", flush=True)
			time.sleep(3)
			camera.capture(image_path)
			print("Success [%s]" % image_path)
			image_num += 1


	
# Define Callback lambda and assign event handler
GPIO.add_event_detect(config.CHANNEL, 
					  GPIO.RISING, 
					  callback=take_picture, 
					  bouncetime=100)

image_num = 0
while True:

	GPIO.event_detected(config.CHANNEL)


