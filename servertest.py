import socket, sys, xbox, time
from multiprocessing import Process

#port number is defined
port = 5558

#socket object is initialized
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket Successfully Created!")

    #socket connects the client(RPi) to the server
    try:
        s.bind(('', port))
        print("Socket has successfully binded to port ", port)
    except socket.error as msg:
        print(msg)
    return s

def setupConnection():
    s.listen(1)
    conn, addr = s.accept()
    print("Connected to ", addr[0], ":" + str(addr[1]))
    return conn

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

def stickCollect(data):
    data += "LX" + str(joy.leftX())
    data += "LY" + str(joy.leftY())
    data += "RX" + str(joy.rightX())
    data += "RY" + str(joy.rightY())
    return data

def trigCollect(data):
    data += "LT" + str(joy.leftTrigger())
    data += "RT" + str(joy.rightTrigger())
    data += "END"
    return data

#xbox joystick is set up here
try:
    joy = xbox.Joystick()
    print("Joystick successfully initialized!")
except:
    print("Joystick could not initialize.")
    sys.exit()

#actual start of the main program
s = setupSocket()
conn = setupConnection()

while True:
    data = ""
    if joy.Start():
        conn.send(str.encode("KILL"))
        time.sleep(1/2)
        conn.close()
        print("Connection was manually severed. Hold Start to shut down server.")
        time.sleep(1)
        if joy.Start():
            joy.close()
            break
        else: 
            time.sleep(1/2)
            if joy.Start():
                joy.close()
                break
            conn = setupConnection()
            
    time.sleep(1/4)
    data = buttonCollect(data)
    data = stickCollect(data)
    data = trigCollect(data)
    if not joy.connected():
        conn.sendall(str.encode("HOLD"))
    else:
        conn.sendall(str.encode(data))

s.close()
print("Server is shutting down...")
joy.close()
sys.exit()
