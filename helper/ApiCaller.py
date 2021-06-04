from json.encoder import JSONEncoder
from rsa.key import PrivateKey, PublicKey
from model.Key import Key
import os
import json
import requests
from helper import const
import rsa


class APICaller:

    @staticmethod
    def createNewFiles(mode: str):

        if mode == const.CLIENT_MODE:
            filenamePrv = const.KEY_PRV_FILE_NAME
            filePrv = const.KEY_PATH_CLIENT + filenamePrv

            filenamePub = const.KEY_PUB_FILE_NAME
            filePub = const.KEY_PATH_CLIENT + filenamePub

            if os.path.exists(filePrv):
                os.remove(filePrv)
                f = open(filePrv, "x")
                f.close()

            if not os.path.exists(const.KEY_PATH_CLIENT):
                os.mkdir(const.KEY_PATH_CLIENT)
                f = open(filePrv, "x")
                f.close()

            if os.path.exists(filePub):
                os.remove(filePub)
                f = open(filePub, "x")
                f.close()

            if not os.path.exists(const.KEY_PATH_CLIENT):
                os.mkdir(const.KEY_PATH_CLIENT)
                f = open(filePub, "x")
                f.close()

        if mode == const.SERVER_MODE:
            filenamePrv = const.KEY_PRV_FILE_NAME
            filePrv = const.KEY_PATH_SERVER + filenamePrv

            filenamePub = const.KEY_PUB_FILE_NAME
            filePub = const.KEY_PATH_SERVER + filenamePub

            if os.path.exists(filePrv):
                os.remove(filePrv)
                f = open(filePrv, "x")
                f.close()

            if not os.path.exists(const.KEY_PATH_SERVER):
                os.mkdir(const.KEY_PATH_SERVER)
                f = open(filePrv, "x")
                f.close()

            if os.path.exists(filePub):
                os.remove(filePub)
                f = open(filePub, "x")
                f.close()

            if not os.path.exists(const.KEY_PATH_SERVER):
                os.mkdir(const.KEY_PATH_SERVER)
                f = open(filePub, "x")
                f.close()

    @staticmethod
    def createNewKey(name: str, mode: str):

        APICaller.createNewFiles(mode)

        if mode == const.CLIENT_MODE:
            filenamePrv = const.KEY_PRV_FILE_NAME
            filePrv = const.KEY_PATH_CLIENT + filenamePrv

            filenamePub = const.KEY_PUB_FILE_NAME
            filePub = const.KEY_PATH_CLIENT + filenamePub

        if mode == const.SERVER_MODE:
            filenamePrv = const.KEY_PRV_FILE_NAME
            filePrv = const.KEY_PATH_SERVER + filenamePrv

            filenamePub = const.KEY_PUB_FILE_NAME
            filePub = const.KEY_PATH_SERVER + filenamePub

        (PubKey, PrivKey) = rsa.newkeys(const.RAS_LENGTH)

        f = open(filePrv, 'w')
        f.write(PrivKey.save_pkcs1().decode('utf-8'))
        f.close()

        f = open(filePub, 'w')
        f.write(PubKey.save_pkcs1().decode('utf-8'))
        f.close()

        data = {
            'id': name,
            'pubKey': PubKey.save_pkcs1().decode('utf-8')
        }

        requestUrl = 'http://' + const.KEY_SERVER + ':' + str(const.KEY_SERVER_PORT) + const.KEY_CREATE_NEW_KEY

        requests.post(requestUrl, json=data)

    @staticmethod
    def getPrvKey(mode):

        if mode == const.CLIENT_MODE:
            filename = const.KEY_PRV_FILE_NAME
            file = const.KEY_PATH_CLIENT + filename

        if mode == const.SERVER_MODE:
            filename = const.KEY_PRV_FILE_NAME
            file = const.KEY_PATH_SERVER + filename

        f = open(file, 'r')
        key = f.read()

        return key

    @staticmethod
    def getServerKey():
        nameparts = const.HOST.split('.')
        hostName = '_'.join(nameparts)
        params = {
            'id': hostName
        }

        requestUrl: str = 'http://' + const.KEY_SERVER + ':' + str(const.KEY_SERVER_PORT) + const.KEY_GET_A_KEY

        key = requests.get(url=requestUrl, params=params)

        data: Key = json.loads(key.content)

        return data['pubKey']

    @staticmethod
    def getClientKey(name: str):
        params = {
            'id': name
        }

        requestUrl: str = 'http://' + const.KEY_SERVER + ':' + \
                          str(const.KEY_SERVER_PORT) + const.KEY_GET_A_KEY

        key = requests.get(requestUrl, params=params)

        data = json.loads(key.content)

        return data['pubKey']

    @staticmethod
    def encryptData(data, mode: str, name: str):

        if mode == const.SERVER_MODE:
            key = APICaller.getClientKey(name)
            result = rsa.encrypt(data, rsa.PublicKey.load_pkcs1(key))

        if mode == const.CLIENT_MODE:
            key = APICaller.getServerKey()
            result = rsa.encrypt(data, rsa.PublicKey.load_pkcs1(key))

        return result

    @staticmethod
    def decryptData(data: bytes, mode: str):

        key = APICaller.getPrvKey(mode)
        result = rsa.decrypt(data, rsa.PrivateKey.load_pkcs1(key))

        return result
