# Led
### Start
1. pixels appears one after each other
2. same, but from bottom to top
3. same, but from center to exterior

### Speeding
1. pixels move from bottom to exterior
  * the pixels move regarding the speed, if the shuttle is fast the pixels move fast and so on

### Stop
1. pixels falls

### Detection
1. eyes are rolling on the screen, looking left and right, sometimes they blink
  * they have 3 different "focus" position, standard to frowned, they change regarding the number of "problematic" entities next to the shuttle
  * the background change regarding the pedestrian next to the shuttle


# Audio
Audio is more problematic, it should not become a pollution, this is why I choose to use it only when the shuttle is starting and for pedestrian awareness

### Start
* booting sound (computer) http://www.winhistory.de/more/winstart/winstart.htm.en
* car starter https://www.freesoundeffects.com/free-track/carstartgarage-466329/
* train-tramway-boat whistle http://soundbible.com/1455-Train-Horn-Low.html

### Detection
* bepping soud, when something is detected, the number of beeping increase with the number of things detected
* 4 speakers to be able to direct the sound and avoid pollution


# TODO
* power ? https://www.amazon.com/ENERGIZER-Inverter-converts-battery-compatible/dp/B00APL77NW
* link between rpi and laptop => try with raspberry pi zero and use it as usb gadget maybe or share connection via rj45


# POWER

### Watts ?
* leds: 60A*5V = 300W
* rpi: 2.5A*5V = 12.5W
* kinect: 2.7A*12V x2 = 65W
* laptop: 70W
* total:  447.5

# Mount

* bache => landi 19.-
* bache opaque ?
