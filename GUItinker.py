import tkinter as tk
from functools import partial

ship_counter = 0
pole = []
game_grid =        [[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]]

ip_adr = ""

#____Colors___________________________________________________________________#
bg_blue = "#3CAEE5"
menubuton_activebg = "#94A7B1"
menubuton_bg = "#BED5E1"
sea_blue = "#3496C5"
act_sea_blue = "#2380AC"

#define window
window = tk.Tk()

#window title
window.title("best game ever")

#window size
wd_width = 800
wd_height = 600
wd_size =(str(wd_width),"x",str(wd_height))
window.geometry("".join(wd_size))

def place_ships(x,y):
    global ship_counter
    global game_grid
    if game_grid[x][y] == 0 and ship_counter < 20:
        game_grid[x][y] = 1
        pole[x][y].configure(bg = "black")
        ship_counter += 1
    
    elif game_grid[x][y] == 1 and ship_counter > 0:
        game_grid[x][y] = 0
        pole[x][y].configure(bg = sea_blue)
        ship_counter -= 1 


#generate buton grid with function in them
def button_grid(function):   
    for x in range(0,10):
        row = []
        for y in range(0,10):
            tile_x = 0
            tile_y = 0
            tile_pad = 1
            tile_square = 50
            
            tile = tk.Button(window,
                             bd = 0,
                             bg = sea_blue,
                             activebackground = act_sea_blue,
                             command = partial(function, x, y))
            
            tile.place(x = tile_x + x * (tile_square + tile_pad),
                       y = tile_y + y * (tile_square + tile_pad),
                       width = tile_square,
                       height = tile_square,
                       )
            row.append(tile)
        pole.append(row)

#_____Main menu_______________________________________________________________#
def main_menu():
    #change background
    window.configure(background = bg_blue)
    
    buttons = []
    labels = ["Host", "Join"]
    
    for i in range(0, 2):
        buttons.append(tk.Button(window,
                     text = labels[i],
                     font =("Arial",30),
                     bd = 0,
                     bg = menubuton_bg,
                     activebackground = menubuton_activebg,
                     command = partial(host_wd, buttons)))    
    
        buttons[i].place(x = (wd_width/2)-50,
               y = (i+1)*wd_height/4,
               width = 100,
               height = 50)








def del_buttons(buttons):
    for i in buttons:
        i.destroy()


#_____Place ships_____________________________________________________________#
def place_wd():
    #change background
    window.configure(background = bg_blue)
    
    button_grid(place_ships)

#_____Host window_____________________________________________________________#
def host_wd(buttons):
    global ip_adr
    
    title = tk.Label(window, text = str(ip_adr), font = ("times",36))
    title.place(x = 0, y = 0)
    
    del_buttons(buttons)

#_____Join window_____________________________________________________________#
def join_wd(buttons):
    global ip_adr
    
    ip = tk.Entry(window)
    ip.place(x = 0, y = 0)
    ip_adr = ip.get()
    
    del_buttons(buttons)
    
    
place_wd()    
#main_menu()
window.mainloop()