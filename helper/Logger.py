from model.Message import Message
from helper import Style
from helper import const
import datetime
import os


def log_message(msg: Message):

        filename = str(datetime.date.today()) + "_chatlog.log"
        file = const.LOG_PATH + filename

        if os.path.exists(const.LOG_PATH) == False:
            os.mkdir(const.LOG_PATH)
            f = open(file, "x")
            f.close

        if os.path.isfile(file) == False:
            f = open(file, "x")
            f.close
        
        f = open(file, "a")
        f.writelines(msg.msg + '\n')
        f.close
