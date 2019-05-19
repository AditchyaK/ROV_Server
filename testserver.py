import socket, time

#socket object is initialized
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket is set to reuse the current port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket Successfully Created!")

    #socket connects the client(RPi) to the server
    try:
        #socket binds to an ip address which is automatically assigned from a client that is connecting
        s.bind(('', port))
        print("Socket has successfully binded to port ", port)
    except socket.error as msg:
        print(msg)
    return s

#server socket listens for a connection and accepts only one incoming request
def setupConnection():
    s.listen(1)
    conn, addr = s.accept()
    print("Connected to ", addr[0], ":" + str(addr[1]))
    return conn

s = setupSocket()
conn = setupConnection()
