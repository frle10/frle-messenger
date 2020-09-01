from tkinter import *
from tkinter.scrolledtext import *
from socket import *

#Widget Functions (button events and such)
def sendMessageButton (event):
    message = type_message.get("1.0", END)
    if message != "" and message != "\n":
        msg_history.config(state = NORMAL)
        msg_history.insert(END, "Me: " + message + "\n")
        msg_history.see(END)
        msg_history.config(state = DISABLED)
        type_message.delete("1.0", END)
    return "break"

def exitMessengerButton (event):
    mainWindow.destroy()
    return

def connectionButton (event):
    connectionWindow = Toplevel()
    connectionWindow.title("Port configuration")
    portLabel = Label(connectionWindow, text = "Please enter the port number:")
    portLabel.pack()
    enterPort = Entry(connectionWindow)
    enterPort.pack()
    #okButton = Button(connectionWindow, command = connection(socket))
    #okButton.pack()
    closeButton = Button(connectionWindow, command = connectionWindow.destroy)
    closeButton.pack()
    connectionWindow.mainloop()

#Interconnection Functions
def connection (socket):
    host = gethostname()
    port = 12345
    socket.bind( (host, port) )
    socket.listen(5)
    while True:
        clientSocket, addr = socket.accept()
        print("Got a connection from:", addr)
        clientSocket.send(str.encode("Connection successful!"))
        clientSocket.close()
    socket.close()

#Main Window
mainWindow = Tk()

mainWindow.geometry("640x480+500+300")
mainWindow.resizable(False, False)
mainWindow.config(bg = "azure3")
mainWindow.title("Frle Messenger 0.3 Alpha")

#Frames
messages_frame = Frame(mainWindow, width = 439, height = 356)
type_message_frame = Frame(mainWindow, width = 381, height = 76)
options_frame = Frame(mainWindow, width = 160, height = 356)

messages_frame.grid(column = 2, row = 0, columnspan = 2, padx = 10, pady = 10)
messages_frame.grid_propagate(False)

type_message_frame.grid(column = 2, row = 1, padx = 10, pady = 10)
type_message_frame.grid_propagate(False)

options_frame.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

#Connect, Exit and Send Button
connectButton = Button(mainWindow, text = "Connect", font = "Arial", padx = 5, pady = 5, bg = "grey")
exitButton = Button(mainWindow, text = "Exit", font = "Arial", padx = 5, pady = 5, bg = "grey")
sendButton = Button(mainWindow, text = "Send", font = "Arial", padx = 5, pady = 5, bg = "grey")

connectButton.grid(column = 0, row = 1, padx = 5, pady = 5)
connectButton.bind("<Button>", connectionButton)

exitButton.grid(column = 1, row = 1, padx = 5, pady = 5)
exitButton.bind("<Button>", exitMessengerButton)

sendButton.grid(column = 3, row = 1, padx = 1, pady = 1)
sendButton.bind("<Button>", sendMessageButton)

#Scrolled Text Widgets for messages history and typing a new message
msg_history = ScrolledText(master = messages_frame, wrap = WORD, width = 38, height = 16, bg = "#F7F7F7")
type_message = ScrolledText(master = type_message_frame, wrap = WORD, width = 40, height = 4)

msg_history.grid(column = 0, row = 0)
msg_history.config(state = DISABLED, font = ("Arial", 14))

#Configuring message typing area
type_message.grid(column = 0, row = 0)
type_message.config(font = ("Arial", 12))
type_message.focus_set()
type_message.bind("<Return>", sendMessageButton)

socket = socket()

mainWindow.mainloop()
