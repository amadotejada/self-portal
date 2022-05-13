# Copyright 2021 Amado Tejada
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PyQt6.QtGui import QIcon, QFont
from .sidetab import SideTab
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject
import os


dir_path = os.path.dirname(os.path.abspath(__file__))


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

        self.apptitle = QtWidgets.QLabel("Self Portal", self)
        self.apptitle.setObjectName("apptitle")
        self.appdesc = QtWidgets.QTextBrowser(self)
        self.appdesc.setText("Welcome!\n\n")
        self.appdesc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.appdesc.setObjectName("appdesc")
        self.appdesc.setMaximumHeight(100)
        self.tab = SideTab(self)

        self.moremenu = Menu(self)
        self.moremenu.setObjectName("moremenu")
        self.moremenu.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup |
                                     Qt.WindowType.NoDropShadowWindowHint)
        self.moremenu.setFont(QFont("Roboto"))
        self.moremenu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.morebutton = QtWidgets.QPushButton(self)
        self.morebutton.setObjectName("morebutton")
        self.morebutton.setMenu(self.moremenu)
        self.morebutton.setText("Menu")

        self.vlay.addWidget(self.apptitle, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vlay.addWidget(self.appdesc)
        self.vlay.addWidget(self.tab, stretch=5)
        self.vlay.addWidget(self.morebutton, alignment=Qt.AlignmentFlag.AlignCenter)


class AppIcon(QtWidgets.QPushButton):
    def __init__(self, p=None):
        super(AppIcon, self).__init__()
        self.setParent(p)
        self.setStyleSheet("background: transparent; border: none;")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

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
        self.appicon.setIcon(QIcon(f"{dir_path}/{icon}".replace("ui", "")))
        self.appicon.setIconSize(QSize(35, 35))

        self.apptitle = QtWidgets.QLabel(name, self)
        self.apptitle.setObjectName("apptitlewidget")

        self.downloadbutton = QtWidgets.QPushButton("Install", self)
        self.downloadbutton.setObjectName("downloadbutton")

        self.statuslabel = QtWidgets.QLabel("Installing", self)
        self.statuslabel.hide()

        self.vlay.addWidget(self.appicon, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.vlay.addWidget(self.apptitle, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vlay.addWidget(self.downloadbutton)
        self.vlay.addWidget(self.statuslabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.clicked.connect(lambda: self.signal.appdesc.emit(self.description))
        self.clicked.connect(lambda: self.signal.appname.emit(name))
        self.downloadbutton.clicked.connect(lambda: self.signal.appname.emit(name))
        self.downloadbutton.clicked.connect(lambda: self.signal.appdesc.emit(self.description))
        self.downloadbutton.clicked.connect(lambda: self.signal.download.emit(self.bashcmd, self))


class Signal(QObject):
    appdesc = pyqtSignal(str)
    appname = pyqtSignal(str)
    download = pyqtSignal(str, object)
