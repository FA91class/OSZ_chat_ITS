from model import Message
import json


def message_to_byte_array(msg: Message.Message):
    x = json.dumps(msg.__dict__)

    return bytearray(x.encode())


def byte_array_to_message(b: bytearray):
    d = json.loads(b.decode("utf8"))
    return Message.Message(d["timestamp"], d["msg"], d["sender"])
