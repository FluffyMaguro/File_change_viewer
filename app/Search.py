import os
import threading
import time

lock = threading.Lock()


class Search:
    def __init__(self, signal):
        self.folder = None
        self.thread = None
        self.interval = 1
        self.new_file_color = "black"
        self.signal = signal
        self.file_data = dict()

    def run(self, path: str):
        """ Runs the search and updates the searched folder
        args:
            path : Folder path to search (str)
        """
        if path is None:
            return

        # Check for new path
        if path == self.folder:
            return
        else:
            with lock:
                self.folder = path
                self.signal.emit((f'Setting new folder: "{path}"', ))

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

    def search_thread(self):
        self.seach_iter()
        self.new_file_color = "green"

        while True:
            time.sleep(self.interval)
            self.seach_iter()

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
                    self.send_log(file_path, changed, self.new_file_color)

                # Changed file
                elif self.file_data[file_path] != changed:
                    self.file_data[file_path] = changed
                    self.send_log(file_path, changed, "blue")

        # Deleted files
        now = time.time()
        for f in tuple(self.file_data):
            if f not in found_files:
                del self.file_data[f]
                self.send_log(f, now, "red")

    def send_log(self, file_path, changed, color):
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                       time.localtime(changed))
        self.signal.emit((f"{formatted_time} | {file_path}", color))