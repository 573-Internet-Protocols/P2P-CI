import socket
import pickle

# import thread module
from _thread import *
import threading

active_peers = []
rfc_index = []
print_lock = threading.Lock()


def threaded(c):
    while True:

        # data received from client
        data = c.recv(4096)
        data = data.decode('utf-8')
        data = eval(data)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        print("action: ", data[0])
        print("peer name: ", data[1])
        print("upload port: ", data[2])
        print("rfc #: ", data[3])
        print("rfc titile: ", data[4])

    # connection closed
    c.close()


# create server socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")
port = 7734
s.bind(('', port))
print("socket binded to", port)
# put the socket into listening mode
s.listen(5)
print("socket is listening")

while True:

    # Establish connection with client.
    c, addr = s.accept()

    print_lock.acquire()
    print('Got connection from', addr)
    start_new_thread(threaded, (c,))

    # Close the connection with the client
    # c.close()


# def client_join(data, c):


class ActivePeer:
    def _init_(self, peer_name, upload_port):
        self.peer_name = peer_name
        self.upload_port = upload_port


class RFCIndex:
    def _init_(self, rfc_number, rfc_titile, peer_name):
        self.rfc_number = rfc_number
        self.rfc_titile = rfc_titile
        self.peer_name = peer_name
