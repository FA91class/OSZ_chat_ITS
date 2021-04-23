from model.Message import Message
import json


def message_to_byte_array(msg: Message):
    x = json.dumps(msg.__dict__)
    return bytearray(x.encode())


def byte_array_to_message(b: bytearray):
    d = json.loads(b.decode("utf8"))
    return Message(d["timestamp"], d["msg"], d["sender"])


def message_to_bytes(msg: Message):
    x = json.dumps(msg.__dict__)
    return bytes(x.encode())


def bytes_to_message(b: bytes):
    d = json.loads(b.decode("utf8"))
    return Message(d["timestamp"], d["msg"], d["sender"])
