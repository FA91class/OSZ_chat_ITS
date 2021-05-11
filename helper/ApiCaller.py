import os
import json
import requests
import rsa
from helper import const
from model import Keys


class APICaller():

    def checkKeys(mode, *name):
        filename = "keys.json"
        file = const.KEY_PATH + filename

        if os.path.exists(const.KEY_PATH) == False:
            os.mkdir(const.KEY_PATH)
            f = open(file, "x")
            f.close

        if os.path.isfile(file) == False:
            f = open(file, "x")
            f.close

            if mode == 'client':
                keys = APICaller.createNewKey(name)
                f = open(file, "w")
                f.write(keys)
                f.close
            if mode == 'server':
                nameparts = const.HOST.split('.')
                hostName = '_'.join(nameparts)
                keys = APICaller.createNewKey(hostName)
                f = open(file, "w")
                f.write(keys)
                f.close

    def createNewKey(name):

        (pubkey, privkey) = rsa.newkeys(4096)

        params = Keys(name, privkey, pubkey)

        data = json.dumps(params)

        requests.post('https://' + const.KEY_SERVER + ':' +
                      const.KEY_SERVER_PORT + const.KEY_CREATE_NEW_KEY, json=data)

        return params

    def getKey(mode):

        filename = "keys.json"
        file = const.KEY_PATH + filename

        f = open(file, "r")
        content = json.loads(f.read().strip())

        if mode == 'public':

            return content.pub

        if mode == 'private':

            return content.prv

    def getServerKey():
        nameparts = const.HOST.split('.')
        hostName = '_'.join(nameparts)
        params = {
            'id': hostName
        }

        key = requests.get('https://' + const.KEY_SERVER +
                           ':' + const.KEY_SERVER_PORT, params=params)

        return key

    def getClientKey(name: str):
        params = {
            'id': name
        }

        key = requests.get('https://' + const.KEY_SERVER +
                           ':' + const.KEY_SERVER_PORT, params=params)

        return key

    def encryptData(data, mode: str, name: str):

        if mode == const.CLIENT_MODE:
            result = rsa.encrypt(data, APICaller.getClientKey(name))

        if mode == const.SERVER_MODE:
            result = rsa.encrypt(data, APICaller.getServerKey())

        return result

    def decryptData(data, mode: str, name: str):

        if mode == const.CLIENT_MODE:
            result = rsa.decrypt(data, APICaller.getClientKey(name))

        if mode == const.SERVER_MODE:
            result = rsa.decrypt(data, APICaller.getServerKey())

        return result
