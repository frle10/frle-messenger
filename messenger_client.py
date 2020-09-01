from socket import *

s = socket()

host = gethostname()
port = 12345

s.connect( (host, port) )
data = s.recv(1024)
print (data.decode())

s.close()
