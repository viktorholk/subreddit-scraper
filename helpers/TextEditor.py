from os import path, system, remove
import time
import json
from .Logger import Logger
from .Wrapper import Wrapper
from .CacheObserver import CacheObserver
from .Singleton import Singleton
from datetime import datetime, timedelta
logger = Logger()

# Singleton class since we want to make sure the observer class only is started once
class TextEditor(metaclass=Singleton):
    def __init__(self):
        self.path = 'cache.json'
        # Observer
        self.observer = CacheObserver()
        self.observer.run()
        
    def edit(self, obj):
        # create cache file
        Wrapper().write_json(self.path,
                {
                    'title': obj.title,
                    'body': obj.body
                })

        system(f'start {self.path}')

        while True:
            if self.observer.get_edited():
                _posts_json  = Wrapper().read_json(Wrapper().postsPath)
                _cache_json = Wrapper().read_json(self.path)

                for i in _posts_json['posts']:
                    if i['id'] == obj.id:
                        i['title']  = _cache_json['title']
                        i['body']   = _cache_json['body']
                        break
                # Update the json
                Wrapper().write_json(Wrapper().postsPath, _posts_json)
                logger.log('Edited post', 2)
                # Remove the file
                try:
                    system(f'taskkill /IM "notepad.exe" /T')
                except:
                    pass
                remove(self.path)
                break
        return True

    def stop(self):
        self.observer.stop()