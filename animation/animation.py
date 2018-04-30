import random,pygame,socket,pickle,time,sys
import numpy as np
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
        self.type = 1

#        hard = Client_renderer(host,port)
        self.clock = pygame.time.Clock()

    @classmethod
    def add_renderer(cls, r):
        cls.output.append(r)

    def to_xy(self, i):
        x,y =i%self.width,int(i/self.width)
        return((x,y))

    def to_i(self, x,y):
        return x%self.width+y*self.width

    def render(self, kind):
        if kind == 1:
            for o in self.output:
                o.draw_mirror(self.pixels)
        if kind == 2:
            print('asymetrical')
            for o in self.output:
                o.draw_asym(self.pixels)
        self.clock.tick(10)

    def set(self, pixels, type):
        pass

    def stop(self):
        self.pixels = []


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

    def stop(self):
        self.g = 255
        super().stop()

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
        self.dir = -1
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
            self.intensity = int(self.intensity/3)

        if self.intensity > 255:
            self.inc *= -1
            self.intensity = 255
        elif self.intensity < 1:
            self.inc *= -1
            self.intensity = 1
        super().render(1)


class Status2(Animation):
    def __init__(self,img):
        super().__init__([],10,45)

        im = Image.open(img)
        self.im2arr = np.array(im)
        self.n = 0
        self.inc = 1
        self.type = 2
        self.blink = 0
        self.blink_inc = 1
        self.state = 1
        self.pup = 0

    def update(self):
        if self.n< -2 or self.n > 2:

            self.inc *= -1
            self.n += self.inc

        self.pixels = [[] for i in range(2)]

        i = random.randint(0,6)

        if i > 5 and self.blink == 0:
            self.blink = 1


        if self.blink == 1:
            print('blink')
            self.eye_blink()

        for iy,y in enumerate(self.im2arr):
            for ix,pix in enumerate(y):
                # print(ix,' : ',iy,' => ',pix)
                if pix.tolist() == [255,255,255]:
                    self.pixels[1].append((self.to_i(ix+5+self.n, iy),self.foreground))
                    self.pixels[0].append((self.to_i(ix+5-self.n, iy),self.foreground))

        self.n+=self.inc

        super().render(2)

    def eye_blink(self):

        if self.state == 0:
            self.blink = 0
            self.blink_inc = 1
            self.state = 1
            self.n = self.pup
            return

        self.pup = self.n
        self.n = 0

        self.im2arr = np.array(Image.open("eyes"+str(self.state)+".png"))
        self.state += self.blink_inc
        if self.state == 5:
            self.state = 4
            self.blink_inc = -1


class Stop(Animation):
    def __init__(self):
        super().__init__([],10,45)

    def set(self,pixels, type):
        self.pixels = pixels
        self.type = type

    def update(self):
        new_p = []

        if self.type == 2:
            for l in self.pixels:
                new_p.append(self.drop_pix(l))
        elif self.type == 1:
            new_p = self.drop_pix(self.pixels)

        self.pixels = new_p
        super().render(self.type)

    def drop_pix(self, pixels):
        new_p = []

        if pixels:
            for p,c in pixels:
                x,y = self.to_xy(p)
                y+=1
                if y < self.height:
                    new_p.append((self.to_i(x,y),c))

        return new_p


class Close_vert(Stop):
    def __init__(self):
        super().__init__()

    def drop_pix(self, pixels):
        new_p = []

        if pixels:
            for p, c in pixels:
                x,y = self.to_xy(p)
                if y < 4:
                    y+= 1
                elif y > 5:
                    y-= 1
                else:
                    continue

                new_p.append((self.to_i(x,y),c))

        return new_p


class Close_horiz(Stop):
    def __init__(self):
        super().__init__()

    def drop_pix(self, pixels):
        new_p = []

        if pixels:
            for p, c in pixels:
                x,y = self.to_xy(p)
                if x < 23:
                    x+= 1
                elif x > 24:
                    x-= 1
                else:
                    continue

                new_p.append((self.to_i(x,y),c))

        return new_p


