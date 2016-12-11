#!/usr/bin/python
############################################################
# Author:  J.R. Lorence <jrlorence@users.noreply.github.com>
# Created: 12/11/2016
# Purpose: Collects the temperature every x minutes, 
#          reports it to statsd, and gives the user a 
#          button to mark when they feel cold
############################################################

# Required python modules
import RPi.GPIO as GPIO
from time import sleep

# Global static variables
ON = 1
OFF = 0
BUTTON_PIN = 19
LED_PIN = 18


def main():
	# Setup board inputs, outputs, pins, etc
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(LED_PIN,GPIO.OUT)
	GPIO.output(LED_PIN,0)

	# Setup the button-press interrupt 
	GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=callback_button, bouncetime=300)

	# Wait for user button press input
	print "Waiting for button press..."
	try:
		while True:
			sleep(10)
			print "Still waiting for button presses..."
	finally:
		GPIO.cleanup()

def callback_button(channel):
	print "Button press detected"
	do_something()

def do_something():

	# Flash LED to ack user input
	print "Doing something..."
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
