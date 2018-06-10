import tkinter as tk

bg_blue = "#3CAEE5"

window = tk.Tk()

window.title("best game ever")

wd_width = 640
wd_height = 480
wd_size =(str(wd_width),"x",str(wd_height))
window.geometry("".join(wd_size))

def turn(x,y):
    print(x,y)

for x in range(0,10):
    for y in range(0,10):
        tile_x = 0
        tile_y = 0
        tile_pad = 5
        tile_square = 10
        
        tile = tk.Button(window,
                         bd = 0,
                         bg = "blue",
                         command = lambda:turn(x+1,y+1))
        tile.place(x = tile_x + x * (tile_square + tile_pad),
                   y = tile_y + y * (tile_square + tile_pad),
                   width = tile_square,
                   height = tile_square,
                   )

window.mainloop()