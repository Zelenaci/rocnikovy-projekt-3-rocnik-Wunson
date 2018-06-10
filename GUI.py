import pygame

pygame.init()

# Nastavení okna
wd_widht = 640
wd_height = 480
window = pygame.display.set_mode((wd_widht,wd_height))
pygame.display.set_caption("Ultimate super mega Lodě")

clock = pygame.time.Clock()  #casovac okna - pro jednotlivé instance nastavíme později

#Definování barev pro snadnější použití pozdeji
black = (0,0,0)
white = (255,255,255)
brigth_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)

bg_light_blue = (80,176,255)
button_gray = (224,224,224)
button_gray_mouse  =(192,192,192)
#Definování fontů pro texty
small_button_text = pygame.font.SysFont("comicsansms",20)    #(font,size)
largetext = pygame.font.Font("freesansbold.ttf" ,115)


def text_object(text,font,color):       #dk how it works but it does xD
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def render_text(text,font,x,y,color = black):
    TextSurf, TextRect = text_object(text,font,color)
    TextRect.center = (x,y)
    window.blit(TextSurf, TextRect)
    pygame.display.update()
    
    
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
        
    render_text(label,small_button_text,(x+w//2),(y+h//2)) #add text to button
    
def quit_game():
    pygame.quit()
    quit()    
    
    
def test_screen():
    test = True
    while test: #very important to have a cycle!!!
    
        for event in pygame.event.get(): #so it can be closed
            if event == pygame.QUIT:
                quit_game()
                
                
        window.fill(white)
        render_text("test",largetext,wd_widht//2,wd_height//2) #text text
        
        button("test",brigth_red,bright_green,wd_widht//2,int(7*wd_height//8),100,50,quit_game) #test buton
        
        
        pygame.display.update()   #redner things to screen
        
        clock.tick(15) #15 FPS

def main_menu():
    m_menu = True
    while m_menu: #very important to have a cycle!!!
    
        for event in pygame.event.get(): #so it can be closed
            if event == pygame.QUIT:
                m_menu = False
                quit_game()
                
                
        window.fill(bg_light_blue)
        render_text("Lodě",largetext,wd_widht//2,wd_height//3) #text text
        
        button("Play",button_gray,button_gray_mouse,wd_widht//2,(wd_height//2)+50,150,30,quit_game) #test buton
        
        
        pygame.display.update()   #redner things to screen
        
        clock.tick(15) #15 FPS
             
main_menu()
pygame.quit()
quit()