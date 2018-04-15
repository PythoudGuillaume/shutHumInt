import pygame, sys, time
from pygame.locals import*

pygame.init()
#DISPLAYSURF = pygame.display.set_mode((400, 300))
#pygame.display.set_caption("Sound!!")

beep = pygame.mixer.Sound('440.wav')
beep.play()
time.sleep(0.14)
beep.stop()
time.sleep(1)
beep.play()
time.sleep(0.14)
beep.stop()

while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
