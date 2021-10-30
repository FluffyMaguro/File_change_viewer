import os
import subprocess
from typing import Tuple

from PyQt5 import QtCore, QtGui, QtWidgets

from app.Search import Search


class MainWidget(QtWidgets.QWidget):
    log_signal = QtCore.pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.folder = None
        self.search = Search(self.log_signal)
        self.log_signal.connect(self.log)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        hlayout = QtWidgets.QHBoxLayout()

        # Folder button
        self.folder_button = QtWidgets.QPushButton(self.folder if isinstance(
            self.folder, str) else "Select a folder to search")
        self.folder_button.clicked.connect(self.change_folder)
        self.folder_button.setStatusTip("Change which folder to search")
        hlayout.addWidget(self.folder_button)

        # Timer
        timer_label = QtWidgets.QLabel("Interval (sec):")
        timer_label.setMaximumWidth(70)
        hlayout.addWidget(timer_label)

        interval = QtWidgets.QLineEdit("1")
        interval.setMaximumWidth(30)
        interval.setStatusTip(
            "Change how often the app searches the directory (seconds)")
        interval.textChanged.connect(self.interval_changed)
        hlayout.addWidget(interval)

        layout.addLayout(hlayout)

        # Log widget
        self.log_widget = QtWidgets.QListWidget()
        self.log_widget.itemDoubleClicked.connect(self.open_file_location)
        layout.addWidget(self.log_widget)

        # Run
        self.search.run(self.folder)

    def interval_changed(self, time):
        try:
            new_interval = float(time)
        except ValueError:
            return

        if new_interval > 0:
            self.search.set_interval(new_interval)
            self.log((f"Changing interval to {new_interval}", ))

    def open_file_location(self, item: QtWidgets.QListWidget):
        """ Opens a location of file or folder"""
        file_path = os.path.abspath(item.text().split(" | ")[1])
        # Select dirname if it the file doesn't exists
        if not os.path.isfile(file_path):
            file_path = os.path.dirname(file_path)

        if os.name == 'nt':
            subprocess.Popen(f'explorer /select,"{file_path}"')
        else:
            subprocess.Popen(["open", file_path])

    def log(self, data: Tuple[str, str]):
        """ Logs data into a widget

        args:
            data : tuple of message and color (or just message)"""

        if len(data) == 2:
            message, color = data
        else:
            message, color = data[0], "black"

        w = QtWidgets.QListWidgetItem(message, self.log_widget)
        w.setForeground(QtGui.QColor(color))
        self.log_widget.scrollToBottom()

    def change_folder(self):
        """ Finds and sets folder that's being searched"""
        dialog = QtWidgets.QFileDialog()
        if self.folder is not None:
            dialog.setDirectory(self.folder)

        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)

        if dialog.exec_():
            dirpath = dialog.selectedFiles()[0]
            dirpath = os.path.normpath(dirpath)
            if not os.path.isdir(dirpath):
                self.log(("Not a valid folder", ))
                return

            if dirpath != self.folder:
                self.log_widget.clear()

            self.folder = dirpath
            self.folder_button.setText(dirpath)
            self.search.run(dirpath)
