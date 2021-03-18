class Message(object):

    def __init__(self, timestamp, msg, sender):
        super(Message, self).__init__()

        self.timestamp = timestamp
        self.msg = msg
        self.sender = sender
        