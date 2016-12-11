#!/usr/bin/python
###############################################
# Author: J.R. Lorence <jrlorence@gmail.com>
# Date:   12/11/2016
###############################################

# Required python modules
import RPi.GPIO as GPIO
from time import sleep

# Global static variables
ON = 1
OFF = 0
in_pin = 19
LED_PIN = 18


def main():
	# Setup board inputs, outputs, pins, etc
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(LED_PIN,GPIO.OUT)
	GPIO.output(LED_PIN,0)

	# Wait for user button press input
	try:
		last_state = 0
		while True:
			button_pressed = GPIO.input(in_pin)
	
			# smooth button debounce and long presses
			if button_pressed and not last_state:
				print "Button pressed"
				do_something()
				# deal with button debounce
				sleep(0.3)
	
			last_state = button_pressed

	finally:
		GPIO.cleanup()

def do_something():
	# Flash LED to ack user input
	flash_led()

	# Do the meat of the work
	toggle_led(ON)
	sleep(2)

	# Flash LED to ack input is complete
	flash_led()
	toggle_led(OFF)
	print "Did something"

def toggle_led(state):
	GPIO.output(LED_PIN,state)

def flash_led(num_flashes=2,delay=0.07):
	toggle_led(OFF)
	while (num_flashes > 0):
		toggle_led(ON)
		sleep(delay)
		toggle_led(OFF)
		sleep(delay)
		num_flashes -= 1
	toggle_led(OFF)

if __name__ == "__main__":
	main()
