import socket
import pickle

# import thread module
from _thread import *
import threading

active_peers = []
rfc_index = []
print_lock = threading.Lock()


class ActivePeer:
    def __init__(self, peer_name, upload_port):
        self.peer_name = peer_name
        self.upload_port = upload_port


class RFCIndex:
    def __init__(self, rfc_number, rfc_titile, peer_name):
        self.rfc_number = rfc_number
        self.rfc_titile = rfc_titile
        self.peer_name = peer_name


def threaded(client_socket):
    while True:

        # data received from client
        data = client_socket.recv(4096)
        data = data.decode('utf-8')
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        p2p_version = get_version(data)
        if (p2p_version != 'P2P-CI/1.0'):
            client_socket.send("505 P2P-CI Version Not Supported".encode())
            print_lock.release()
            break

        method = get_method(data)
        if (method == "ADD"):
            add_rfc(data, client_socket)

        if (method == "LOOKUP"):
            print("To-do")
            # c.sendall(data.encode('utf-8'))

            # connection closed
    client_socket.close()


def get_method(data):
    return data.split(' ')[0]


def get_version(data):
    return data.split(' ')[3].rstrip('\r\nHost:')


def add_rfc(data, client_socket):
    fields = data.split(' ')
    peer_name = fields[4].rstrip('\r\nPort:')
    print(peer_name)
    upload_port = fields[5].rstrip('\r\nTitle:')
    print(upload_port)
    rfc_number = fields[2]
    print(rfc_number)
    rfc_title = ' '.join(fields[6:])
    print(rfc_title)

    new_peer = ActivePeer(peer_name, upload_port)
    if new_peer not in active_peers:
        active_peers.insert(0, new_peer)

    # For each RFC, the server creates an appropriate record and
    # inserts it at the front of the list
    new_rfc = RFCIndex(rfc_number, rfc_title, peer_name)
    if new_rfc not in rfc_index:
        rfc_index.insert(0, new_rfc)
        response = format_add_response(new_peer, new_rfc)
        client_socket.send(response.encode('utf-8'))


def format_add_response(new_peer, new_rfc):
    response = "P2P-CI/1.0 200 OK\r\n" + "RFC " + new_rfc.rfc_number + " " + \
        new_rfc.rfc_titile + " " + new_rfc.peer_name + " " + new_peer.upload_port
    return response

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
    client_socket, addr = s.accept()

    print_lock.acquire()
    print('Got connection from', addr)
    start_new_thread(threaded, (client_socket,))

    # Close the connection with the client
    # c.close()


# def client_join(data, c):
