import socket

# import thread module
from _thread import *
import threading

active_peers = []
rfc_index = []


class ActivePeer:

    def __init__(self, peer_name, upload_port):
        self.peer_name = peer_name
        self.upload_port = upload_port

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.peer_name == other.peer_name and self.upload_port == other.upload_port
        return False


class RFCIndex:
    def __init__(self, rfc_number, rfc_title, peer_name):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.peer_name = peer_name

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.rfc_number == other.rfc_number and self.rfc_title == other.rfc_title and self.peer_name == other.peer_name
        return False


def threaded(client_socket):
    while True:
        # data received from client
        data = client_socket.recv(4096)
        data = data.decode('utf-8')
        if not data:
            print('Disconnection from', addr)
            print('Bye')
            break

        p2p_version = get_version(data)
        if (p2p_version != '1.0'):
            client_socket.send("505 P2P-CI Version Not Supported".encode())
            break

        method = get_method(data)
        if (method == "ADD"):
            add_rfc(data, client_socket)

        if (method == "LOOKUP"):
            lookup(data, client_socket)

        if (method == "LIST"):
            list_all(client_socket)

        if (method == "LEAVE"):
            leave(data, client_socket)

            # connection closed
    client_socket.close()


def get_method(data):
    return data.split(' ')[0]


def get_version(data):
    return data.split('\r')[0][-3:]


def add_rfc(data, client_socket):
    fields = data.split(' ')
    peer_name = fields[4].rstrip('\r\nPort:')
    upload_port = fields[5].rstrip('\r\nTitle:')
    rfc_number = fields[2]
    rfc_title = ' '.join(fields[6:])
    new_peer = ActivePeer(peer_name, upload_port)

    response = "P2P-CI/1.0 400 Bad Request\r\nRFC already exists under your registration\n"
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
    response = "P2P-CI/1.0 200 OK\r\n" + "RFC " + str(new_rfc.rfc_number) + " " + \
        str(new_rfc.rfc_title) + " " + str(new_rfc.peer_name) + \
        " " + str(new_peer.upload_port)
    return response


def lookup(data, client_socket):
    fields = data.split(' ')
    rfc_number = fields[2]
    rfc_title = ' '.join(fields[6:])

    list = []
    found = False
    for rfc in rfc_index:
        if (rfc.rfc_number == rfc_number and rfc.rfc_title == rfc_title):
            list.append(rfc.peer_name)
            found = True

    if (found):
        response = "P2P-CI/1.0 200 OK\n"
        for host in list:
            for peer in active_peers:
                if (host == peer.peer_name):
                    response += "RFC " + rfc_number + " " + rfc_title + \
                        " " + host + " " + peer.upload_port + "\n"
    else:
        response = "P2P-CI/1.0 404 Not Found\n"

    client_socket.send(response.encode('utf-8'))


def list_all(client_socket):
    if (len(rfc_index) == 0):
        response = "P2P-CI/1.0 404 Not Found\n"
    else:
        response = "P2P-CI/1.0 200 OK\n"
        for rfc in rfc_index:
            rfc_number = rfc.rfc_number
            rfc_title = rfc.rfc_title
            for peer in active_peers:
                if (str(rfc.peer_name) == str(peer.peer_name)):
                    response += "RFC " + rfc_number + " " + rfc_title + \
                        " " + str(peer.peer_name) + " " + \
                        str(peer.upload_port) + "\n"

    client_socket.send(response.encode('utf-8'))


def leave(data, client_socket):
    fields = data.split(' ')
    peer_name = fields[2].rstrip('\r\nPort:')
    upload_port = fields[3].rstrip('\r\nTitle:')
    print("Leaving peer is: ")
    print(peer_name)
    print("leaving peer's port is: ")
    print(upload_port)

    for peer in active_peers:
        if (peer.peer_name == peer_name):
            active_peers.remove(peer)
    for rfc in rfc_index:
        if (rfc.peer_name == peer_name):
            rfc_index.remove(rfc)

    response = "bye!"
    client_socket.send(response.encode('utf-8'))


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
    print('Got connection from', addr)
    client_thread = threading.Thread(target=threaded, args=(client_socket,))
    client_thread.start()
