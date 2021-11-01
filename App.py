import sys
import webbrowser
from functools import partial

from PyQt6 import QtCore, QtGui, QtWidgets

from app.MainWidget import MainWidget

VERSION = "1.1"


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"File change viewer (v{VERSION})")
        self.setWindowIcon(QtGui.QIcon('src/Icon.ico'))
        self.setGeometry(0, 0, 800, 600)
        self.init_UI()

    def init_UI(self):
        # Center the app
        self.center()

        # Create the central widget
        self.setCentralWidget(MainWidget())

        # Create menu bar items
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        link_menu = menubar.addMenu('Links')
        setting_menu = menubar.addMenu('Settings')

        # Exit
        icon = self.style().standardIcon(
            getattr(QtWidgets.QStyle.StandardPixmap, 'SP_DialogCloseButton'))

        exitAction = QtGui.QAction(icon, 'Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.QApplication.quit)
        file_menu.addAction(exitAction)

        # Github
        icon = QtGui.QIcon("src/github.png")
        githubAction = QtGui.QAction(icon, 'Github page', self)
        githubAction.triggered.connect(
            partial(webbrowser.open,
                    "https://github.com/FluffyMaguro/File_change_viewer"))
        link_menu.addAction(githubAction)

        # Maguro
        icon = QtGui.QIcon("src/maguro.jpg")
        maguroAction = QtGui.QAction(icon, 'Maguro.one', self)
        maguroAction.triggered.connect(
            partial(webbrowser.open, "https://www.maguro.one/"))
        link_menu.addAction(maguroAction)

        # Init
        init_log_Action = QtGui.QAction('Log initial files', self)
        init_log_Action.setStatusTip(
            'Affects whether to show the log of all files when a folder is selected'
        )
        init_log_Action.setCheckable(True)
        init_log_Action.setChecked(True)
        init_log_Action.triggered.connect(
            self.centralWidget().search.set_init_log)
        setting_menu.addAction(init_log_Action)

        # Save to file
        save_data_Action = QtGui.QAction('Save log data', self)
        save_data_Action.setStatusTip('Saves logged data to a file')
        save_data_Action.setCheckable(True)
        save_data_Action.setChecked(False)
        save_data_Action.triggered.connect(
            self.centralWidget().search.set_save_data)
        setting_menu.addAction(save_data_Action)

        self.statusBar()
        self.show()

    def center(self):
        """ Centers the current widget"""
        rectangle = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rectangle.moveCenter(center)
        self.move(rectangle.topLeft())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec())
