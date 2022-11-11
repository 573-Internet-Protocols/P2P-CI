
# # create an INET, STREAMing socket
# import socket

# serverName = 'servername'
# serverPort = 7734
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientSocket.connect(('127.0.0.1', serverPort))
# # sentence = raw_input(‘Input lowercase sentence: ’)
# # clientSocket.send(sentence)
# # modifiedSentence = clientSocket.recv(1024)
# # print ‘From Server: ’, modifiedSentence
# clientSocket.close()

# Import socket module
import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
port = 7734

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# Send data to server 'Hello world'
peer_name = input("enter peer name")
upload_port = input("enter unload port")

## s.sendall('Hello World')
y = ["join", peer_name, upload_port, "123456", "Internet classification"]
input_string = str(y).encode()
s.send(input_string)

# receive data from the server
print(s.recv(1024).decode())

# close the connection
s.close()
