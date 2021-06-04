import socket
import threading

from helper import Logger
from helper import MessageParser
from helper import Style
from helper import const
from helper.ApiCaller import APICaller
from model import Message
from model import Session
from model.Client import Client

HOST = const.HOST
PORT = const.PORT
MODE = const.CLIENT_MODE

SESSION = Session.Session()


def on_new_client(client_socket: socket.socket, addr):
    connect = 'Connected by ' + str(addr)
    print(connect)
    client: Client
    try:
        while True:

            msg = client_socket.recv(1024)
            if not msg:
                break
            m: Message.Message = MessageParser.bytes_to_message(
                APICaller.decryptData(msg, const.SERVER_MODE))

            client = Client(client_socket, m.sender)

            if "LOGOUT" in m.msg:
                try:
                    SESSION.client_list.remove(client)
                except ValueError as e:
                    continue
                m.msg = Style.logout_message(m)
                Logger.log_message(m)
                msg = MessageParser.message_to_bytes(m)
                SESSION.broadcast_message(msg, client)
                print(m.msg)
                client_socket.close()
                break
            if "LOGIN" in m.msg:
                m.msg = Style.login_message(m)
                Logger.log_message(m)
                msg = MessageParser.message_to_bytes(m)
                SESSION.client_list.append(client)
                SESSION.broadcast_message(msg, client)
                continue
            else:
                m.msg = Style.print_message(m)
                Logger.log_message(m)
                msg = MessageParser.message_to_bytes(m)
                SESSION.broadcast_message(msg, client)

    except (ConnectionAbortedError, ConnectionResetError):
        client_socket.close()
        close = "Connection with " + str(addr) + " closed!"
        print(close)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    nameparts = const.HOST.split('.')
    hostName = '_'.join(nameparts)
    APICaller.createNewKey(hostName, const.SERVER_MODE)
    print("Server has loaded!")

    while True:
        conn, address = s.accept()

        thread = threading.Thread(target=on_new_client, args=(conn, address))
        thread.start()
