import socket
from model import Message
from model import Session
from helper import MessageParser
from helper import Style
from helper import const
import threading

HOST = const.HOST
PORT = const.PORT

SESSION = Session.Session()

def on_new_client(client_socket: socket.socket, address):
    print('Connected by ', address)
    try:
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            m: Message.Message = MessageParser.byte_array_to_message(msg)
            if "LOGOUT" in m.msg:
                m.msg = Style.logout_message(m)
                msg = MessageParser.message_to_byte_array(m)
                client_socket.sendall(msg)
                client_socket.close()
            if "LOGIN" in m.msg:
                m.msg = Style.login_message(m)
                msg = MessageParser.message_to_byte_array(m)
            else:
                m.msg = Style.print_message(m)
                msg = MessageParser.message_to_byte_array(m)
            client_socket.sendall(msg)
        client_socket.close()
    except (ConnectionAbortedError, ConnectionResetError):
        print("Connection with " + str(address) + " closed!")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, address = s.accept()

        thread = threading.Thread(target=on_new_client, args=(conn, address))
        thread.start()
