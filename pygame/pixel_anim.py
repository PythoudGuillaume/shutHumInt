import pygame
from PIL import Image

h = 10
w = 45
e = 10


def img_2_list(img):
    im = Image.open(img)

    pixels = list(im.getdata())
    width, height = im.size
    print(width,height)
    return pixels


def main():
    pygame.init()
    clock = pygame.time.Clock()
    plist = img_2_list('eyes.png')
    print(plist)
    screen = pygame.display.set_mode((w*e,h*e))
    screen.fill((0, 0, 0))

    decal = 0
    inc = 4
    out = 0

    while 1:
        screen.fill((0,0,0))
        p = 0
        while( p < h*w):
            x,y =(p%w*e + decal),int(p/w)*e
            if plist[p] == (255,255,255) and (x < 10 or x > (w*e-20)):
                out = 1
            pygame.draw.rect(screen,plist[p],(x,y,e,e))
            p+=1

        pygame.display.flip()
        if out:
            inc *= -1
            out = 0
        decal+= inc
        clock.tick(10)


if __name__ == '__main__':
    main()
