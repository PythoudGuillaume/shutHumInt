import pygame
from PIL import Image
import random
import time
import sys

h = 10
w = 45
e = 10

state = 0
pause_s = 0
laststate = -1
max_pix = 2*w

speed = 30
pixels = []

blink = 1
blink_i = 1

focus = 1

pup = []
glob = []
times = 0
inc = 1
pause = 0

foreground = (255,255,255)
background = (0,0,0)
midbox = background

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
beep = pygame.mixer.Sound('440.wav')

def img_2_list(img):
    im = Image.open(img)

    pixels = list(im.getdata())
    width, height = im.size
    print(width,height)
    return pixels

def random_color():
    r = random.randint(150,255)
    g = random.randint(150,255)
    b = random.randint(150,255)
    fg = (r, g, b)
    bg = (255 - r, 255 - g, 255 - b)
    return (fg,bg)

def anim_blink(screen):
    global blink, blink_i,state, speed
    speed = 30
    if blink == 0 :
        state = 4
        blink = 1
        blink_i*=-1
        speed = 10
        return

    screen.fill(background)
    pygame.draw.rect(screen,midbox,(450,0,100,100))

    plist = img_2_list('eyes'+str(blink)+'.png')
    eyes = [i for i, x in enumerate(plist) if x == (255,255,255) ]
    for g in eyes:
        x,y =(g%w),int(g/w)
        pygame.draw.rect(screen,foreground,(550 + x*e,y*e,e,e))
        pygame.draw.rect(screen,foreground,(440 - x*e,y*e,e,e))
    for p in pup:
        x,y =p%w,int(p/w)
        pygame.draw.rect(screen,foreground,(550 + (x+times)*e,y*e,e,e))
        pygame.draw.rect(screen,foreground,(440 - (x-times)*e,y*e,e,e))

    if blink == 7 :
        blink_i *= -1

    blink += blink_i

def anim_look(screen):
    global times, inc, beep, pixels, pause, focus, pup, state

    screen.fill(background)
    pygame.draw.rect(screen,midbox,(450,0,100,100))

    plist = img_2_list('eyes'+str(focus)+'.png')
    glob = [i for i, x in enumerate(plist) if x == (255,255,255)]
    pup = [i for i, x in enumerate(plist) if x == (254,254,254)]

    pixels = []

    new_p = []
    for g in glob:
        x,y =(g%w),int(g/w)
        pygame.draw.rect(screen,foreground,(550 + x*e,y*e,e,e))
        pygame.draw.rect(screen,foreground,(440 - x*e,y*e,e,e))

    if (pause == 0) and ((times > 2) or (times < -2)):
        beep.play(loops=0, maxtime=70, fade_ms=0)
        pause = 5

    if pause > 1:
        pause -= 1

    elif pause == 1:
        pause -= 1
        inc*=-1
        times+=inc

    else:
        times+=inc
    print(pause)

    print(times)
    for p in pup:
        x,y =p%w,int(p/w)
        pygame.draw.rect(screen,foreground,(550 + (x+times)*e,y*e,e,e))
        pygame.draw.rect(screen,foreground,(440 - (x-times)*e,y*e,e,e))
        new_p.append(x%w+y*w)

    if times == 0:
        if random.randint(0,10) > 7:
            state = 5

def anim_start():
    global pixels, max_pix
    print('started')
    if len(pixels) < max_pix:
        if not pygame.mixer.get_busy() and len(pixels)%10 == 0:
            beep.play(0,50,0)
        p = random.randint(0,449)
        pixels.append(p)
        beep.set_volume(len(pixels)/60.*1.)
    elif pygame.mixer.get_busy():
         beep.stop()

def anim_start_bottom():
    global pixels, max_pix
    print('started')
    if len(pixels) < max_pix:
        if not state == laststate:
            beep.play()
        b = int(10/max_pix*len(pixels))+1
        p = random.randint(w*h-w*b,w*h-w*(b-1))
        pixels.append(p)
        beep.set_volume(len(pixels)/60.*1.)
    elif pygame.mixer.get_busy():
         beep.stop()

def anim_start_mid():
    global pixels, max_pix
    print('started')
    if len(pixels) < max_pix:
        if not state == laststate and 0:
            beep.play()
        b = (int(w/max_pix*len(pixels)))
        print(b)
        p = random.randint(0,9)*w+b
        print(p)
        pixels.append(p)
        beep.set_volume(len(pixels)/60.*1.)
    elif pygame.mixer.get_busy():
         beep.stop()



def anim_speed():
    n = 0
    new_p = []
    kg = 1
    global pixels,max_pix
    if len(pixels) < max_pix:
        p = random.randint(0,449)
        pixels.append(p)
    for p in pixels:
        x,y =(p%w)+1,int(p/w)
        if x > 44:
            x = 0
            y = random.randint(0,9)

        new_p.append(x%w+y*w)
    pixels = new_p

def anim_stop():
    global pixels,state, speed
    if speed > 10:
        speed -= 3
        anim_speed()
    elif pixels:
        print(pixels)
        new_p = []
        for p in pixels:
            x,y =(p%w)+1,int(p/w)+1
            if y < h:
                new_p.append(x%w+y*w)
        pixels = list(new_p)
    else :
        state = 4
def draw_pixel(screen):

    screen.fill(background)
    pygame.draw.rect(screen,midbox,(450,0,100,100))
    for p in pixels:
        x,y =(p%w*e),int(p/w)*e
        pygame.draw.rect(screen,foreground,(550 + x,y,e,e))
        pygame.draw.rect(screen,foreground,(440 - x,y,e,e))
    pygame.display.flip()

def anim_pixel(screen):
    global state
    if state > 1:
        beep.stop()
        beep.set_volume(1)
    if state == 1:
        anim_start_mid()
    elif state == 2:
        anim_speed()
    elif state == 3:
        anim_stop()
    elif state == 4:
        anim_look(screen)
        pygame.display.flip()
        return 1
    elif state == 5:
        anim_blink(screen)
        pygame.display.flip()
        return 1
    else :
        print("ok")
    print(state)
    if not state == 0:
        draw_pixel(screen)



def main():
    global state, laststate, speed,focus, pause_s,background, foreground, midbox
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(((2*w+10)*e,h*e))
    pix = []

    s = 10
    lastkey = None

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #start
                if event.key == pygame.K_a:
                    state = 1
                    speed = 20
                #mouvement
                elif event.key == pygame.K_s:
                    if state != 2:
                        speed = 10
                    state = 2
                #stop
                elif event.key == pygame.K_d:
                    state = 3
                #look
                elif event.key == pygame.K_f:
                    state = 4
                    speed = 10
                #blink
                elif event.key == pygame.K_b:
                    state = 5
                    speed = 10
                #change eyes form
                elif event.key == pygame.K_r:
                    if focus == 1 :
                        focus = 2
                    else:
                        focus = 1
                    print(focus)
                #pause animation
                elif event.key == pygame.K_SPACE:
                    if state == 0:
                        state = pause_s
                    else :
                        pause_s = state
                        state = 0
                #increase speed
                elif event.key == pygame.K_i:
                    if state == 2:
                        speed += 10
                #decrease speed
                elif event.key == pygame.K_k:
                    if state == 2:
                        speed -= 10
                        if speed < 1:
                            speed = 5
                elif event.key == pygame.K_y:

                    (foreground, background) = random_color()
                    midbox = background


                laststate = event.key
        anim_pixel(screen)
        clock.tick(speed)


if __name__ == '__main__':
    main()
