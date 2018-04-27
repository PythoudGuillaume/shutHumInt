import socket,pickle, random, random
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

def random_color():
    return Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

def server():
    blocksize = 16384
    sentinel = b'\x00\x00END_MESSAGE!\x00\x00'[:blocksize]

    serversocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversocket.bind(('', 8051))
    serversocket.listen(5)
    render = Pixel_renderer()
    while True:
        clientsocket, address = serversocket.accept()
        print("New client")

        while True:
            blocks = []
            while True:
                b = clientsocket.recv(blocksize)
                blocks.append(b)
                if blocks[-1] == sentinel:
                    blocks.pop()
                    break
            data = b''.join(blocks)
            list = pickle.loads(data)
            draw_pixels(list)





server()

for i in range(strip.numPixels()):
    strip.setPixelColor(i,black)
strip.show()
print("Close")
client.close()
