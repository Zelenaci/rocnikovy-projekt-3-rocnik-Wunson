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
        soc.send(clients_input.encode("utf8"))
        #soc.send(clients_input.encode("utf8")) # we must encode the string to bytes  
        result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
        result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode  