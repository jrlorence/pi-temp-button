#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

in_pin = 19
out_pin = 18

GPIO.setup(in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(out_pin,GPIO.OUT)
GPIO.output(out_pin,0)

try:
	last_state = 0
	while True:
		# save time, output gets the input
		button_pressed = GPIO.input(in_pin)
		if button_pressed:
			GPIO.output(out_pin,GPIO.HIGH)
		else:
			GPIO.output(out_pin,GPIO.LOW)

		# smooth button debounce and long presses
		if button_pressed and not last_state:
			print "State switched"
			# deal with button debounch
			sleep(0.3)

		last_state = button_pressed
		#sleep(0.1)

finally:
	GPIO.cleanup()
