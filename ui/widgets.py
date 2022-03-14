from shutil import which

from PyQt5.QtGui import QIcon, QFont
from .sidetab import SideTab
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
import os

class Menu(QtWidgets.QMenu):
    def __init__(self, p=None):
        super(Menu, self).__init__()
        self.setParent(p)

class SideFrame(QtWidgets.QFrame):
    def __init__(self, p=None):
        super(SideFrame, self).__init__()
        self.setParent(p)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.setObjectName("sidesection")

        self.apptitle = QtWidgets.QLabel("Company Name", self)
        self.apptitle.setObjectName("apptitle")
        self.appdesc = QtWidgets.QTextBrowser(self)
        self.appdesc.setText("Self Portal \U0001F37D")
        self.appdesc.setAlignment(Qt.AlignCenter)
        self.appdesc.setObjectName("appdesc")
        self.appdesc.setMaximumHeight(120)
        self.tab = SideTab(self)

        self.tabnames = ["All", "Onboarding", "Browser", "Design", "Security", "Programming", "Utility", "Communications"]
        self.tab.addTabs(self.tabnames)

        self.moremenu = Menu(self)
        self.moremenu.setObjectName("moremenu")
        self.moremenu.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.moremenu.setFont(QFont("Arial"))
        self.moremenu.setAttribute(Qt.WA_TranslucentBackground)

        self.morebutton = QtWidgets.QPushButton(self)
        self.morebutton.setObjectName("morebutton")
        self.morebutton.setMenu(self.moremenu)
        self.morebutton.setText("Menu")

        self.vlay.addWidget(self.apptitle, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.appdesc)
        self.vlay.addWidget(self.tab, stretch=5)
        self.vlay.addWidget(self.morebutton, alignment=Qt.AlignCenter)


class AppIcon(QtWidgets.QPushButton):
    def __init__(self, p=None):
        super(AppIcon, self).__init__()
        self.setParent(p)
        self.setStyleSheet("background: transparent; border: none;")
        self.setAttribute(Qt.WA_TransparentForMouseEvents)


class AppWidget(QtWidgets.QPushButton):
    def __init__(self, p=None, icon=None, name=None, category=None, description=None, bashcmd=None):
        super(AppWidget, self).__init__()
        self.setParent(p)
        self.setFixedSize(150, 150)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.signal = Signal()
        self.setMouseTracking(True)
        self.category = category
        self.description = description
        self.bashcmd = bashcmd
        self.name = name

        self.appicon = AppIcon(self)
        self.appicon.setIcon(QIcon(icon))
        self.appicon.setIconSize(QSize(40, 40))

        self.apptitle = QtWidgets.QLabel(name, self)
        self.apptitle.setObjectName("apptitlewidget")

        self.downloadbutton = QtWidgets.QPushButton("Install", self)
        self.downloadbutton.setObjectName("downloadbutton")

        if which('chef-client'):
            self.statuslabel = QtWidgets.QLabel("Installing...", self)
            self.statuslabel.hide()
        else:
            self.statuslabel = QtWidgets.QLabel("Chef not installed", self)
            self.statuslabel.hide()

        self.vlay.addWidget(self.appicon, alignment=Qt.AlignVCenter)
        self.vlay.addWidget(self.apptitle, alignment=Qt.AlignCenter)
        self.vlay.addWidget(self.downloadbutton)
        self.vlay.addWidget(self.statuslabel, alignment=Qt.AlignCenter)

        self.clicked.connect(lambda: self.signal.appdesc.emit(self.description))
        self.clicked.connect(lambda: self.signal.appname.emit(name))
        self.downloadbutton.clicked.connect(lambda: self.signal.appname.emit(name))
        self.downloadbutton.clicked.connect(lambda: self.signal.appdesc.emit(self.description))
        self.downloadbutton.clicked.connect(lambda: self.signal.download.emit(self.bashcmd, self))


class Signal(QObject):
    appdesc = pyqtSignal(str)
    appname = pyqtSignal(str)
    download = pyqtSignal(str, object)
