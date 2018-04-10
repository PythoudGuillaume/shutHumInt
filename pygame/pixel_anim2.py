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


detect_lev = 1
pup = []
glob = []
times = 0
inc = 1
pause = 0

foreground = (255,255,255)
background = (0,0,0)

eyes_pixel = []

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
beep = pygame.mixer.Sound('fuzzy_beep_short.wav')

start = pygame.mixer.Sound('train_start.wav')
start = pygame.mixer.Sound('win31.wav')
start = pygame.mixer.Sound('carstart.wav')

#http://soundbible.com/291-Fuzzy-Beep.html

#utility function
def img_2_list(img):
    im = Image.open(img)

    pixels = list(im.getdata())
    width, height = im.size
    return pixels

def random_color():
    r = random.randint(150,255)
    g = random.randint(150,255)
    b = random.randint(150,255)
    fg = (r, g, b)
    bg = (255 - r, 255 - g, 255 - b)
    return (fg,bg)

def sound_detect(lvl = 10, snd = beep):
    snd.play(loops=lvl-1, maxtime=0, fade_ms=0)
    print('played')


def draw_background(screen):
    screen.fill(background)


    pygame.draw.rect(screen,(100,100,100),(25*e,2*e,3*e,10*e))
    pygame.draw.rect(screen,background,(450,0,100,100))



#animtion function
def anim_blink(screen):
    global blink, blink_i,state, speed
    speed = 30
    if blink == (focus-1) :
        state = 4
        blink = focus
        blink_i*=-1
        speed = 10
        return

    draw_background(screen)

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
    global times, inc, beep, pixels, pause, focus, pup, glob, state, background, blink

    draw_background(screen)

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
        sound_detect(detect_lev)
        pause = 5

    if pause > 1:
        pause -= 1

    elif pause == 1:
        pause -= 1
        inc*=-1
        times+=inc

    else:
        times+=inc

    for p in pup:
        x,y =p%w,int(p/w)
        pygame.draw.rect(screen,foreground,(550 + (x+times)*e,y*e,e,e))
        pygame.draw.rect(screen,foreground,(440 - (x-times)*e,y*e,e,e))
        new_p.append(x%w+y*w)

    if times == 0:
        beep.stop()
        if random.randint(0,10) > 7:
            blink = focus
            state = 5
    (r,g,b) = background
    if not g == 200:
        g+=25
        if g > 255:
            g = 255
        background = (r,g,b)



def anim_look_stop(screen):
    global eyes_pixel, state, background


    draw_background(screen)
    if not eyes_pixel:
        eyes_pixel = glob + pup
    new_p = []

    for p in eyes_pixel:
            x,y =p%w,int(p/w) + 1
            pygame.draw.rect(screen,foreground,(550 + (x)*e,y*e,e,e))
            pygame.draw.rect(screen,foreground,(440 - (x)*e,y*e,e,e))
            if x < 45 and y < 10:
                new_p.append(x%w+y*w)
    eyes_pixel = new_p
    if not eyes_pixel:
        state = 3
        background = (0,0,0)
        draw_pixel(screen)
    print(eyes_pixel)

    (r,g,b) = background
    if not g == 0:
        g-=50
        if g < 0:
            g = 0
        background = (r,g,b)


def anim_start():
    global pixels, max_pix, state
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
    global pixels, max_pix, state
    if len(pixels) < max_pix:
        if not state == laststate:
            start.play()
        b = (int(w/max_pix*len(pixels)))
        p = random.randint(0,9)*w+b
        pixels.append(p)
        beep.set_volume(len(pixels)/60.*1.)
    elif pygame.mixer.get_busy():
         beep.stop()
         state = 2


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
        new_p = []
        for p in pixels:
            x,y =(p%w)+1,int(p/w)+1
            if y < h:
                new_p.append(x%w+y*w)
        pixels = list(new_p)
    else :
        #state = 4
        print('no more pixels')
def draw_pixel(screen):

    screen.fill(background)
    pygame.draw.rect(screen,background,(450,0,100,100))
    for p in pixels:
        x,y =(p%w*e),int(p/w)*e
        pygame.draw.rect(screen,foreground,(550 + x,y,e,e))
        pygame.draw.rect(screen,foreground,(440 - x,y,e,e))
    pygame.display.flip()

def anim_pixel(screen):
    print(laststate)
    global state
    if state > 1:
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
    elif state == 6:
        print('stop looking')
        anim_look_stop(screen)
        pygame.display.flip()
        return 1

    if not state == 0:
        draw_pixel(screen)



def main():
    global state, laststate, speed,focus, pause_s,background, foreground, background, detect_lev
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(((2*w+10)*e,h*e))
    pix = []

    s = 10
    lastkey = None

    while 1:
        laststate = state
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
                    if laststate == (4 or 5):
                        state = 6
                    else:
                        state = 3
                #look
                elif event.key == pygame.K_f:
                    state = 4
                    speed = 10

                #blink
                elif event.key == pygame.K_b:
                    blink = focus
                    state = 5
                    speed = 10
                #change eyes form
                elif event.key == pygame.K_r:
                    if focus == 1:
                        focus = 2
                    elif focus == 2:
                        focus = 5
                    else :
                        focus = 1
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
                        speed += 1
                    else:
                         detect_lev +=1
                #decrease speed
                elif event.key == pygame.K_k:
                    if state == 2:
                        speed -= 10
                        if speed < 1:
                            speed = 5
                    elif detect_lev > 1:
                         detect_lev -=1
                elif event.key == pygame.K_y:

                    (foreground, background) = random_color()
                    background = background

                elif event.key == pygame.K_q:
                    exit(0)

        anim_pixel(screen)
        clock.tick(speed)


if __name__ == '__main__':
    main()
