# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:56:14 2018

@author: jakubvasi, Wunson 
"""

import socket
from threading import Thread

MAX_BUFFER_SIZE = 4096
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

#_____Communication_______________________________________________________________________________#
def rx(soc):  
    data = []
    while True:
        rx_data_bytes = soc.recv(MAX_BUFFER_SIZE)
        rx_data = rx_data_bytes.decode("utf8").rstrip()
       
        if "--END--" in rx_data:                # Konec prenosu
            return data
        else:
            data.append(rx_data)
            soc.sendall("-".encode("utf8"))     # Ready for another data

def tx(soc, data):
    for x in data:
        msg = "{}\t".format(x)
        soc.sendall(msg.encode("utf8"))
        if soc.recv(MAX_BUFFER_SIZE).decode("utf8") == "-":    # Wait for response
            pass
    soc.send(b'--END--')

#_____Server______________________________________________________________________________________#
def client_thread(conn, ip, port):
        my_array = rx(conn)
        tx(conn, ["Success", 1, 2, "nejaka data", "funguje to!"])
        print(my_array)
        print('Connection ' + ip + ':' + port + " ended")
        conn.close()

def get_local_IP():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
                if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
                s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
                socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

def start_server(local_IP):
    print('Vase IP: ' + local_IP)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        soc.bind((local_IP, 666))
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()
    
    soc.listen(10)
    
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Error!")
            import traceback
            traceback.print_exc()
    soc.close()


#_____Client______________________________________________________________________________________#
def client(server_ip = "10.0.0.35", data = []):    
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    try:
        soc.connect((server_ip, 666))
    except:
        return("Error, connection failed!")
    
    tx(soc, data)
    response = rx(soc)
    return(response)
    
    
#*************************************************************************************************#    
import tkinter as tk
from functools import partial

#____Windows options__________________________________________________________#
# Colors
bg_blue = "#3CAEE5"
menubuton_activebg = "#94A7B1"
menubuton_bg = "#BED5E1"
sea_blue = "#3496C5"
act_sea_blue = "#2380AC"

# Window
window = tk.Tk()

# Window Title
window.title("best game ever")

# Window Size
wd_width = 800
wd_height = 600
wd_size =(str(wd_width),"x",str(wd_height))
window.geometry("".join(wd_size))
#_____________________________________________________________________________#

def place_ships(x,y):
    global ship_counter
    global game_grid
    if game_grid[x][y] == 0 and ship_counter < 20:
        game_grid[x][y] = 1
        pole[x][y].configure(bg = "black")
        ship_counter += 1
        
        #####_Test_###############
        response = client(data=["shot", x, y])
        print(response)
        ##########################
    
    elif game_grid[x][y] == 1 and ship_counter > 0:
        game_grid[x][y] = 0
        pole[x][y].configure(bg = sea_blue)
        ship_counter -= 1

# generate buton grid with function in them
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
    window.configure(background = bg_blue)
    
    buttons = []
    labels = ["Host", "Join"]
    commands = [host_wd, join_wd]
    
    for i in range(0, 2):
        buttons.append(tk.Button(window,
                     text = labels[i],
                     font =("Arial",30),
                     bd = 0,
                     bg = menubuton_bg,
                     activebackground = menubuton_activebg,
                     command = partial(commands[i], buttons)))    
    
        buttons[i].place(x = (wd_width/2)-50,
               y = (i+1)*wd_height/4,
               width = 100,
               height = 50)


#_____Place ships_____________________________________________________________#
def del_buttons(buttons):
    for i in buttons:
        i.destroy()

#_____Place ships_____________________________________________________________#
def place_wd():
    button_grid(place_ships)

#_____Host window_____________________________________________________________#
def host_wd(buttons):
    local_IP = get_local_IP()
    Thread(target=start_server, args=(local_IP,)).start()
    
    title = tk.Label(window, text = local_IP, font = ("times",36))
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
    

#_____Main________________________________________________________________________________________#

main_menu()
window.mainloop()
