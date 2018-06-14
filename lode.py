# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:56:14 2018

@author: jakubvasi, Wunson 
"""

import socket
from threading import Thread

mode = "UNDEF"

ip_adr = ""
MAX_BUFFER_SIZE = 4096
PORT = 1025

ship_counter = 0

my_pole = []
enemy_pole = []

my_grid =          [[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]]
                   
enemy_grid =       [[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]]

enemy_grid_hidden = [[0,0,0,0,0,0,0,0,0,0],
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
       
        if "--END--" in rx_data:                                # End of transfer
            return data
        else:
            data.append(rx_data)
            soc.sendall("-".encode("utf8"))                     # Ready for another data

def tx(soc, data_type = "X", data = []):
    tx_data = [data_type]
    tx_data.extend(data)
    
    for x in tx_data:
        msg = "{}\t".format(x)
        soc.sendall(msg.encode("utf8"))
        if soc.recv(MAX_BUFFER_SIZE).decode("utf8") == "-":     # Wait for response
            pass
    soc.send(b'--END--')
    
def process_data(conn, data = []):
    try:
        data_type = data.pop(0)
    except:
        tx(conn, "M", "Error")
    
    if data_type == "L":
        global enemy_grid
        enemy_grid = data
        tx(conn, "C")
        
    else:
        tx(conn, "X")
        
#_____Server______________________________________________________________________________________#
def client_thread(conn, ip, port):
        received_data = rx(conn)
        process_data(conn, received_data)
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
        soc.bind((local_IP, PORT))
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()
    
    soc.listen(10)
    
    send_buffer = []
    
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
def client(server_ip, data_type = "X", data = []):    
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    soc.settimeout(1000)
    try:
        soc.connect((server_ip, PORT))
    except:
        return("Error, connection failed!")
    soc.settimeout(None)
    
    tx(soc, data_type, data)
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
    global my_grid
    if my_grid[x][y] == 0 and ship_counter < 20:
        my_grid[x][y] = 1
        my_pole[x][y].configure(bg = "black")
        ship_counter += 1
    
    elif my_grid[x][y] == 1 and ship_counter > 0:
        my_grid[x][y] = 0
        my_pole[x][y].configure(bg = sea_blue)
        ship_counter -= 1
        

# generate buton grid with function in them
def button_grid(function,tile_x = 0,tile_y = 0, pole = my_pole):   
    for x in range(0,10):
        row = []
        for y in range(0,10):
            tile_pad = 1
            tile_square = 50
            
            tile = tk.Button(window,
                             bd  = 0,
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

#_____Killer__________________________________________________________________#
def killer(widgets):
    for i in widgets:
        i.destroy()
        
def ip_get(entry):              #Get IP from text field
    global ip_adr
    ip_adr = entry.get()
    
    response = client(ip_adr)   #Check connection
    print(response)
    
#_____Main menu_______________________________________________________________#
def main_menu(widgets = []):
    window.configure(background = bg_blue)
    
    widgets = []
    labels = ["Host", "Join"]
    commands = [host_wd, join_wd]
    
    title = tk.Label(window,
                     text = "HRA LODĚ   ",
                     font =("Arial Black",50),
                     bg = bg_blue,
                     fg = "white"
                     )
    title.pack()
    
    
    for i in range(0, 2):
        widgets.append(tk.Button(window,
                     text = labels[i],
                     font =("Arial Black",30),
                     bd = 0,
                     fg = "white",
                     bg = sea_blue,
                     activebackground = act_sea_blue,
                     command = partial(commands[i], widgets)))    
    
        widgets[i].place(x = (wd_width/2)-75,
               y = ((i+1)*wd_height/4) + 75,
               width = 150,
               height = 75)
        
    widgets.append(title)


#_____Host window_____________________________________________________________#
def host_wd(widgets):
    global mode
    
    killer(widgets)
    
    mode = "SERVER"
    local_IP = get_local_IP()
    Thread(target=start_server, args=(local_IP,)).start()
    
    window.configure(background = bg_blue)
    
    widgets = []
    
    label = tk.Label(window,
                     text = "Your IP is:",
                     font =("Arial Black",20),
                     bg = bg_blue,
                     fg = "white"
                     )
    
    label.grid(row = 0,
               column = 0)
    
    widgets.append(label)
    
    ip_label = tk.Label(window,
                     text = local_IP,
                     font =("Arial Black",20),
                     bg = bg_blue,
                     fg = "white"
                     )
    
    ip_label.grid(row = 0,
                  column = 1)
    
    widgets.append(ip_label)
    
    start = tk.Button(window,
                       text = "Start",
                       font =("Arial Black",30),
                       bd  = 0,
                       fg = "white",
                       bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(place_wd, widgets))
    
    start.place(x = (wd_width/2)-75,
                y = (wd_height/3),
                width = 150,
                height = 75)
    
    widgets.append(start)
    

#_____Join window_____________________________________________________________#
def join_wd(widgets):
    global ip_adr
    global mode
    
    killer(widgets)
    
    mode = "CLIENT"
    ip_label = tk.Label(window,
                     text = "Connect to:",
                     font =("Arial Black",10),
                     bg = bg_blue,
                     fg = "white"
                     )
    
    ip_label.grid(row = 0,
                  column = 0)
    
    widgets.append(ip_label)
    
    
    
    ip = tk.Entry(window)
    
    ip.grid(row = 0, column = 1,)
    
    widgets.append(ip)
    
    confirm = tk.Button(window,
                       text = "Connect",
                       font = ("Arial Black", 10),
                       bd  = 0,
                       fg = "white",
                       bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(ip_get,ip)
                       )
    
    confirm.grid(row = 0, 
                 column = 2,)
    
    widgets.append(confirm)
    
    
    
    connect = tk.Button(window,
                      text = "Start",
                      font =("Arial Black",30),
                      bd  = 0,
                      fg = "white",
                      bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(place_wd, widgets))
    
    connect.place(x = (wd_width/2)-100,
                y = (wd_height/3),
                width = 200,
                height = 75)
    
    widgets.append(connect)
    

#_____Place ships_____________________________________________________________#
def place_wd(widgets):
    killer(widgets)
    button_grid(place_ships,tile_y = 65,)
    
    title = tk.Label(window,
                     text = "Place your ships",
                     font =("Arial Black",30),
                     bg = bg_blue,
                     fg = "white"
                     )
    
    title.pack()

    widgets.append(title)
    
    done = tk.Button(window,
                      text = "Done",
                      font =("Arial Black",30),
                      bd  = 0,
                      fg = "white",
                      bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(game_wd, widgets))
    
    done.place (x = 550,
                y = (wd_height/3),
                width = 200,
                height = 75)
    
    widgets.append(done)


#_____Place ships_____________________________________________________________#
def game_wd(widgets):
    killer(widgets)
    
    if mode == "CLIENT":
        response = client(ip_adr, "L", my_grid) 
        print(response)
    
    
    button_grid(place_ships,tile_x = 600,tile_y = 65, pole = enemy_pole)
    wd_width = 1150
    wd_height = 600
    wd_size =(str(wd_width),"x",str(wd_height))
    window.geometry("".join(wd_size))


#_____Main____________________________________________________________________#

main_menu()
window.mainloop()