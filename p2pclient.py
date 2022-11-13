
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
import os
import glob

server_name = '127.0.0.1'
server_port = 7734


def get_local_rfc():
    dir_path = r'/Users/zijunlu/CSC573/Project/P2P-CI/*.txt'
    files = glob.glob(dir_path, recursive=True)

    res = [i.split('/')[6].rstrip('.txt') for i in files]
    title = [str.split('_')[0] for str in res]
    rfc_number = [str.split('_')[1][3:] for str in res]

    return title, rfc_number


def format_msg_p2p(method, rfc_number, host_name):
    if (method == 'GET'):
        msg = "GET RFC " + rfc_number + " P2P-CI/1.0\r\n" + \
            "Host: " + host_name + "\r\n" + "OS: Mac OS 10.4.1\r\n\r\n"
    else:
        msg = "Method type is invalid."
    return msg


def format_msg_p2s(method, title, rfc_number, host_name, upload_port):
    if (method == 'ADD'):
        msg = "ADD RFC " + rfc_number + " P2P-CI/1.0\r\n" + \
            "Host: " + host_name + "\r\n" + "Port: " + \
            upload_port + "\r\n" "Title: " + title + "\r\n\r\n"
    else:
        msg = "Method type is invalid."
    return msg


def transmit(msg, client_socket):
    client_socket.sendall(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode()
    print("Request Response from the Server: ")
    print(response)


def sync_rfc(client_socket):
    title, rfc_number = get_local_rfc()
    for (t, n) in zip(title, rfc_number):
        print(t)
        msg = format_msg_p2s("ADD", t, n, "Zijun", "123")
        transmit(msg, client_socket)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    sync_rfc(client_socket)
# print(res)
# # Create a socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Define the port on which you want to connect
# port = 7734

# # connect to the server on local computer
# s.connect(('127.0.0.1', port))

# # Send data to server 'Hello world'
# peer_name = input("enter peer name")
# upload_port = input("enter unload port")

# ## s.sendall('Hello World')
# y = ["join", peer_name, upload_port, "123456", "Internet classification"]
# input_string = str(y).encode()
# s.send(input_string)

# # receive data from the server
# print(s.recv(1024).decode())


# # close the connection
# s.close()
main()
