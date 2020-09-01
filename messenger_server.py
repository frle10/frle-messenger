from socket import *
from tkinter import *

mainWindow = Tk()

socket = socket()

host = gethostname()
port = 12345

socket.bind( (host, port) )

socket.listen(5)

msg = "Thank you for connecting! :)"

while True:
    clientSocket, addr = socket.accept()
    print("Got a connection from:", addr)
    clientSocket.send(str.encode(msg))
    clientSocket.close()

mainWindow.mainloop()
