from .Singleton import Singleton
from datetime import datetime
from colorama import Fore,Back, Style

class Logger(metaclass=Singleton):
    def __init__(self):
        self.logs = []

    def log(self, msg, type=1):
        ## Types
        # 1 : Information
        # 2 : Success
        # 3 : Failure
        # 4 : Data
        date = datetime.now().strftime('%Y %H:%M:%S')
        types = {
            1: Fore.YELLOW,
            2: Fore.GREEN,
            3: Fore.RED,
            4: Fore.MAGENTA
        }
        color = types.get(type)
        log = str(f'{date} *{color} {msg} {Style.RESET_ALL}')
        Logger().logs.append(log)
        print(log)

