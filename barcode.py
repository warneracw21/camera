import sys
import os

import threading
import functools

def read_barcode(*args, **kwargs):
	""" Input: 	(barcode queue, barcode_lock)
		Output:	None
		Method:	Main Module Interface (open and close handler)
				Threading: Notify zip, post and clean of barcode
	"""

	barcode_queue = kwargs['barcode_queue']
	barcode_lock = kwargs['barcode_lock']

	barcode = ''
	while True:

		# Acquire Lock
		barcode_lock.acquire()
		print("Barcode Acquired Lock")

		# Add the new barcode to the Queue
		# Notify the file handlers that barcode is ready
		if barcode:
			print("Barcode Filling Buffer")
			barcode_queue.put(barcode)
			barcode_lock.notify()

		# Release the lock
		barcode_lock.release()
		print("Barcode Released Lock")

		# Now we scan again for barcode
		# Open and close handler on each scan
		handler = open('/dev/hidraw0', 'rb')

		# Remember WE GET STUCK HERE
		barcode = __get_barcode(handler)
		print("Scanning Barcode ... ", end=" ", flush=True)
		print("Success")
		handler.close()



hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

def __get_char(handler):
	""" Input:	file handle
		Output:	character from barcode scan iter
		Method:	Read in 8 bytes from Serial, reduce to nonzero entity in buffer
	"""

	char_buff = handler.read(8)
	char = functools.reduce(lambda a, b: a if a > 0 else b, char_buff)

	return char

def __get_barcode(handler):
	""" Input:	file handle
		Output:	barcode string
		Method:	iterate through characters in scan, stop at ord == 40
	"""

	barcode_chars = []
	char = __get_char(handler)
	while char != 40:
		if char:
			barcode_chars.append(hid[char])
		char = __get_char(handler)

	return ''.join(barcode_chars)










	


