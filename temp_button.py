#!/usr/bin/python
########################################################################
# Author:  J.R. Lorence <jrlorence@users.noreply.github.com>           #
# Created: 12/11/2016                                                  #
# Purpose: Collects the temperature every x minutes, reports it to     #
#          statsd, and gives the user a button to mark when they       #
#          feel cold.                                                  #
########################################################################

########################################################################
#                        REQUIRED MODULES                              #
########################################################################
import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep

########################################################################
#                          USER SETTINGS                               #
########################################################################

# DHT Model number, used by Adafruit_DHT
# Options:
#   * 11 = DHT11
#   * 22 = DHT22
#   * 2302 = AM2302
model_number = 11

########################################################################
#                     GLOBAL STATIC VARIABLES                          #
########################################################################

# States for easy pin/LED output control
ON = 1
OFF = 0

# Location of various hardware pieces
BUTTON_PIN = 19
LED_PIN = 18
SENSOR_PIN = 6

########################################################################
#                         MAIN DRIVER                                  #
########################################################################


def main():
    """Start a loop, waiting for user input or time-based triggers.

    Temperature reporting conditions:
        * Users can trigger temp reporting via button
        * A time-based trigger will report temp every X seconds
    """
    # Setup board inputs, outputs, pins, etc
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, OFF)

    # Setup the button-press interrupt
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=callback_button, bouncetime=300)

    # Wait for user button press input
    print "Started monitoring. Waiting for button or time trigger..."
    try:
        while True:
            sleep(10)
            print "Triggering auto-report..."
            get_temperature_stats()
    finally:
        GPIO.cleanup()

########################################################################
#                         HELPER FUNCTIONS                             #
########################################################################


def callback_button(channel):
    print "Button press detected"
    do_something()


def do_something():
    # Flash LED to ack user input
    print "Doing something..."
    flash_led()

    # Do the meat of the work
    toggle_led(ON)
    get_temperature_stats()

    # Flash LED to ack input is complete
    print "Did something"
    flash_led()
    toggle_led(OFF)


def get_temperature_stats():
    # 11 for the model DHT11 
    humidity, temperature = Adafruit_DHT.read_retry(model_number, SENSOR_PIN)
    if humidity and temperature:
        # convert C to F
        temperature = (temperature * 9/5.0) + 32
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')


def toggle_led(state):
    GPIO.output(LED_PIN, state)


def flash_led(num_flashes=2, delay=0.07):
    toggle_led(OFF)
    while num_flashes > 0:
        toggle_led(ON)
        sleep(delay)
        toggle_led(OFF)
        sleep(delay)
        num_flashes -= 1
    toggle_led(OFF)

########################################################################
#                         DEFAULT TO MAIN                              #
########################################################################


if __name__ == "__main__":
    main()
