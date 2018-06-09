import socket

def main(input):  
    """
    This is where all the processing happens.

    Let's just read the string backwards
    """
    return output


def client():
    while True:    
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        soc.connect(("10.0.0.35", 666))
    
        clients_input = main()
        soc.send(clients_input)
        respone = soc.recv(4096)                    # max message size
        result_string = respone.decode("utf8")