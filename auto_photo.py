"""
This code is used to automatically organize photos.

Author: Chengzhang Zhu
Email: kevin.zhu.china@gmail.com
"""

from watchdog.observers import Observer
from watchdog.events import *
from organization import organize
import time
import argparse


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, watch_path, destination_path, organized_files, organize_period):
        self.watch_path = watch_path
        self.destination_path = destination_path
        self.organized_files = organized_files
        self.organize_period = organize_period
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        if event.is_directory:
            self.organized_files = organize(self.watch_path, self.destination_path, self.organized_files, self.organize_period)
        else:
            self.organized_files = organize(self.watch_path, self.destination_path, self.organized_files, self.organize_period)


parser = argparse.ArgumentParser(description='Auto-Photo: organizing your photos by time')
parser.add_argument('--watch', help='the file path need to watch', dest='watch', type=str)
parser.add_argument('--dest', help='the destination path to organized file', dest='dest', type=str)
parser.add_argument('--period', help='the organization period, can use the combination of "ymd", "y" for year, "m" for month, "d" for day', dest='period', type=str)

args = parser.parse_args()

watch_file_path = args.watch
destination_file_path = args.dest
organized_files_list = organize(watch_file_path, destination_file_path, period=args.period)
observer = Observer()
event_handler = FileEventHandler(watch_file_path, destination_file_path, organized_files_list, args.period)
observer.schedule(event_handler, watch_file_path, True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
