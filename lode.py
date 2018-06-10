# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:34:02 2018

@author: Kuba
"""

import socket

MAX_BUFFER_SIZE = 4096


#_____Server______________________________________________________________________________________#

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

#_________________________________________________________________________________________________#

def client_thread(conn, ip, port):
        my_array = rx(conn)
        tx(conn, ["Success", 1, 2, "nejaka data", "funguje to!"])
        print(my_array)
        print('Connection ' + ip + ':' + port + " ended")
        conn.close()

def start_server():
    local_IP = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
                if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
                s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
                socket.SOCK_DGRAM)]][0][1]]) if l][0][0])    
    
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
    
    from threading import Thread
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
def client(server_ip, data = []):    
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    try:
        soc.connect((server_ip, 666))
    except:
        return("Error, connection failed!")
    
    tx(soc, data)
    response = rx(soc)
    return(response)


#_____Main________________________________________________________________________________________#

mode = input("Server, nebo klient> ")

if mode == "server":
    start_server()
    
else:
    while True:
        server_ip = input("Zadejte IP serveru> ")
        response = client(server_ip)
        
        if "Error, connection failed!" in response:
            print(response)
        
        else:
            data = []
            while True:
                user_input = input(">")
                
                if "^" in user_input:
                    response = client(server_ip, data)
                    print(response)
                    data = []
                    
                else:
                    data.append(user_input)

# Vlastni hraci pole
my_array = []

# Hraci pole protivnika
enemy_array = []

# Inicializace hernich poli
for i in range(10):
    temp = []
    for j in range(10):
        temp.append(0)
    my_array.append(temp)
    enemy_array.append(temp)
    