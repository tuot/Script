import shutil
import time
import os
import pathlib

import fire
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

if os.name == 'nt':
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
elif os.name == 'posix':
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

print(desktop)


class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self, listen_path):
        event_handler = Handler()
        self.observer.schedule(event_handler, listen_path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as e:
                os.unlink(d)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
    # shutil.rmtree(src)


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

            if "execute.bat" in event.src_path:
                print("Copy It!")
                parent = pathlib.Path(event.src_path).parent
                copytree(parent, desktop)


if __name__ == '__main__':
    fire.Fire(Watcher)
