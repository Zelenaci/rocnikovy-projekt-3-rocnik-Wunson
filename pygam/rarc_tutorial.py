# -*- coding: utf-8 -*-
"""
Created on Sat May  5 20:19:23 2018

@author: Ondra
"""
import random
import pygame

pygame.init()

wd_widht = 800      #set window dimentions
wd_height = 600
window = pygame.display.set_mode((wd_widht,wd_height))
pygame.display.set_caption("racr")

clock = pygame.time.Clock()

#Colors
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)

#Fonts
largetext = pygame.font.Font("freesansbold.ttf" ,115)
small_button_text = pygame.font.SysFont("comicsansms",20)

carimg = pygame.image.load("racecar.png")
car_width = 73     #width of the car in pixels

pause = False

def button(label,color,mouse_on_color,x,y,w,h,action=None): #all numbers must be int
    x -= w//2           #center the coorinates
    y -= h//2
    hitbox = range(x,x+w) #hitbox of the button 
    hitboy = range(y,y+h)
    
    mouse = pygame.mouse.get_pos()  #coordinates of mouse pointer
    click = pygame.mouse.get_pressed()
    
    if mouse[0] in hitbox and mouse[1] in hitboy: #change color no mouse hover
        pygame.draw.rect(window,mouse_on_color,(x,y,w,h))
        
        if click[0] == 1 and action != None: #execute click action if any
            action()
    else:
        pygame.draw.rect(window,color,(x,y,w,h))
        
    render_text(label,small_button_text,black,(x+w//2),(y+h//2)) #add text to button



def text_object(text,font,color):       #dk how it works but it does xD
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def render_text(text,font,color,x,y):
    TextSurf, TextRect = text_object(text,font,color)
    TextRect.center = (x,y)
    window.blit(TextSurf, TextRect)
    pygame.display.update()

def game_quit():
            pygame.quit()
            quit()

def blocks(blockx,blocky,blockw,blockh,color):  #draws falling blocks
    pygame.draw.rect(window,color,[blockx,blocky,blockw,blockh])

def car(x,y):
    window.blit(carimg,(x,y))

def dislpay_score(count):
    font = pygame.font.SysFont(None,25)
    text = font.render("Score: "+str(count),True,black)
    window.blit(text,(0,0))

def game_intro():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()    
            
        window.fill(white)
        render_text("game",largetext,black,wd_widht//2,wd_height//2)
        
        button("Start",green,bright_green,wd_widht//4,int(wd_height*0.7),100,50,game_loop)
        button("Quit",red,bright_red,(3*wd_widht)//4,int(wd_height*0.7),100,50,game_quit)
        
        pygame.display.update()
        clock.tick(15)

def crash():
    gameover = True
    
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()    
            
        window.fill(white)
        render_text("game over",largetext,black,wd_widht//2,wd_height//2)
        
        button("Again",green,bright_green,wd_widht//4,int(wd_height*0.7),100,50,game_loop)
        button("Quit",red,bright_red,(3*wd_widht)//4,int(wd_height*0.7),100,50,game_quit)
        
        pygame.display.update()
        clock.tick(15)
def unpause():
    global pause
    pause = False

def paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()    
            
        render_text("Paused",largetext,black,wd_widht//2,wd_height//2)
        
        button("Continue",green,bright_green,wd_widht//4,int(wd_height*0.7),100,50,unpause)
        button("Quit",red,bright_red,(3*wd_widht)//4,int(wd_height*0.7),100,50,game_quit)
        
        pygame.display.update()
        clock.tick(15)
    
    
def game_loop():
    global pause
    
    x = wd_widht * 0.45
    y = wd_height * 0.8
    xmove = 0
    
    block_x = random.randrange(0,wd_widht - 100)
    block_y = -600
    block_speed = 7
    block_height = 100
    block_width = 100
    dodged = 0    
    game_exit = False    
    
    
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xmove -= 5
                if event.key == pygame.K_RIGHT:
                    xmove += 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    xmove = 0
                    
        x += xmove
            
        window.fill(white)
        
        blocks(block_x,block_y,block_width,block_height,black)
        block_y += block_speed
        
        car(x,y)
        dislpay_score(dodged)
        
        if x > wd_widht - car_width or x < 0 :
            crash()
        
        if block_y > wd_height:
            block_y = 0 - wd_height
            block_x = random.randrange(0,wd_widht - 100)    
            dodged += 1
            block_speed += 1
            block_width += int(dodged * 1.2)
        
        block_hitx = range(block_x,block_x+block_width)
        block_hity = range(block_y,block_y+block_height)
        
        if y in block_hity or y + 82 in block_hity:
            if x in block_hitx or x + car_width in block_hitx:
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()    
game_loop()
pygame.quit()
quit()