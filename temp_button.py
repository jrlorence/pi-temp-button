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

# The amount of time in seconds to wait before auto-reporting temperature
reporting_interval = 10

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
            sleep(reporting_interval)
            print "Triggering auto-report..."
            get_temperature_stats()
    finally:
        GPIO.cleanup()

########################################################################
#                         HELPER FUNCTIONS                             #
########################################################################


def callback_button(channel):
    """Trigger on button press. Kick-off real work. """
    print "Button press detected"
    do_something()


def do_something():
    """TODO: Refactor function and add doc"""
    # Flash LED to ack user input
    print "Doing something..."
    flash_led()

    # Do the meat of the work
    set_led(ON)
    get_temperature_stats()

    # Flash LED to ack input is complete
    print "Did something"
    flash_led()
    set_led(OFF)


def get_temperature_stats():
    """TODO: Refactor function and add doc"""
    # Grab the temperature stats from the hardware device
    humidity, temperature = Adafruit_DHT.read_retry(model_number, SENSOR_PIN)
    if humidity and temperature:
        # convert C to F
        temperature = (temperature * 9/5.0) + 32
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')


def set_led(state=OFF):
    """Turn the LED ON or OFF.

    Params:
        state = ON or OFF (Default: OFF)
    """
    GPIO.output(LED_PIN, state)


def flash_led(num_flashes=2, delay=0.07):
    """Flash the LED.

    Used to acknowledged user action and report status, in lieu of an LCD.

    Params:
        num_flashes = Number of times to flash LED (Default: 2)
        delay = Delay (in sec) between each LED state toggle (Default: 0.07)

    """
    set_led(OFF)
    while num_flashes > 0:
        set_led(ON)
        sleep(delay)
        set_led(OFF)
        sleep(delay)
        num_flashes -= 1
    set_led(OFF)

########################################################################
#                         DEFAULT TO MAIN                              #
########################################################################


if __name__ == "__main__":
    # Trigger main() on launch to drive the program
    main()
