import socket, sys

#port number is defined
port = 5557

#socket object is initialized
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket Successfully Created!")

    #socket connects the client(RPi) to the server
    try:
        s.bind(('', port))
        print("Socket has successfully binded")
    except socket.error as msg:
        print(msg)
    return s

def setupConnection():
    s.listen(1)
    conn, addr = s.accept()
    print("Connected to ", addr[0], ":" + str(addr[1]))
    return conn

def transferData(conn, data):
    while True:
        conn.sendall(str.encode(data))

s = setupSocket()
while True:
    try:
        conn = setupConnection()
        transferData(conn, "Hello World!")
    except:
        break

conn.close()
s.close()
print("Server is shutting down...")
sys.exit()
