import socket, sys, xbox, time

#port number is defined
port = 5555

buttonKeys = ["AB", "BB", "XB", "YB", "LH", "RH", "DU", "DD", "DL", "DR", "LB", "RB", "LX", "LY", "RX", "RY", "LT", "RT"]

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

#this takes all the joystick data and concatenates it into a string with its 
def dataCollect(buttons, buttonKeys):
    data = ""
    for i in range(len(buttons)):
        data += buttonKeys[i] + str(buttons[i])
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
    #refreshes button values at the beginning of each loop
    buttons = [joy.A(), joy.B(), joy.X(), joy.Y(), joy.leftThumbstick(), joy.rightThumbstick(), joy.dpadUp(), joy.dpadDown(), joy.dpadLeft(), joy.dpadRight(),
joy.leftBumper(), joy.rightBumper(), joy.leftX(), joy.leftY(), joy.rightX(), joy.rightY(), joy.leftTrigger(), joy.rightTrigger()]

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

    data = dataCollect(buttons, buttonKeys)
    data += "END"

    #sends HOLD command if controller is disconnected
    if not joy.connected():
        conn.sendall(str.encode("HOLD"))
        time.sleep(5)
    else:
        conn.sendall(str.encode(data))

    tempData = conn.recv(1024)
    tempData = tempData.decode('utf-7')
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nTemperature:\t", tempData)
        
    
    time.sleep(1/30)

#everything is cleaned up after breaking the main loop
s.close()
print("Server is shutting down...")
sys.exit()
