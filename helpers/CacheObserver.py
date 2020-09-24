from .Singleton import Singleton
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
EDITED = False

class EventHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = datetime.now()

    def on_any_event(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()

        if event.is_directory:
            return None

        if (event.event_type == 'modified' and event.src_path == r'.\cache.json'):
            print(event.event_type)
            global EDITED
            EDITED = True

class CacheObserver(metaclass=Singleton):
    def __init__(self):
        self.observer           = Observer()
        self.path               = '.'
        self.event_handler      = EventHandler()

    def run(self):
        self.observer.schedule(self.event_handler, self.path)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def get_edited(self):
        global EDITED
        _ = EDITED
        EDITED = False
        return _