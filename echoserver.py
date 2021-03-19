import socket
from helper import MessageParser
from helper import Style
from helper import const
import threading

HOST = const.HOST
PORT = const.PORT


def on_new_client(client_socket: socket.socket, address, global_socket: socket.socket):
    print('Connected by ', address)
    while True:
        msg = client_socket.recv(1024)
        if not msg:
            break
        m = MessageParser.byte_array_to_message(msg)
        print(Style.print_message(m))
        global_socket.sendall(msg)
    client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, address = s.accept()
        threading.Thread(target=on_new_client, args=(conn, address, s))
