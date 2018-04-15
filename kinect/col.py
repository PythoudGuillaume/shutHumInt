# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

import argparse
import signal
import sys

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', type=int, default=150, help='nubmer of led')
	parser.add_argument('-c', type=str, default="0, 0, 0", help='color given in the form \"r, g, b\"')
        args = parser.parse_args()
        rgb = args.c.split(',')
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        return (args.n,(r,g,b))
        
#LED strip configuration:
#LED_COUNT      = n      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_ROW        = 6
LED_COLUMN     = 5

#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


# Main program logic follows:
if __name__ == '__main__':
    (LED_COUNT,(r,g,b)) = opt_parse()
    print(r)
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()	
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r,g,b))
    strip.show()
    print ( 'led off' )