class CloseFade(Stop):
    def __init__(self):
        super().__init__()

    def drop_pix(self, pixels):
        new_p = []

        if pixels:
            for p, c in pixels:
                r,g,b = c
                col = (self.to_zero(r),self.to_zero(g),self.to_zero(b))
                new_p.append((p,col))

        return new_p

    @staticmethod
    def to_zero(r):
        new_r = r- 10
        if new_r > 0:
            return new_r
        else:
            return 0


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

    def draw_mirror(self, pixels):
        self.screen.fill(self.background)
        pygame.draw.rect(self.screen,(40,40,40),(450,0,100,100))
        for p,c in pixels:
            x,y =(p%self.width*self.e),int(p/self.width)*self.e
            pygame.draw.rect(self.screen, c,(550 + x,y,self.e,self.e))
            pygame.draw.rect(self.screen, c,(440 - x,y,self.e,self.e))

        pygame.display.flip()

    def draw_asym(self,pixels):
        self.screen.fill(self.background)
        pygame.draw.rect(self.screen,(40,40,40),(450,0,100,100))

        if pixels:
            for p,c in pixels[0]:
                x,y =(p%self.width*self.e),int(p/self.width)*self.e
                pygame.draw.rect(self.screen, c,(550 + x,y,self.e,self.e))
            for p,c in pixels[1]:
                x,y =(p%self.width*self.e),int(p/self.width)*self.e
                pygame.draw.rect(self.screen, c,(440 - x,y,self.e,self.e))

        pygame.display.flip()



class Client_renderer():
    def __init__(self, host, port):
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.addr = host,port
        print(self.addr)
        self.sock.connect(self.addr)

    def draw_mirror(self, pixels):

        blocksize = 16384
        sentinel = b'\x00\x00END_MESSAGE!\x00\x00'[:blocksize]

        data = pickle.dumps((1,pixels),protocol=2)

        while data:
            send, data = data[:blocksize], data[blocksize:]
            self.sock.send(send)
        self.sock.send(sentinel)

    def draw_asym(self,pixels):

        blocksize = 16384
        sentinel = b'\x00\x00END_MESSAGE!\x00\x00'[:blocksize]

        data = pickle.dumps((2,pixels),protocol=2)

        while data:
            send, data = data[:blocksize], data[blocksize:]
            self.sock.send(send)
        self.sock.send(sentinel)


class Animation_controller():

    def __init__(self):
        self.animations = dict()
        self.anim_list = dict()

    def add_anim(self, key,a):
        self.animations[key] = a

    def run(self):
        anim = None
        print('select')
        print(self.anim_list)
        self.select_anim()
        current_anim = -1
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    elif event.key == pygame.K_r:
                        self.select_anim()
                    else:
                        try:
                            kint = chr(event.key)
                            if current_anim != kint:
                                print('ok')
                                if anim != None:
                                    previous_anim = (anim.pixels, anim.type)
                                    anim.stop()
                                else: previous_anim = ([],1)
                                anim = self.animations[kint]
                                p, t = previous_anim
                                anim.set(p,t)
                                current_anim = kint
                        except:
                            print(f'{kint} is not bind')

            if anim:
                anim.update()

    def select_anim(self):
        for k,t in self.anim_list.items():
            s,v = t

            i = int(input(f'{k}? (1-{len(v)})'))
            self.add_anim(s, v[i-1])

            print(f'{s} -> {k}')
        print(self.animations.items())


Animation.add_renderer(Pixel_renderer())
host = "10.42.0.27"
# host = "localhost"
port = 8051
# Animation.add_renderer(Client_renderer(host,port))

print()
ac = Animation_controller()

ac.anim_list = {
    'start': ('a', [Start(100),Start2(100)]),
    'speed': ('s', [Speed([],100),Speed2(),Speed3()]),
    'status': ('d', [Status(),Status2('eyes')]),
    'stop': ('f', [Stop(), Close_vert(), Close_horiz(), CloseFade()])
}


ac.run()
