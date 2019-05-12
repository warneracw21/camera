
# Import Operating System
import sys
import os

# Import Modules
import RPi.GPIO as GPIO
import threading
import queue
import functools
import picamera
import time

# Import Threaded Methods
from file_handler import zip_post_and_clean
from camera import button
from barcode import read_barcode

# Import Constants and Globals
import config

if __name__ == '__main__':

	# Create Barcode Lock and Queue
	barcode_queue = queue.Queue()
	barcode_lock = threading.Condition()

	# Create and Run Barcode Thread
	print("Initializing Barcode Scanner Thread ... ", end=" ", flush=True)
	barcode_thread = threading.Thread(target=read_barcode, 
									 	kwargs={
									  		'barcode_queue': barcode_queue, 
									  		'barcode_lock': barcode_lock
									  	})
	print("Success\n")

	print("Initializing Zip, Post, and Clean Thread ...", end=" ", flush=True)
	zip_post_and_clean_thread = threading.Thread(target=zip_post_and_clean, 
										kwargs={
									  		'barcode_queue': barcode_queue, 
									  		'barcode_lock': barcode_lock
									  	})
	print("Success")

	# Run the threads
	barcode_thread.start()
	zip_post_and_clean_thread.start()



	while True:
		pass

