import xbox, time

joy = xbox.Joystick()
print("Joystick has initialized")

while True: 
    time.sleep(1/2)
    print(str(joy.rightX()))
