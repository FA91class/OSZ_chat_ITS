import socket
from model import Message
from model import Session
from helper import MessageParser
from helper import Style
from helper import const
from typing import cast
import threading

HOST = const.HOST
PORT = const.PORT

SESSION = Session.Session()


def on_new_client(client_socket: socket.socket, addr):
    print('Connected by ', addr)
    try:
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            m: Message.Message = MessageParser.bytes_to_message(msg)
            if "LOGOUT" in m.msg:
                SESSION.socket_list.remove(client_socket)
                m.msg = Style.logout_message(m)
                msg = MessageParser.message_to_byte_array(m)
                SESSION.broadcast_message(msg, client_socket)
                print(m.msg)
                client_socket.close()
                break
            if "LOGIN" in m.msg:
                m.msg = Style.login_message(m)
                msg = MessageParser.message_to_byte_array(m)
                SESSION.socket_list.append(client_socket)
                SESSION.broadcast_message(msg, client_socket)
            else:
                m.msg = Style.print_message(m)
                msg = MessageParser.message_to_byte_array(m)
            SESSION.broadcast_message(msg, cast(socket.socket, None))
        client_socket.close()
    except (ConnectionAbortedError, ConnectionResetError):
        print("Connection with " + str(addr) + " closed!")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, address = s.accept()

        thread = threading.Thread(target=on_new_client, args=(conn, address))
        thread.start()
