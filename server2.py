import socket, sys, xbox, time
from threading import Thread
from SocketServer import ThreadingMixIn

#port number is defined
port = 5555

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
    s.listen(1)



def buttonCollect(data):
    if joy.A():
        data += "AB1"
    else:
        data += "AB0"
    if joy.B():
        data += "BB1"
    else:
        data += "BB0"
    if joy.X():
        data += "XB1"
    else:
        data += "XB0"
    if joy.Y():
        data += "YB1"
    else:
        data += "YB0"
    if joy.leftThumbstick():
        data += "LH1"
    else:
        data += "LH0"
    if joy.rightThumbstick():
        data += "RH1"
    else:
        data += "RH0"
    if joy.dpadUp():
        data += "DU1"
    else:
        data += "DU0"
    if joy.dpadDown():
        data += "DD1"
    else:
        data += "DD0"
    if joy.dpadLeft():
        data += "DL1"
    else:
        data += "DL0"
    if joy.dpadRight():
        data += "DR1"
    else:
        data += "DR0"
    if joy.leftBumper():
        data += "LB1"
    else:
        data += "LB0"
    if joy.rightBumper():
        data += "RB1"
    else:
        data += "RB0"
    return data

#input from the sticks are concanenated to a string (data)
def stickCollect(data):
    data += "LX" + str(joy.leftX())
    data += "LY" + str(joy.leftY())
    data += "RX" + str(joy.rightX())
    data += "RY" + str(joy.rightY())
    return data

#input from triggers is concatenated to a string (data)
def trigCollect(data):
    data += "LT" + str(joy.leftTrigger())
    data += "RT" + str(joy.rightTrigger())
    #the END must be concatenated to break the string at the other end
    data += "END"
    return data

def dataCollect(data, buttons):
    for i in range(len(buttons)):
        data += str(buttons[i]) + " "
    return data

#xbox joystick class is initilized
try:
    joy = xbox.Joystick()
    print("Joystick successfully initialized!")
except:
    print("Joystick could not initialize.")
    sys.exit()

#program starts here
s = setupSocket()
conn = setupConnection()

# Multithread python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port)")

    def run(self):
        while True:
            data = conn.recv(2048)

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 20 

while True:
    s.listen(2)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)
    threads = [2]

#server socket listens for a connection and accepts only one incoming request
def setupConnection():
    conn, addr = s.accept()
    print("Connected to ", addr[0], ":" + str(addr[1]))
    return conn

for t in threads:
    t.join()

#main loop for the program which sends the string which contains all the controller input
#to the client which must decode it properly
while True:
    #buttons = [joy.A(), joy.B(), joy.X(), joy.Y(), joy.leftThumbstick(), joy.rightThumbstick(), joy.dpadUp(), joy.dPadDown(), joy.dpadLeft(), joy.dpadRight(),
    #joy.leftBumper(), joy.rightBumper(), joy.leftX(), joy.leftY(), joy.rightX(), joy.rightY(), joy.leftTrigger(), joy.rightTrigger()]
    data = ""
    #shuts the client down remotely if Start and Back are pressed
    if joy.Start() & joy.Back():
        conn.send(str.encode("KILL"))
        time.sleep(1/2)
        conn.close()
        print("Connection was manually severed. Hold Start to shut down server.")
        time.sleep(2)
        #if Start and Back are held, the server shuts down too
        if joy.Start() & joy.Back():
            joy.close()
            break
        else: 
            conn = setupConnection()

    #data string is concatenated to include all data 
    data = buttonCollect(data)
    data = stickCollect(data)
    data = trigCollect(data)

    #sends HOLD command if controller is disconnected
    if not joy.connected():
        conn.sendall(str.encode("HOLD"))
        print("HOLD")
        time.sleep(5)
    else:
        conn.sendall(str.encode(data))
        
    
    time.sleep(1/30)

#everything is cleaned up after breaking the main loop
s.close()
print("Server is shutting down...")
sys.exit()
