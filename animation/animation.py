import random,pygame,socket,pickle,time,sys
from PIL import Image

class Animation:
    output = []
    foreground = (255,255,255)
    def __init__(self, pixels, height, width):

        pygame.init()
        self.colors = []
        self.pixels = pixels
        self.height = height
        self.width = width


        #hard = Client_renderer(host,port)
        self.clock = pygame.time.Clock()

    @classmethod
    def add_renderer(self,r):
        self.output.append(r)

    def to_xy(self, i):
        x,y =i%self.width,int(i/self.width)
        return((x,y))

    def to_i(self, x,y):
        return x%self.width+y*self.width

    def render(self, kind):
        if kind == 1:
            for o in self.output:
                o.draw(self.pixels)
        if kind == 2:
            print('asymetrical')
        self.clock.tick(4)

    def stop(self):
        return self.pixels

class Start(Animation):
    def __init__(self, max_p):
        super().__init__( [], 10, 45)
        self.max_p = max_p
        self.g = 255

    def update(self):
        if len(self.pixels) < self.max_p:
            b = (int(self.width/self.max_p*len(self.pixels)))
            p = random.randint(0,9)*self.width+b

            self.pixels.append((p,(0,self.g,0)))

            if self.g > 50:
                self.g-=1
        super().render(1)

class Start2(Animation):
    def __init__(self, max_p):
        super().__init__( [], 10, 45)
        self.max_p = max_p
        self.blink = 10
        self.test = self.blink

    def update(self):

        if self.test >= 0 :
            self.test-=1
            self.pixels = []


        elif self.blink >= 0:
            self.blink-=1
            self.test=self.blink
            for _ in range(self.width*self.height):
                p = random.randint(0,self.width*self.height)
                self.pixels.append((p,self.foreground))
            print(self.test)

        super().render(1)


class Speed(Animation):
    def __init__(self, pixels, max_p):
        super().__init__(pixels,10,45)
        self.max_p = max_p

    def update(self):
        if len(self.pixels) < self.max_p:
            p = random.randint(1,10)*45 - 1
            self.pixels.append((p,self.foreground))

        new_pixels = []
        for p,c in self.pixels:
            x,y =(p%self.width),int(p/self.width)
            max = int((x*5)/44)
            min = int((x*3)/44)
            val = random.randint(min,max)
            x = x+(1+val)
            if x > 44:
                x = 0
                y = random.randint(0,9)

            new_pixels.append((x%self.width+y*self.width,c))

        self.pixels = new_pixels
        super().render(1)

class Speed2(Animation):
    def __init__(self):
        super().__init__([],10,45)
        self.top_left = 0
        self.dir = 1
        self.arrow_d = -1


    def update(self):
        p = self.top_left
        self.pixels = []
        for y in range(self.height):
            for x in range(p%5, self.width, 5 ):
                print(x,y)
                self.pixels.append((self.to_i(x,y), self.foreground))
            if y < self.height/2-1:
                p += self.dir
            elif y > self.height/2-1:
                p -= self.dir

        self.top_left += self.arrow_d
        super().render(1)


class Speed3(Animation):
    def __init__(self):
        super().__init__([],10,45)
        self.speed = 0
        self.inc = 1

    def get_color(self):
        return (self.speed , 255 - self.speed, 0)

    def update(self):
        self.pixels = []
        if self.speed < 0 or self.speed > 255:
            self.inc*=-1
            self.speed += 10*self.inc

        print(self.speed)
        for x in range(int(self.speed/255*self.width)):
            for y in range(self.height):
                self.pixels.append((self.to_i(x,y),self.get_color()))
        super().render(1)
        self.speed += 10*self.inc

class Status(Animation):
    def __init__(self):
        super().__init__([],10,45)
        self.intensity = 1
        self.inc = 1

    def update(self):
        color  =(self.intensity, self.intensity, self.intensity)
        self.pixels = [(i, color) for i in range(0,self.width*self.height,2)]

        if self.inc == 1:
            self.intensity *= 3
        else:
            self.intensity  = int(self.intensity/3)

        if self.intensity > 255:
            self.inc *= -1
            self.intensity = 255
        elif self.intensity < 1:
            self.inc *= -1
            self.intensity = 1
        super().render(1)

class Status2(Animation):
    def __init__(self):
        super().__init__([],10,45)



class Static(Animation):
    def __init__(self, img, scroll = False):
        super().__init__([],10,45)
        im = Image.open(img)
        pix = list(im.getdata())
        self.pixels = [(i,self.foreground) for i, x in enumerate(pix) if x == (255,255,255)]
        self.scroll = scroll


    def update(self):
        if self.scroll:
            new_pixels = []
            for p,c in self.pixels:
                    x,y =p%self.width + 1,int(p/self.width)
                    if y >= self.width:
                        y = 0
                    new_pixels.append((x%self.width+y*self.width, self.foreground))
            self.pixels = new_pixels
        super().render(1)






class Pixel_renderer:
    e = 10
    width = 45
    height = 10

    background = (0,0,0)
    foreground = (255,255,255)


    def __init__(self):

        self.screen = pygame.display.set_mode(((2*self.width+10)*self.e,self.height*self.e))

    def draw(self, pixels):
        self.screen.fill(self.background)
        pygame.draw.rect(self.screen,(40,40,40),(450,0,100,100))
        for p,c in pixels:
            x,y =(p%self.width*self.e),int(p/self.width)*self.e
            pygame.draw.rect(self.screen, c,(550 + x,y,self.e,self.e))
            pygame.draw.rect(self.screen, c,(440 - x,y,self.e,self.e))
        pygame.display.flip()


class Client_renderer():
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.fail = 0
        self.socket.settimeout(2)
        self.connect()

    def connect(self):
        if self.fail < 3:
            try:
                print('trying to connect')
                self.socket.connect((self.host, self.port))
                print("Connection on {}".format(port))
                self.fail = 0
            except:
                print('connection impossible')
                self.fail+=1
                self.connect()



    def draw(self, pixels):
        data = pickle.dumps(pixels, protocol=2)
        try:
            self.socket.send(data)
        except:
            print('connection lost try to reconnect')
            self.connect()



class Animation_controller():

    def __init__(self):
        self.animations = dict()

    def add_anim(self, key,a):
        self.animations[key] = a

    def run(self):
        anim = None
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    else:
                        try:
                            anim = self.animations[chr(event.key)]
                        except:
                            print('key is not bind to anything')
            if anim:
                anim.update()

    def test(self):
        for k, v in self.animations.items():
            print(k,v)

Animation.add_renderer(Pixel_renderer())
host = "10.42.0.27"
port = 15555
#Animation.add_renderer(Client_renderer(host,port))

print()
ac = Animation_controller()
ac.add_anim('r', Static('apero.png',scroll=True))
ac.add_anim('v', Speed3())
ac.add_anim('s', Status())

test = Speed2()
print(test.to_i(44,3))
print(test.to_xy(179))

ac.run()
