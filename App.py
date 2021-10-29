import sys
import webbrowser
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

from app.MainWidget import MainWidget

VERSION = "1.1"


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"File change viewer (v{VERSION})")
        self.setWindowIcon(QtGui.QIcon('src/Icon.ico'))
        self.setGeometry(0, 0, 800, 600)

        # Center the app
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() -
                  QtCore.QPoint(int(self.width() / 2), int(self.height() / 2)))

        # Create the central widget
        self.setCentralWidget(MainWidget())

        # Create menu bar items
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        link_menu = menubar.addMenu('Links')
        setting_menu = menubar.addMenu('Settings')

        # Exit
        icon = self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_DialogCloseButton'))
        exitAction = QtWidgets.QAction(icon, 'Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        file_menu.addAction(exitAction)

        # Github
        icon = QtGui.QIcon("src/github.png")
        githubAction = QtWidgets.QAction(icon, 'Github page', self)
        githubAction.triggered.connect(
            partial(webbrowser.open,
                    "https://github.com/FluffyMaguro/File_change_viewer"))
        link_menu.addAction(githubAction)

        # Maguro
        icon = QtGui.QIcon("src/maguro.jpg")
        maguroAction = QtWidgets.QAction(icon, 'Maguro.one', self)
        maguroAction.triggered.connect(
            partial(webbrowser.open, "https://www.maguro.one/"))
        link_menu.addAction(maguroAction)

        # Init
        init_log_Action = QtWidgets.QAction('Log initial files', self)
        init_log_Action.setStatusTip(
            'Affects whether to show the log of all files when a folder is selected'
        )
        init_log_Action.setCheckable(True)
        init_log_Action.setChecked(True)
        init_log_Action.triggered.connect(
            self.centralWidget().search.set_init_log)
        setting_menu.addAction(init_log_Action)

        self.statusBar()
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())
