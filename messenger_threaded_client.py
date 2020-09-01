from tkinter import *
from tkinter.scrolledtext import *
from socket import *
import threading

def setMasterFlag (flag):
    global masterFlag
    masterFlag = flag

def connectToClient ():
    global s, host, port
    try:
        s.connect( ("127.0.0.1", port) )
        print("Successfully connected to:", host)
    except s.Timeouterror:
        print("Error. Can't connect to client.")

def sendMessageToClient (message):
    global s
    s.send(str.encode(message))

class Gui(threading.Thread):
    def __init__ (self):
        self.port = 12345
        threading.Thread.__init__(self)

    def showMessage (self, clientMessage, hostName):
        self.msg_history.config(state = NORMAL)
        self.msg_history.insert(END, hostName + ": " + clientMessage.decode() + "\n")
        self.msg_history.see(END)
        self.msg_history.config(state = DISABLED)

    #Widget Functions (button events and such)
    def sendMessageButton (self, event):
        self.message = self.type_message.get("1.0", END)
        sendMessageToClient(self.message)
        if self.message != "" and self.message != "\n":
            self.msg_history.config(state = NORMAL)
            self.msg_history.insert(END, "Me: " + self.message + "\n")
            self.msg_history.see(END)
            self.msg_history.config(state = DISABLED)
            self.type_message.delete("1.0", END)
        return "break"

    def exitMessengerButton (self, event):
        setMasterFlag(False)
        self.mainWindow.destroy()
        return

    def connectionButton (self, event):
        connectToClient()
        self.connectionWindow = Toplevel()
        self.connectionWindow.geometry("200x100+620+450")
        self.connectionWindow.title("Port Configuration")
        self.portLabel = Label(self.connectionWindow, text = "Please enter the port number:")
        self.portLabel.pack()
        self.enterPort = Entry(self.connectionWindow)
        self.enterPort.pack()
        self.enterPort.focus_set()
        self.okButton = Button(self.connectionWindow, text = "Set", command = self.setPort)
        self.okButton.pack()
        self.closeButton = Button(self.connectionWindow, text = "Cancel", command = self.connectionWindow.destroy)
        self.closeButton.pack()
        self.connectionWindow.mainloop()

    def setPort (self):
        if self.enterPort.get() != "":
            self.port = int(self.enterPort.get())
            print("Port set to:", self.port)
        else:
            pass
        self.connectionWindow.destroy()
        
    def run(self):
        #Main Window
        self.mainWindow = Tk()
        self.mainWindow.geometry("640x480+500+300")
        self.mainWindow.resizable(False, False)
        self.mainWindow.config(bg = "azure3")
        self.mainWindow.title("Frle Messenger Client 0.9 Beta")

        #Frames
        self.messages_frame = Frame(self.mainWindow, width = 439, height = 356)
        self.type_message_frame = Frame(self.mainWindow, width = 381, height = 76)
        self.options_frame = Frame(self.mainWindow, width = 160, height = 356)

        self.messages_frame.grid(column = 2, row = 0, columnspan = 2, padx = 10, pady = 10)
        self.messages_frame.grid_propagate(False)

        self.type_message_frame.grid(column = 2, row = 1, padx = 10, pady = 10)
        self.type_message_frame.grid_propagate(False)

        self.options_frame.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

        #Connect, Exit and Send Button
        self.connectButton = Button(self.mainWindow, text = "Connect", font = "Arial", padx = 5, pady = 5, bg = "grey")
        self.exitButton = Button(self.mainWindow, text = "Exit", font = "Arial", padx = 5, pady = 5, bg = "grey")
        self.sendButton = Button(self.mainWindow, text = "Send", font = "Arial", padx = 5, pady = 5, bg = "grey")

        self.connectButton.grid(column = 0, row = 1, padx = 5, pady = 5)
        self.connectButton.bind("<Button>", self.connectionButton)

        self.exitButton.grid(column = 1, row = 1, padx = 5, pady = 5)
        self.exitButton.bind("<Button>", self.exitMessengerButton)

        self.sendButton.grid(column = 3, row = 1, padx = 1, pady = 1)
        self.sendButton.bind("<Button>", self.sendMessageButton)

        #Scrolled Text Widgets for messages history and typing a new message
        self.msg_history = ScrolledText(master = self.messages_frame, wrap = WORD, width = 38, height = 16, bg = "#F7F7F7")
        self.type_message = ScrolledText(master = self.type_message_frame, wrap = WORD, width = 40, height = 4)

        self.msg_history.grid(column = 0, row = 0)
        self.msg_history.config(state = DISABLED, font = ("Arial", 14))

        #Configuring message typing area
        self.type_message.grid(column = 0, row = 0)
        self.type_message.config(font = ("Arial", 12))
        self.type_message.focus_set()
        self.type_message.bind("<Return>", self.sendMessageButton)

        self.mainWindow.mainloop()

#Main
root = Gui()
root.start()

s = socket()
#clientSocket = 0

host = gethostname()
port = 12345
data = ""

#s.bind( (host, port) )

#s.listen(5)

masterFlag = True

s.connect( (host, port) )
print("Successfully connected to:", host)

while masterFlag == True:
    #clientSocket, addr = s.accept()
    #print("Got a connection from:", addr)
    try:
        data = s.recv(1024)
        if data != "":
            root.showMessage(data, host)
    except:
        pass

#clientSocket.close()
s.close()
print("Program returned 0 and successfully shut down!")
