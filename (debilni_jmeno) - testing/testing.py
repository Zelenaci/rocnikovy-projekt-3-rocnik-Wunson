import tkinter as tk
from functools import partial

bg_blue = "#3CAEE5"

window = tk.Tk()

window.title("best game ever")

wd_width = 800
wd_height = 600
wd_size =(str(wd_width),"x",str(wd_height))
window.geometry("".join(wd_size))

def turn(x,y):
    print(x,y)

for x in range(0,10):
    for y in range(0,10):
        tile_x = 0
        tile_y = 0
        tile_pad = 5
        tile_square = 50
        
        tile = tk.Button(window,
                         bd = 0,
                         bg = "blue",
                         command = partial(turn, x, y))
        
        
        
        
        tile.place(x = tile_x + x * (tile_square + tile_pad),
                   y = tile_y + y * (tile_square + tile_pad),
                   width = tile_square,
                   height = tile_square,
                   )

window.mainloop()