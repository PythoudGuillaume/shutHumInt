import socket,pickle
from neopixel import *

# LED strip configuration:
LED_COUNT      = 900      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_ROW        = 10
LED_COLUMN     = 90

#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

white = Color(255,255,255)
black = Color(0,0,0)


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))

socket.listen(5)
client, address = socket.accept()
print("{} connected".format( address ))
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
## Intialize the library (must be called once before other functions).
strip.begin()

def to_dis(n):
    step = int(n/45)
    print(step)
    print(step%2)
    if step%2 == 1:

        return ((step*45-1)+(45-n%45))
    else :
        return n

while True:

        try:
            response = pickle.loads(client.recv(255))
        except:
            print("something weird happens")
        if response != "":
                    #print(response)
                    for i in range(strip.numPixels()):
                        strip.setPixelColor(i,black)

                    for p in response:
                        new_p = to_dis(p)
                        strip.setPixelColor(new_p,white)
                        strip.setPixelColor(450+new_p,white)
                    strip.show()





for i in range(strip.numPixels()):
    strip.setPixelColor(i,black)
strip.show()
print("Close")
client.close()
