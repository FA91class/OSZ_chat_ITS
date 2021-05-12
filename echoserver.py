import socket
from model import Message
from model import Session
from helper import MessageParser
from helper import Style
from helper import const
from helper import Logger
from helper.ApiCaller import APICaller
from typing import cast
import threading

HOST = const.HOST
PORT = const.PORT
MODE = const.CLIENT_MODE

SESSION = Session.Session()


def on_new_client(client_socket: socket.socket, addr):
    connect = 'Connected by ' + str(addr)
    print(connect)
    try:
        while True:
            APICaller.checkKeys(const.SERVER_MODE)
            msg = client_socket.recv(1024)
            if not msg:
                break
            m: Message.Message = MessageParser.bytes_to_message(
                APICaller.decryptData(msg, const.SERVER_MODE))
            if "LOGOUT" in m.msg:
                SESSION.socket_list.remove(client_socket)
                m.msg = Style.logout_message(m)
                Logger.log_message(m)
                msg = MessageParser.message_to_bytes(m)
                SESSION.broadcast_message(APICaller.encryptData(
                    msg, const.CLIENT_MODE, m.sender), client_socket)
                print(m.msg)
                client_socket.close()
                break
            if "LOGIN" in m.msg:
                m.msg = Style.login_message(m)
                Logger.log_message(m)
                msg = MessageParser.message_to_bytes(m)
                SESSION.socket_list.append(client_socket)
                SESSION.broadcast_message(APICaller.encryptData(
                    msg, const.CLIENT_MODE, m.sender), client_socket)
                continue
            else:
                m.msg = Style.print_message(m)
                Logger.log_message(m)
                msg = MessageParser.message_to_bytes(m)
                SESSION.broadcast_message(APICaller.encryptData(
                    msg, const.CLIENT_MODE, m.sender), cast(socket.socket, None))
        client_socket.close()
    except (ConnectionAbortedError, ConnectionResetError):
        close = "Connection with " + str(addr) + " closed!"
        print(close)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    nameparts = const.HOST.split('.')
    hostName = '_'.join(nameparts)
    APICaller.createNewKey(hostName, const.SERVER_MODE)

    while True:
        conn, address = s.accept()

        thread = threading.Thread(target=on_new_client, args=(conn, address))
        thread.start()
