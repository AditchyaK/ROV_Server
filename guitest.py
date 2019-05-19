import tkinter as tk
import socket

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.s, self.conn = ()
        self.pack()
        self.create_widgets(s, conn)

    def create_widgets(self, s, conn):
        self.master.title("Surface Server")
        self.serverStart = tk.Button(self)
        self.serverStart["text"] = "Start Server"
        self.serverStart["command"] = startServer(s, conn)
        self.serverStart.pack(side="top")
        self.clientclose = tk.Button(self, text="SHUTDOWN CLIENT", fg="red", command=self.master.destroy)
        self.clientclose.pack(side="bottom")

    def say_hi(self):
        print("Hello World!")

    def startServer(self, s, conn):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(('', port))
            print("Socket has successfully binded to port ", port)
        except socket.error as msg:
            print(msg)
        
        s.listen(1)
        conn, addr = s.accept()
        print("Connected to ", addr[0], ":" + str(addr[1]))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
