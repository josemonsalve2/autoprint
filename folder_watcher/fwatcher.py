import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config.debug import log
from config.params import ap_params
import os
from printer.printer import printer_driver as pd


class Watcher:
    dirs_to_watch = None
    observers = {}
    event_handlers = {}

    def __init__(self):
        self.dirs_to_watch = ap_params["FOLDERS_TO_WATCH"]
        for d in self.dirs_to_watch:
            log.info(f"Creating Observer for folder {d}")
            self.observers[d] = Observer()

    def create_observers(self):
        for d in self.dirs_to_watch:
            log.info(f"Scheduling Handler for folder {d}")
            self.event_handlers[d] = Handler()
            self.observers[d].schedule(self.event_handlers[d], d, recursive=True)
            self.observers[d].start()
            
    def run(self):
        log.info(f"Running until program quit")
        try:
            while True:
                time.sleep(ap_params["WAITING_TIME"])
        except Exception as e:
            self.stop_observers()
            log.critical(f"Error when watching folders{str(e)}")
        except KeyboardInterrupt as e:
            self.stop_observers()
            log.info(f"Finishing process normally")


    def stop_observers(self):
        for d in self.dirs_to_watch:
            log.info(f"Stoping observer for {d}")
            self.observers[d].stop()
            self.observers[d].join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        log.debug(f"Detected event {event.event_type}")
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            log.info(f"Received created event on file - {event.src_path}")
            if checkIfExtensionMatch(event.src_path) and checkIfPrefixMatch(event.src_path):
                log.info(f"Printing {event.src_path}")
                p_driver = pd(ap_params['PRINTER_NAME'])
                p_driver.print(event.src_path)
                if ap_params["AUTODELETE"]:
                    os.remove(event.src_path)


def checkIfExtensionMatch(filename):
    _ , file_extension = os.path.splitext(filename)
    if len(ap_params["EXTENSIONS_FILTER"]) == 0 or file_extension in ap_params["EXTENSIONS_FILTER"]:
        return True
    return False

def checkIfPrefixMatch(filename):
    basename = os.path.basename(filename)
    if len(ap_params["FILES_PREFIX"]) == 0:
        return True
    for prefix in ap_params["FILES_PREFIX"]:
        if basename.startswith(prefix):
            return True
    return False