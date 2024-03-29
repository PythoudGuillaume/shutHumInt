import socket
import time

from neopixel import *

import argparse
import signal
import sys
import pickle
# NeoPixel library strandtest example

# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_ROW        = 6
LED_COLUMN     = 5

#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


def boot(strip,color=Color(255,255,255), wait_ms=100):
	for i in range(LED_ROW,0,-1):
                for j in range(i,LED_COUNT+1, LED_ROW):
			strip.setPixelColor(j-1,color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def boot2(strip, color=Color(0,255,0),wait_ms=300):
	mirror = 1
	for i in range(LED_ROW/2,0,-1):
		for j in range(i, LED_COUNT+1, LED_ROW):
			strip.setPixelColor(j-1,color)
			strip.setPixelColor(j-1+mirror,color)
		strip.show()
		mirror+=2
		print(mirror)
		time.sleep(wait_ms/1000.0)

def speed(strip, color=Color(0,255,0), wait_ms=100):
	for i in range(LED_COLUMN):
		for j in range(LED_ROW):
			strip.setPixelColor(i*LED_ROW+j,color)
		strip.show()
		time.sleep(wait_ms/1000.0)


def react(strip, leds):
    for i, l in enumerate(leds):
        if l < 1000:
            c = Color(255,0,0)
        elif l < 1500:
            c = Color(255,255,0)
        else:
            c = Color(255,255,255)
        strip.setPixelColor(i,c)
    strip.show()

def react_b(strip, leds):
    for i, l in enumerate(leds):
        if l < 1500:
            strip.setPixelColor(i,Color(0,0,0))
    strip.show()
    time.sleep(0.1)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,Color(255,255,255))
    strip.show()

# Define functions which animate LEDs in various ways.

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))

socket.listen(5)
client, address = socket.accept()
print("{} connected".format( address ))
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

boot(strip)

while True:
        try:
            response = pickle.loads(client.recv(255))
        except:
            print("smthg wrong happen")
            colorWipe(strip, Color(0,0,0))
            break

        if response != "":
                    #print(response)
                    react(strip, response)



print("Close")
client.close()
