import socket, sys, xbox, time

#port number is defined
port = 5558

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
        time.sleep(5)
    else:
        conn.sendall(str.encode(data))
        
    #tempData = s.recv(1024)
    #temPData = tempData.decode('utf-6')
    #print(tempData)
    time.sleep(1/30)

#everything is cleaned up after breaking the main loop
s.close()
print("Server is shutting down...")
sys.exit()
