from model import Message
import json

def messagetobytearray(msg: Message.Message):

    x = json.dumps(msg.__dict__)

    return bytearray(x.encode())

def bytearraytomessage(b: bytearray):

    return json.loads(b.decode("utf8"))
