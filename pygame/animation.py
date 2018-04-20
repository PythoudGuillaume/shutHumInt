import random,pygame,socket,pickle,time
from PIL import Image

class Animation:
    def __init__(self, pixels, height, width):
        host = "10.42.0.27"
        port = 15555

        pygame.init()

        self.pixels = pixels
        self.height = height
        self.width = width
        screen = Pixel_renderer()
        hard = Client_renderer(host,port)
        self.output = [screen,hard]
        self.clock = pygame.time.Clock()

    def render(self, kind):
        print(self.pixels)
        if kind == 1:
            for o in self.output:
                o.draw(self.pixels)
        if kind == 2:
            print('asymetrical')
        self.clock.tick(5)

    def stop(self):
        return self.pixels

class Start(Animation):
    def __init__(self, max_p):
        super().__init__( [], 10, 45)
        self.max_p = max_p

    def update(self):
        if len(self.pixels) < self.max_p:
            b = (int(self.width/self.max_p*len(self.pixels)))
            p = random.randint(0,9)*self.width+b
            self.pixels.append(p)
        super().render(1)


class Speed(Animation):
    def __init__(self, pixels, max_p):
        super().__init__(pixels,10,45)
        self.max_p = max_p

    def update(self):
        if len(self.pixels) < self.max_p:
            p = random.randint(1,10)*45 - 1
            self.pixels.append(p)

        new_pixels = []
        for p in self.pixels:
            x,y =(p%self.width),int(p/self.width)
            max = int((x*5)/44)
            min = int((x*3)/44)
            val = random.randint(min,max)
            x = x+(1+val)
            if x > 44:
                x = 0
                y = random.randint(0,9)

            new_pixels.append(x%self.width+y*self.width)

        self.pixels = new_pixels
        super().render(1)

class Static(Animation):
    def __init__(self, img):
        super().__init__([],10,45)
        im = Image.open(img)
        pix = list(im.getdata())
        self.pixels = [i for i, x in enumerate(pix) if x == (255,255,255)]


    def update(self):
        new_pixels = []
        for p in self.pixels:
                x,y =p%self.width + 1,int(p/self.width)
                if y >= self.width:
                    y = 0
                new_pixels.append(x%self.width+y*self.width)
        self.pixels = new_pixels
        super().render(1)

class Arrow(Animation):
    def __init__(self):
        super().__init__([],10,45)
        self.top_left = 0


    def update(self):
        self.pixels = []
        first_line = []
        if self.top_left >= 45:
            self.top_left = 0

        first_line.append(self.top_left)
        val = self.top_left -5
        while val >= 0:
            first_line.append(val)
            val -= 5
        val = self.top_left+5
        while val < self.width:
            first_line.append(val)
            val += 5

        self.pixels += first_line
        n = 1
        for l in range(1, self.height):
            for p in first_line:
                new_p = p + self.width*l - n
                if new_p >= 0 or new_p <= self.width:
                    self.pixels.append(new_p)

            if l >= self.height/2:
                n-=1
            elif l == self.height/2 - 1:
                n = n
            else:
                n+=1

        self.top_left += 1

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
        for p in pixels:
            x,y =(p%self.width*self.e),int(p/self.width)*self.e
            pygame.draw.rect(self.screen,self.foreground,(550 + x,y,self.e,self.e))
            pygame.draw.rect(self.screen,self.foreground,(440 - x,y,self.e,self.e))
        pygame.display.flip()



class Client_renderer():
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print("Connection on {}".format(port))


    def draw(self, pixels):
        data = pickle.dumps(pixels, protocol=2)
        self.socket.send(data)




anim = Static('apero.png')
while 1:
    anim.update()
