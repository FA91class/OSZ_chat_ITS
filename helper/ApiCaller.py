from Crypto import PublicKey
from model.Key import Key
import os
import json
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from helper import const


class APICaller():

    def createNewFiles(mode):
        
        if mode == const.CLIENT_MODE:
            filenamePrv = const.KEY_PRV_FILE_NAME
            filePrv = const.KEY_PATH_CLIENT + filenamePrv

            filenamePub = const.KEY_PUB_FILE_NAME
            filePub = const.KEY_PATH_CLIENT + filenamePub

            if os.path.exists(filePrv):
                os.remove(filePrv)
                f = open(filePrv, "x")
                f.close

            if os.path.exists(const.KEY_PATH_CLIENT) == False:
                os.mkdir(const.KEY_PATH_CLIENT)
                f = open(filePrv, "x")
                f.close

            if os.path.exists(filePub):
                os.remove(filePub)
                f = open(filePub, "x")
                f.close

            if os.path.exists(const.KEY_PATH_CLIENT) == False:
                os.mkdir(const.KEY_PATH_CLIENT)
                f = open(filePub, "x")
                f.close

        if mode == const.SERVER_MODE:
            filenamePrv = const.KEY_PRV_FILE_NAME
            filePrv = const.KEY_PATH_SERVER + filenamePrv

            filenamePub = const.KEY_PUB_FILE_NAME
            filePub = const.KEY_PATH_SERVER + filenamePub

            if os.path.exists(filePrv):
                os.remove(filePrv)
                f = open(filePrv, "x")
                f.close

            if os.path.exists(const.KEY_PATH_SERVER) == False:
                os.mkdir(const.KEY_PATH_SERVER)
                f = open(filePrv, "x")
                f.close

            if os.path.exists(filePub):
                os.remove(filePub)
                f = open(filePub, "x")
                f.close

            if os.path.exists(const.KEY_PATH_SERVER) == False:
                os.mkdir(const.KEY_PATH_SERVER)
                f = open(filePub, "x")
                f.close
        
    def createNewKey(name, mode):

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

        key = RSA.generate(2048)

        PrivKey = key.exportKey('PEM')
        PubKey = key.publickey().exportKey('PEM')

        f = open(filePrv, 'wb')
        f.write(PrivKey)
        f.close()

        f = open(filePub, 'wb')
        f.write(PubKey)
        f.close()

        data = {
            'ID': name,
            'pubKey': str(PubKey)
        }

        requestUrl = 'https://' + const.KEY_SERVER + ':' + str(const.KEY_SERVER_PORT) + const.KEY_CREATE_NEW_KEY

        requests.post( requestUrl, json=data)

    def getKey(mode):

        if mode == const.CLIENT_MODE:
            filename = const.KEY_FILE_NAME
            file = const.KEY_PATH_CLIENT + filename

        if mode == const.SERVER_MODE:
            filename = const.KEY_FILE_NAME
            file = const.KEY_PATH_SERVER + filename

        f = open(file, 'r')
        key = RSA.import_key(f.read())

        return key

    def getServerKey():
        nameparts = const.HOST.split('.')
        hostName = '_'.join(nameparts)
        params = {
            'id': hostName
        }

        requestUrl:str = 'https://' + const.KEY_SERVER + ':' + str(const.KEY_SERVER_PORT) + const.KEY_GET_A_KEY

        key = requests.get(requestUrl, params=params)

        data: Key = json.loads(key)

        return data.pubKey

    def getClientKey(name: str):
        params = {
            'id': name
        }

        requestUrl: str = 'https://' + const.KEY_SERVER + ':' + \
            str(const.KEY_SERVER_PORT) + const.KEY_GET_A_KEY

        key = requests.get(requestUrl, params=params)

        data: Key = json.loads(key)

        return data.pubKey

    def encryptData(data, mode: str, name: str):

        if mode == const.SERVER_MODE:

            recipient_key = RSA.import_key(APICaller.getClientKey(name))
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            result = cipher_rsa.encrypt(data)

        if mode == const.CLIENT_MODE:

            recipient_key = RSA.import_key(APICaller.getServerKey())
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            result = cipher_rsa.encrypt(data)

        return result

    def decryptData(data, mode):

        recipient_key = APICaller.getKey(mode)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        result = cipher_rsa.decrypt(data)

        return result
