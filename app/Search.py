import os
import threading
import time

from PyQt5 import QtCore

lock = threading.Lock()


class Search:
    base_color = "black"
    file_deleted_color = "red"
    file_created_color = "green"
    file_changed_color = "blue"

    def __init__(self, signal: QtCore.pyqtSignal):
        self.folder = None
        self.thread = None
        self.interval = 1
        self.signal = signal
        self.file_data = dict()
        self.init_log = True
        self.init_search = True

    def run(self, path: str):
        """ Runs the search and updates the searched folder

        args:
            path : Folder path to search (str)
        """
        if path is None:
            return

        # Check for new path
        if path != self.folder:
            with lock:
                self.folder = path
                self.file_data = dict()
                self.init_search = True

        # Create a thread for searching
        if self.thread is None:
            self.thread = threading.Thread(target=self.search_thread,
                                           daemon=True)
            self.thread.start()

    def set_timer(self, time: float):
        if time <= 0:
            self.signal.emit((f'Invalid new interval: {time}', "red"))
            return

        with lock:
            self.interval = time

    def set_init_log(self, status: bool):
        with lock:
            self.init_log = status

    def search_thread(self):
        while True:
            self.seach_iter()
            time.sleep(self.interval)

    def seach_iter(self):
        found_files = set()
        for root, _, files in os.walk(self.folder):
            for f in files:
                file_path = os.path.join(root, f)
                changed = os.path.getmtime(file_path)
                found_files.add(file_path)

                # New file
                if file_path not in self.file_data:
                    self.file_data[file_path] = changed
                    if self.init_search and self.init_log:
                        self.send_log(file_path, changed, self.base_color)

                    elif not self.init_search:
                        self.send_log(file_path, changed,
                                      self.file_created_color)

                # Changed file
                elif self.file_data[file_path] != changed:
                    self.file_data[file_path] = changed
                    self.send_log(file_path, changed, self.file_changed_color)

        # Deleted files
        now = time.time()
        for f in tuple(self.file_data):
            if f not in found_files:
                del self.file_data[f]
                self.send_log(f, now, self.file_deleted_color)

        # Not an initial search anymore
        self.init_search = False

    def send_log(self, file_path: str, changed: float, color: str):
        """ Passes information about file changes up"""
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                       time.localtime(changed))
        self.signal.emit(
            (f"{formatted_time} | {os.path.normpath(file_path)}", color))
