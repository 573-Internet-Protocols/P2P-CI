import socket
import os
import glob
import datetime
import time
import platform
import threading
import sys

# server_name = '152.7.98.254'
server_name = '127.0.0.1'
server_port = 7734


def get_local_rfc():
    files = glob.glob('./*.txt')
    for i in files:
        print(i)
    res = [i.split('/')[1].rstrip('.txt') for i in files]
    title = [str.split('_')[0] for str in res]
    rfc_number = [str.split('_')[1][3:] for str in res]

    return title, rfc_number


def format_get_request(rfc_number, peer_name):

    msg = "GET RFC " + rfc_number + " P2P-CI/1.0\r\n" + \
        "Host: " + socket.gethostname() + "\r\n" + "OS: " + platform.platform()

    print(msg)
    return msg


def format_get_response(rfc_number, peer_name):
    filepath = ""
    date = str(datetime.datetime.now().strftime("%A, %d %b %Y %X %z"))
    local_os = platform.platform()
    txt_files = glob.glob('./*.txt')
    # To-do: make the date and last-modified format the same
    msg = "P2P-CI/1.0 404 Not Found\n"
    for file in txt_files:
        print("file directory txt:", file.split('_rfc')[1].rstrip('.txt'))
        if (file.split('_rfc')[1].rstrip('.txt') == rfc_number):
            content_length = os.path.getsize(file)
            last_modified = time.ctime(os.path.getmtime(file))
            msg = "P2P-CI/1.0 200 OK\r\n" + "Date: " + date + \
                "OS: " + local_os + "\n" + "Last-Modified: " + \
                str(last_modified) + "\n" + "Content-Length: " + \
                str(content_length) + "\n" + "Content-Type: text/text\n"
            filepath = file
            print(msg)

    return msg, filepath


def format_msg_p2s(method, rfc_number, title, host_name, upload_port):
    msg = ""
    print("method is :")
    print(method)
    if (method == 'ADD'):
        msg = "ADD RFC " + rfc_number + " P2P-CI/1.0\r\n" + \
            "Host: " + host_name + "\r\n" + "Port: " + \
            str(upload_port) + "\r\n" "Title: " + title
    elif (method == 'LOOKUP'):
        msg = "LOOKUP RFC " + rfc_number + " P2P-CI/1.0\r\n" + \
            "Host: " + host_name + "\r\n" + "Port: " + \
            str(upload_port) + "\r\n" "Title: " + title

    print(msg)
    return msg


def transmit(msg, client_socket):
    client_socket.sendall(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode()
    print("Request Response from the Server: ")
    print(response)


def sync_rfc(client_socket):
    title, rfc_number = get_local_rfc()
    for (t, n) in zip(title, rfc_number):
        msg = format_msg_p2s("ADD", n, t, socket.gethostname(), upload_port)
        print("Message sent: \n")
        transmit(msg, client_socket)


def lookup(client_socket):
    rfc_number = input("Please enter the #RFC you try to look up\n")
    title = input("Please enter the RFC title")
    msg = format_msg_p2s("LOOKUP", rfc_number, title,
                         socket.gethostname(), upload_port)
    transmit(msg, client_socket)


def list_all(client_socket):
    msg = "LIST ALL P2P-CI/1.0\r\n" + \
        "Host: " + socket.gethostname() + "\r\n" + "Port: " + \
        str(upload_port)
    transmit(msg, client_socket)


def user_interface():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    while (True):
        print("********************************************************")
        print("Welcome to P2P-CI system\n")
        print("Please enter the option which you like to proceed\n")
        print("Option 1: ADD\n")
        print("Option 2: LOOKUP\n")
        print("Option 3: LIST\n")
        print("Option 4: Download RFC\n")
        print("Option 5: Leave\n")
        option = input("Enter your option")
        print("********************************************************")
        if (option == "1"):
            sync_rfc(client_socket)
        elif (option == "2"):
            lookup(client_socket)
        elif (option == "3"):
            list_all(client_socket)
        elif (option == "4"):
            download_rfc()
        elif (option == "5"):
            leave(client_socket)
            break
        else:
            print("Invalid Input\n")
    print("End of program!")
    client_socket.close()
    return


def download_rfc():
    print("download rfc")
    port = input("Please enter the upload port")
    peer_host = input("Please enter the peer host address")
    title = input("Please enter rfc title")
    rfc_number = input("Please enter rfc number")
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_host, int(port)))
        # peer_socket.connect(('0.0.0.0', int(port)))
        msg = format_get_request(rfc_number, "peer_name")
        peer_socket.sendall(msg.encode('utf-8'))
        response = peer_socket.recv(1024).decode()
        print("look at the following response: ")
        print(response)
        file_size = int(response.split(' ')[-2].rstrip('\nContent-Type:'))
        file_size = file_size_helper(file_size)
        print("this is the file size: ")
        print(str(file_size))
        filename = title + "_" + "rfc"+rfc_number+".txt"
        file = open(filename, "w")
        data = peer_socket.recv(file_size).decode("utf-8")
        file.write(data)
        file.close()
        peer_socket.close()
        print("Request Response from the peer: ")
        print(response)
    except Exception as e:
        print(str(e))


def file_size_helper(num):
    if (num == 0):
        return 0
    temp = num
    msb = 0
    num = int(num / 2)
    while (num > 0):
        num = int(num / 2)
        msb += 1

    round_filesize = 1 << (msb + 1)
    msb_set = 1 << msb
    if (msb_set - temp == 0):
        file_size = temp
    else:
        file_size = round_filesize
    return file_size


def upload_server_process(upload_server):
    upload_server.listen(3)
    # Establish connection with peer
    while True:
        peer_socket, addr = upload_server.accept()
        print("Got a peer connection from :", addr)

        data = peer_socket.recv(1024).decode('utf-8')
        print(data)
        rfc_number = data.split(' ')[2]
        print("rfc number is ", rfc_number)
        response, filepath = format_get_response(rfc_number, "peer_name")
        peer_socket.send(response.encode('utf-8'))
        if (filepath != ""):
            upload_thread = threading.Thread(
                target=upload_file, args=(filepath, peer_socket,))
            upload_thread.start()
            upload_thread.join()

    upload_server.close()


def upload_file(filepath, peer_socket):
    print("read and sending file data\n")
    file = open(filepath, "r")
    data = file.read()
    peer_socket.send(data.encode("utf-8"))
    file.close()
    peer_socket.close()


def leave(client_socket):
    msg = "LEAVE " + "P2P-CI/1.0\r\n" + \
        "Host: " + socket.gethostname() + "\r\n" + "Port: " + \
        str(upload_port)
    transmit(msg, client_socket)


def main():
    global upload_port
    # hostname = socket.gethostname()
    # address = socket.gethostbyname(hostname)
    upload_port = input("Please enter an upload port between 29170 to 29998\n")

    try:
        upload_server = socket.socket()
        upload_server.bind(('0.0.0.0', int(upload_port)))
        peer_upload_thread = threading.Thread(target=upload_server_process,
                                              args=(upload_server,))
        peer_upload_thread.daemon = True
        peer_upload_thread.start()
        peer_server_thread = threading.Thread(target=user_interface)
        peer_server_thread.daemon = True
        peer_server_thread.start()
        peer_upload_thread.join()
        peer_server_thread.join()

    except KeyboardInterrupt:
        sys.exit(0)


main()
