import socket,pickle, random, random, pygame,functools

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
        for p,c in pixels[0]:
            x,y =(p%self.width*self.e),int(p/self.width)*self.e
            pygame.draw.rect(self.screen, c,(550 + x,y,self.e,self.e))
        for p,c in pixels[1]:
            x,y =(p%self.width*self.e),int(p/self.width)*self.e
            pygame.draw.rect(self.screen, c,(440 - x,y,self.e,self.e))

        pygame.display.flip()

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
            render.draw_mirror(list)

server()
