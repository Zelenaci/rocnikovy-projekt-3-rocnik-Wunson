# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:56:14 2018

@author: jakubvasi, Wunson 
"""

import socket
from threading import Thread, Timer

server_EN = False
your_turn = False
ready_status = 0

shot_buffer = []
connection_status = "Disconnected"

# Data types
SHIP_LAYOUT = "L"
SHIP_LAYOUT_REQUEST = "R"
SHOT = "S"
SHOT_REQUEST = "K"
START_REQUEST = "T"
MESSAGE = "M"
NOTHING = "X"


ip_adr = ""
MAX_BUFFER_SIZE = 4096
PORT = 1025

ship_number = 20

my_pole = []        # List for storing buttons
enemy_pole = []     # List for storing buttons


my_grid =           [[0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0]]
                   
enemy_grid =        [[0,0,0,0,0,0,0,0,0,0],
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

ship_counter = 0

#=====Communication===============================================================================#
def rx(soc):  
    import ast
    data = []
    while True:
        rx_data_bytes = soc.recv(MAX_BUFFER_SIZE)
        rx_data = rx_data_bytes.decode("utf8").rstrip()
       
        if "--END--" in rx_data:                                # End of transfer
            return data
        else:
            try:
                rx_data = ast.literal_eval(rx_data)
            except:
                pass
            data.append(rx_data)
            soc.sendall("-".encode("utf8"))                     # Ready for another data

def tx(soc, data_type = NOTHING, data = []):
    tx_data = [data_type]
    tx_data.extend(data)
    
    for x in tx_data:
        msg = "{}\t".format(x)
        soc.sendall(msg.encode("utf8"))
        if soc.recv(MAX_BUFFER_SIZE).decode("utf8") == "-":     # Wait for response
            pass
    soc.send(b'--END--')
    
def process_data(conn, data = []):
    global shot_buffer
    
    # Try to pop data type
    try:
        data_type = data.pop(0)
    except:
        #tx(conn, MESSAGE, "Error")
        pass
    
    # Process data based od data_type
    if data_type == NOTHING:
        tx(conn, MESSAGE, [1])
    
    elif data_type == SHIP_LAYOUT:
        global enemy_grid_hidden
        enemy_grid_hidden = data
        if server_EN: 
            tx(conn, MESSAGE)
        
    elif data_type == SHIP_LAYOUT_REQUEST:
        tx(conn, SHIP_LAYOUT, my_grid)
    
    elif data_type == SHOT:
        try:
            destroy_ships(data[0], data[1], False)
        except:
            pass
        if server_EN:
            tx(conn, MESSAGE)
            
    elif data_type == SHOT_REQUEST:
        if shot_buffer == []:
            tx(conn, MESSAGE)
        else: 
            tx(conn, SHOT, shot_buffer)
            shot_buffer = []
            
    elif data_type == START_REQUEST:
        tx(conn, MESSAGE, [ready_status])
            
    elif data_type == MESSAGE:
        return data
    
    return 0
        
        
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
    global server_EN
    server_EN = True
    #print('Vase IP: ' + local_IP)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        soc.bind((local_IP, PORT))
    except socket.error as msg:
        import sys
        #print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()
    
    soc.listen(10)
    
    while server_EN:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            #print("Error!")
            import traceback
            traceback.print_exc()
    soc.close()


#_____Client______________________________________________________________________________________#
def client(server_ip, data_type = NOTHING, data = []):    
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    soc.settimeout(1000)
    try:
        soc.connect((server_ip, PORT))
    except:
        return("Error, connection failed!")
    soc.settimeout(None)
    
    tx(soc, data_type, data)
    response = rx(soc)
    response = process_data(soc, response)
    return(response)
    
def client_timer():
    if not your_turn:
        client(ip_adr, SHOT_REQUEST)
    Timer(0.5, client_timer).start()
    
    
#===GUI===========================================================================================#    
import tkinter as tk
from functools import partial

#____Windows options__________________________________________________________#
# Colors
bg_blue = "#3CAEE5"
menubuton_activebg = "#94A7B1"
menubuton_bg = "#BED5E1"
sea_blue = "#3496C5"
act_sea_blue = "#2380AC"
killed_red = "#8B1B1B"
u_missed = "#47A9D7"

# Window
window = tk.Tk()

# Window Title
window.title("Lode")

# Window Size
wd_width = 800
wd_height = 600
wd_size =(str(wd_width),"x",str(wd_height))
window.geometry("".join(wd_size))
#_____________________________________________________________________________#

def place_ships(x,y):                   # Generate user ship layout
    global ship_counter
    global my_grid
    if my_grid[x][y] == 0 and ship_counter < ship_number:
        my_grid[x][y] = 1
        my_pole[x][y].configure(bg = "black")
        ship_counter += 1
    
    elif my_grid[x][y] == 1 and ship_counter > 0:
        my_grid[x][y] = 0
        my_pole[x][y].configure(bg = sea_blue)
        ship_counter -= 1
    
def destroy_ships(x, y, enemy = True):  # Placen't ships 
    global enemy_grid
    global my_grid
    global ship_counter
    global shot_buffer
    global your_turn
    colors = [u_missed, killed_red]
    
    if shot_buffer == []:                               # Only if ship buffer is empty
        if enemy and your_turn:
            visible_grid = enemy_grid
            hidden_grid = enemy_grid_hidden
            pole = enemy_pole
            # Hold data in buffer or send it to server
            if server_EN:
                shot_buffer = [x, y]
            else:
                client(ip_adr, SHOT, [x, y])
        else:
            visible_grid = my_grid
            hidden_grid = my_grid
            pole = my_pole
            
        if (enemy and your_turn) or not enemy:
            h = hidden_grid[x][y]                       # handler
            
            if h and (not enemy) and (ship_counter > 0):
                ship_counter -= 1
                print("Ships remaining:" + str(ship_counter))
                if ship_counter == 0:
                    print("You Lose")
            
            your_turn = not (enemy ^ h)                 # XNOR function, calculate if you on turn
            pole[x][y].configure(bg = colors[h], state = "disabled")    # Update button state
            visible_grid[x][y] = h + 2                  # Update ship table (grid)
        

#_____generate buton grid with function in them_______________________________#
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

#_____________________________________________________________________________#
def button_grid_EN(pole, state = "disabled"):
    for x in pole:
        for y in x:
            y.configure(state = state)

def killer(widgets):                #Function for killing buttons
    for i in widgets:
        i.destroy()
        
def ip_get(entry, status_field):    #Get IP from text field
    global ip_adr
    global connection_status
    
    ip_adr = entry.get()            # Read text field
    
    response = client(ip_adr)    
    if response == [1]:             #Check connection
        connection_status = "Connected"
        text_color = "lime"
    else:
        connection_status = response
        text_color = "red"
        
    status_field.configure(fg = text_color, text = connection_status)
    
#_____Main menu_______________________________________________________________#
def main_menu(widgets = []):
    global server_EN
    global your_turn
    global ready
    
    server_EN = False
    your_turn = False
    ready = 0
    
    try:
        for row in my_pole:
            for i in row:
                i.destroy()
    except:
        pass
    
    killer(widgets)
    
    window.configure(background = bg_blue)
    
    widgets = []
    
    title = tk.Label(window,
                     text = "LODĚ",
                     font =("Arial Black",50),
                     bg = bg_blue,
                     fg = "white"
                     )
    title.pack()
    
    
    labels = ["Host", "Join"]
    commands = [host_wd, join_wd]
    
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
    global your_turn
    
    mode = "SERVER"
    your_turn = False
    killer(widgets)
    
    local_IP = get_local_IP()
    Thread(target=start_server, args=(local_IP,)).start()
    
    window.configure(background = bg_blue)
    
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
    
    back = tk.Button(window,
                       text = "Back",
                       font =("Arial Black",10),
                       bd  = 0,
                       fg = "white",
                       bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(main_menu, widgets))
    
    back.place(x = 0,
               y = wd_height - 25
               )
    
    widgets.append(back)

#_____Join window_____________________________________________________________#
def join_wd(widgets):
    global ip_adr
    global mode
    global your_turn
    
    mode = "CLIENT"
    your_turn = True
    killer(widgets)
    
    state = tk.Label(window, text = connection_status, font =("Arial Black",12),
                 bg = bg_blue, fg = "white")
    state.place(x = 0, y = 30)
    widgets.append(state)
    
    ip_label = tk.Label(window,
                     text = "Connect to:",
                     font =("Arial Black",10),
                     bg = bg_blue,
                     fg = "white"
                     )
    ip_label.grid(row = 0, column = 0)
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
                       command = partial(ip_get,ip, widgets[widgets.index(state)])
                       )
    confirm.grid(row = 0, column = 2,)
    widgets.append(confirm)
    
    ip_label = tk.Label(window,
                     text = "Connect to:",
                     font =("Arial Black",10),
                     bg = bg_blue,
                     fg = "white"
                     )
    ip_label.grid(row = 0, column = 0)
    widgets.append(ip_label)
    
    start = tk.Button(window,
                      text = "Start",
                      font =("Arial Black",30),
                      bd  = 0,
                      fg = "white",
                      bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(place_wd, widgets))
    start.place(x = (wd_width/2)-100,
                y = (wd_height/3),
                width = 200,
                height = 75)
    widgets.append(start)
    
    back = tk.Button(window,
                       text = "Back",
                       font =("Arial Black",10),
                       bd  = 0,
                       fg = "white",
                       bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(main_menu, widgets))
    back.place(x = 0, y = wd_height - 25)
    widgets.append(back)
    
#_____Place ships_____________________________________________________________#
def place_wd(widgets):
    if mode == "CLIENT" and not(connection_status == "Connected"):
        return
    
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
    
    game_status =  tk.Label(window,
                     text = "",
                     font =("Arial Black",16),
                     bg = bg_blue,
                     fg = "red"
                     )
    game_status.place(x = 550, y = ((wd_height/3) + 80))
    widgets.append(game_status)
    
    done = tk.Button(window,
                      text = "Done",
                      font =("Arial Black",30),
                      bd  = 0,
                      fg = "white",
                      bg = sea_blue,
                       activebackground = act_sea_blue,
                       command = partial(game_start, widgets, widgets[widgets.index(game_status)]))
    done.place (x = 550,
                y = (wd_height/3),
                width = 200,
                height = 75)
    widgets.append(done)


def game_start(widgets, game_status):
    global ready_status
    
    if ship_counter < ship_number:
        game_status.configure(text = "Not enough ships ♥")
        return
        
    if mode == "CLIENT":
        response = client(ip_adr, START_REQUEST)        # Wait for server
        if response == [0]:
            game_status.configure(text = "Server is not ready")
            return
        
        client(ip_adr, SHIP_LAYOUT, my_grid)
        client(ip_adr, SHIP_LAYOUT_REQUEST)
        client_timer()
        
    ready_status = 1
    game_wd(widgets)
        

#_____Game Window_____________________________________________________________#
def game_wd(widgets):
    killer(widgets)
    button_grid_EN(my_pole, "disabled")
    
    wd_width = 1150
    wd_height = 600
    wd_size =(str(wd_width),"x",str(wd_height))
    window.geometry("".join(wd_size))
    
    title = tk.Label(window,
                     text = "Your ships                         Enemy ships:",
                     font =("Arial Black",30),
                     bg = bg_blue,
                     fg = "white"
                     )
    
    title.pack()

    widgets.append(title)
    
    button_grid(destroy_ships,tile_x = 600,tile_y = 65, pole = enemy_pole)

#_____Main____________________________________________________________________#
main_menu()
window.mainloop()