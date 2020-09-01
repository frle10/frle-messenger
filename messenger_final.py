from tkinter import *
from tkinter.scrolledtext import *
from socket import *
import threading

def setMasterFlag (flag):
    global masterFlag
    masterFlag = flag

def connectToClient (IP, username):
    global receiver, host, port
    try:
        receiver.settimeout(1)
        receiver.connect( (IP, port) )
    except:
        print("Error. Can't connect to:", IP, "on port:", port)

def sendMessageToClient (message):
    global clientSocket
    try:
        clientSocket.send(str.encode(message))
    except:
        pass

def closeSockets():
    global sender
    dummy = socket()
    dummy.connect( (gethostname(), 12345) )
    sender.close()
    
class Gui(threading.Thread):
    def __init__ (self):
        self.username = "Guest"
        self.IP = "127.0.0.1"
        threading.Thread.__init__(self)

    def showMessage (self, clientMessage, clientName):
        self.msg_history.config(state = NORMAL)
        self.msg_history.insert(END, clientName + ": " + clientMessage.decode() + "\n")
        self.msg_history.see(END)
        self.msg_history.config(state = DISABLED)

    #Widget Functions (button events and such)
    def sendMessageButton (self, event):
        self.message = self.type_message.get("1.0", END)
        if self.message != "" and self.message != "\n":
            sendMessageToClient(self.message)
            self.msg_history.config(state = NORMAL)
            self.msg_history.insert(END, "Me: " + self.message + "\n")
            self.msg_history.see(END)
            self.msg_history.config(state = DISABLED)
            self.type_message.delete("1.0", END)
        return "break"

    def exitMessengerButton (self, event):
        setMasterFlag(False)
        self.mainWindow.destroy()
        closeSockets()
        return

    def connectionButton (self, event):
        self.connectionWindow = Toplevel()
        self.connectionWindow.geometry("320x200+620+450")
        self.connectionWindow.title("Connection Configuration")
        self.userNameLabel = Label(self.connectionWindow, text = "Please enter your username:", padx = 5, pady = 5)
        self.userNameLabel.pack()
        self.enterUserName = Entry(self.connectionWindow)
        self.enterUserName.pack()
        self.enterUserName.focus_set()
        self.changeButton = Button(self.connectionWindow, text = "Set", padx = 5, pady = 5, command = self.setUserName)
        self.changeButton.pack()
        self.IPLabel = Label(self.connectionWindow, text = "Please enter the target IP address:", padx = 5, pady = 5)
        self.IPLabel.pack()
        self.enterTargetIP = Entry(self.connectionWindow)
        self.enterTargetIP.pack()
        self.connectToIP = Button(self.connectionWindow, text = "Connect", padx = 5, pady = 5, command = self.setIP)
        self.connectToIP.pack()
        self.closeButton = Button(self.connectionWindow, text = "Cancel", padx = 5, pady = 5, command = self.connectionWindow.destroy)
        self.closeButton.pack()
        self.connectionWindow.mainloop()

    def setUserName (self):
        if self.enterUserName.get() != "":
            self.username = self.enterUserName.get()
            print("Username set to:", self.username)
        else:
            pass

    def setIP (self):
        if self.enterTargetIP.get() != "":
            self.IP = self.enterTargetIP.get()
            print("Target IP set to:", self.IP)
            connectToClient(self.IP, self.username)
        else:
            pass
        
    def run(self):
        #Main Window
        self.mainWindow = Tk()
        self.mainWindow.geometry("640x480+500+300")
        self.mainWindow.resizable(False, False)
        self.mainWindow.config(bg = "azure3")
        self.mainWindow.title("Frle Messenger 0.99 Beta")

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

masterFlag = True

receiver = socket()
sender = socket()
clientSocket = socket()

host = gethostname()
port = 12345
data = ""
peerName = "Client"

sender.bind( (host, port) )

sender.listen(5)

try:
    clientSocket, addr = sender.accept()
    print("Got a connection from:", addr)
except:
    pass

while masterFlag == True:
    try:
        data = receiver.recv(4096)
        if data != "":
            root.showMessage(data, peerName)
    except:
        pass

receiver.close()
sender.close()
clientSocket.close()
print("Program returned 0 and successfully shut down!")
