# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:34:02 2018

@author: Kuba
"""

import socket


#_____Server_________________________________________________________________#
def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    import sys
    siz = sys.getsizeof(input_from_client_bytes)
    if  siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()
    res = main(input_from_client)
    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client
    conn.close()
    print('Connection ' + ip + ':' + port + " ended")

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

    # for handling task in separate jobs we need threading
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



#_____Client_________________________________________________________________#
def start_client(server_ip):
    while True:    
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        
        try:
            soc.connect((server_ip, 666))
        except:
            print("Error, nespravna IP!")
            break
    
        clients_input = input("Zprava pro server: ")
        
        try:
            soc.send(clients_input.encode("utf8"))
        except:
            print("Pada server, neco si prej...")
            break
        
        respone = soc.recv(4096)                    # max message size
        result_string = respone.decode("utf8")
        print("Odpoved od serveru:" + result_string)

#_____Main____________________________________________________________________#

def main(input_string = "xxx"):  
    
    output_string = input("Zprava pro klienta> ")
    
    return output_string



mode = input("Server, nebo klient> ")

if(mode == "server"):
    start_server()
    
else:
    while True:
        server_ip = input("Zadejte IP serveru> ")
        start_client(server_ip)



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
    