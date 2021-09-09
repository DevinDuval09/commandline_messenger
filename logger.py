'''logger'''

import logging
import datetime
import os

class Messenger_Logger(logging.getLoggerClass()):
    def __init__(self, log_type:str):
        super().__init__(log_type)
        self.log_type = log_type
        
        if not os.path.isdir(f".//logs//{self.log_type}"):
            try:
                os.mkdir(f".//logs//{self.log_type}")
            except FileNotFoundError:
                os.mkdir(f".//logs")
                os.mkdir(f".//logs//{self.log_type}")

        today = datetime.datetime.now()
        self.file = f'{log_type.capitalize()}Log_{today.month:0>2}_{today.day:0>2}_{today.year}.log'

        LOG_FORMAT = '"%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"'
        formatter = logging.Formatter(LOG_FORMAT)

        file_handler = logging.FileHandler(f'.//logs//{self.file}', mode='a')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.CRITICAL)

        self.setLevel(logging.INFO)
        self.addHandler(file_handler)
        self.addHandler(console_handler)
