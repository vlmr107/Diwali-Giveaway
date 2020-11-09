x = 250
y = 30
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame
import time
import random


pygame.init()
##############
crash_sound = pygame.mixer.Sound("crash.wav")
##############
display_w = 800
display_h = 600

background = pygame.image.load('picture4.png')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
yellow = (255, 255, 0)
green = (0,128,0)
car_width = 73
Display = pygame.display.set_mode((display_w,display_h))
pygame.display.set_caption('Car game')
clock= pygame.time.Clock()
carImg = pygame.image.load("racecar1.png")
pause = False

def quitgame():
    pygame.quit()
    quit()
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x  and y + h > mouse[1] > y:
        pygame.draw.rect(Display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(Display, ic, (x, y, w, h))
    smalltext = pygame.font.SysFont("comicsansms",20)
    TextSurf, TextRect = text_objects(msg, smalltext)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    Display.blit(TextSurf, TextRect)

def unpause():
    pygame.mixer.music.unpause()
    global pause
    pause = False
def paused():

    pygame.mixer.music.pause()
    largetext = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largetext)
    TextRect.center = ((display_w/2), (display_h/2))
    Display.blit(TextSurf, TextRect)
    while pause:
        print(pause)
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("continue", 150,450,100,50, green, blue, unpause)
        button("exit", 550,450,100,50, red, blue, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_intro(text):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        Display.blit(background,(0,0))
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects(text, large_text)
        TextRect.center = ((display_w / 2), (display_h / 2))
        Display.blit(TextSurf, TextRect)

        pygame.draw.rect(Display, green,(150,450,100,50))
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = text_objects('Go!', smalltext)
        TextRect.center = ((150+ (100/ 2)), (450+(50/ 2)))
        Display.blit(TextSurf, TextRect)


        pygame.draw.rect(Display, red, (550, 450, 100, 50))

        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = text_objects('Exit!', smalltext)
        TextRect.center = ((550+ (100/ 2)), (450+(50/ 2)))
        Display.blit(TextSurf, TextRect)

        button("Go!", 150, 450, 100, 50, green, blue, game_loop)
        button("Exit!", 550, 450, 100, 50, red, blue, quitgame)

        pygame.display.update()
        clock.tick(100)
        #time.sleep(3)
        #intro = False



def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("dodged: "+ str(count), True, white)
    Display.blit(text,(0,0))


def thing(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(Display, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    Display.blit(carImg, (x,y))
def text_objects(text, font):
    text_surface = font.render(text,True,white)
    return text_surface, text_surface.get_rect()
def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect =text_objects(text,large_text)
    TextRect.center=((display_w/2),(display_h/2))
    Display.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()
def crash():

    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    #message_display('You crashed')
    large_text = pygame.font.SysFont('comicsansms', 115)
    TextSurf, TextRect = text_objects('You crashed!', large_text)
    TextRect.center = ((display_w / 2), (display_h / 2))
    Display.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Play Again", 150, 450, 100, 50, green, blue, game_loop)
        button("Exit!", 550, 450, 100, 50, red, blue, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    global pause

    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)

    x = display_w*0.45
    y = display_h*0.8
    x_change = 0
    car_speed = 0
    GameExit = False


    thing_startx = random.randrange(0, display_w)
    thing_starty = -600
    thing_speed = 7
    thing_width =  100
    thing_height = 100

    dodged = 0
    #crashed=False
    while not GameExit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type== pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    print("paused")
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0
        x += x_change

        Display.blit(background,(0,0))
        ###################
        thing(thing_startx, thing_starty, thing_width, thing_height, red)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
        if x > display_w - car_width or x < 0:
            crash()

        if thing_starty > display_h:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_w)
            dodged += 1
            if dodged >= 2 and dodged < 12:
                thing_speed += 1
            if dodged >= 10:
                thing_width = 100
            thing_width += (dodged*1.2)

        if y < thing_starty + thing_height:
            print('ycrossover')

            if x > thing_startx and x < thing_startx + thing_width or x + \
                car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print('xcrossover')
                crash()
        pygame.display.update()
        clock.tick(60)
game_intro("Racey Game")
game_loop()
pygame.quit()
quit()