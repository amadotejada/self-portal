import glob
import json
import subprocess
import sys
import os
import time
from shutil import which

from PyQt5.QtCore import QSize, center, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QPixmap
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QFrame, QMessageBox, QWidget)

from ui.scrollable import Scrollable
from ui.tasking import Task, TaskManager, TaskSignals
from ui.widgets import AppWidget, SideFrame

dir_path = os.path.dirname(os.path.abspath(__file__))

class Signal(TaskSignals):
    installCompleted = pyqtSignal()
    installFailed = pyqtSignal()
    showApp = pyqtSignal(object)
    hideApp = pyqtSignal(object)
    delAppFromLayout = pyqtSignal(object)
    addAppFromLayout = pyqtSignal(object)

class BashInstall(Task):
    def __init__(self, bashcmd):
        super(BashInstall, self).__init__()
        self.signal = Signal()
        self.bashcmd = bashcmd

    def run(self) -> None:
        if which('chef-client'):
            print (self.bashcmd)
            results = subprocess.call(self.bashcmd.split())
            if results == 0:
                print("chef-client ran successfully")
                self.signal.installCompleted.emit()
            else:
                print("chef-client ran failed")
                self.signal.installFailed.emit()
        else:
            print("chef not found")

class Search(Task):
    def __init__(self, apps, term):
        super(Search, self).__init__()
        self.searchTerm = term
        self.apps = apps
        self.signal = Signal()
        self.isStopped = False

    def run(self) -> None:
        if self.searchTerm != "":
            for app in self.apps:
                if self.searchTerm.lower() in app.name.lower():
                    self.signal.addAppFromLayout.emit(app)
                    self.signal.showApp.emit(app)
                else:
                    self.signal.hideApp.emit(app)
                    self.signal.delAppFromLayout.emit(app)
        else:
            for app in self.apps:
                self.signal.addAppFromLayout.emit(app)
                self.signal.showApp.emit(app)
                # time.sleep(0.02)

class MainPage(QFrame):
    def __init__(self, parent=None):
        super(MainPage, self).__init__()
        self.setParent(parent)
        self.flay = Scrollable(self)
        self.apps = []
        for jsonfile in glob.glob(f"{dir_path}/resources/apps/*json"):
            with open(jsonfile, encoding="utf-8") as file:
                data = json.load(file)
            appwidget = AppWidget(self, f"{dir_path}/" + data["icon"],
            data["name"], data["category"], data["description"], data["bashcmd"])
            self.flay.addApp(appwidget)
            self.apps.append(appwidget)
            appwidget.signal.appdesc.connect(self.parent().sideframe.appdesc.setText)
            appwidget.signal.appname.connect(self.parent().sideframe.apptitle.setText)
            appwidget.signal.download.connect(self.parent().initiateBashInstall)

    def resizeEvent(self, e):
        self.flay.resize(self.width() - 5, self.height())

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1090, 690)
        self.centerWindow()
        self.setWindowIcon(QIcon(f"{dir_path}/resources/icons/appicon.png"))
        self.setObjectName("window")
        self.setWindowTitle("Self Portal \U0001F37D")
        self.sideframe = SideFrame(self)

        self.mainframe = MainPage(self)
        self.mainframe.move(255, 0)

        aboutMsg = "Self Portal is a cross-platform application used to deploy software via Chef"
        informativeMsg =\
        "\n\nVersion: 0.7.0 beta"\
        "\n\n*Self Portal is in no way affiliated with Chef Progress."

        self.aboutwindow = QMessageBox(self)
        aboutIcon = QPixmap(f"{dir_path}/resources/icons/appicon.png")
        self.aboutwindow.setIconPixmap(aboutIcon.scaled(72, 72))
        # self.aboutwindow.setIcon(QMessageBox.Information)
        self.aboutwindow.setWindowTitle("Self Portal \U0001F37D")
        self.aboutwindow.setText(aboutMsg)
        self.aboutwindow.setInformativeText(informativeMsg)
        # self.aboutwindow.setBaseSize(QSize(550, 250))

        self.sideframe.moremenu.addAction("GitHub", self.requestapp)
        self.sideframe.moremenu.addAction("About", self.aboutwindow.show)
        self.sideframe.tab.searchbar.textChanged.connect(self.search)

        self.taskmanager = TaskManager()

        self.sideframe.tab.tabs["All"].clicked.connect(lambda: self.showSpecificCategory("all"))
        self.sideframe.tab.tabs["Browser"].clicked.connect(lambda: self.showSpecificCategory("browser"))
        self.sideframe.tab.tabs["Onboarding"].clicked.connect(lambda: self.showSpecificCategory("pnboarding"))
        self.sideframe.tab.tabs["Design"].clicked.connect(lambda: self.showSpecificCategory("design"))
        self.sideframe.tab.tabs["Security"].clicked.connect(lambda: self.showSpecificCategory("security"))
        self.sideframe.tab.tabs["Programming"].clicked.connect(lambda: self.showSpecificCategory("programming"))
        self.sideframe.tab.tabs["Utility"].clicked.connect(lambda: self.showSpecificCategory("utility"))
        self.sideframe.tab.tabs["Communications"].clicked.connect(lambda: self.showSpecificCategory("communications"))

    def centerWindow(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def search(self, term):
        task = Search(self.mainframe.apps, term)
        task.signal.showApp.connect(lambda app: app.show())
        task.signal.hideApp.connect(lambda app: app.hide())
        task.signal.addAppFromLayout.connect(self.mainframe.flay.widgetLayout.addWidget)
        task.signal.delAppFromLayout.connect(self.mainframe.flay.widgetLayout.removeWidget)
        self.taskmanager.setMaxThreadCount(1000)
        self.taskmanager.start(task)

    def requestapp(self):
        url = "https://github.com/amadotejada/self-portal"
        if "linux" in sys.platform:
            subprocess.call([f"sudo -u $(logname) bash -c 'xdg-open {url}'"], shell=True)
        if "darwin" in sys.platform:
            subprocess.call(["/usr/bin/open", f"{url}"])
        if "win32" in sys.platform:
            subprocess.call(["start", f"{url}"])

    def initiateBashInstall(self, bashcmd, app):
        app.downloadbutton.hide()
        app.statuslabel.show()

        installTask = BashInstall(bashcmd)
        self.taskmanager.start(installTask)

        installTask.signal.installCompleted.connect(app.downloadbutton.show)
        installTask.signal.installCompleted.connect(app.statuslabel.hide)
        installTask.signal.installCompleted.connect(
            lambda: app.downloadbutton.setText("Installed"))

        installTask.signal.installFailed.connect(app.downloadbutton.show)
        installTask.signal.installFailed.connect(app.statuslabel.hide)
        installTask.signal.installFailed.connect(
            lambda: app.downloadbutton.setText("Failed to install"))

    def showSpecificCategory(self, category):
        for app in self.mainframe.apps:
            for cat in app.category:
                if cat == category:
                    self.mainframe.flay.widgetLayout.addWidget(app)
                    app.show()
                    break
                elif category == "all":
                    self.mainframe.flay.widgetLayout.addWidget(app)
                    app.show()
                else:
                    app.hide()
                    self.mainframe.flay.widgetLayout.removeWidget(app)

    def resizeEvent(self, a0) -> None:
        self.sideframe.resize(250, self.height())
        self.mainframe.resize(self.width() - 250, self.height())

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    # QFontDatabase.addApplicationFont(":/font/Arial.ttf")
    # qapp.setFont(QFont("Arial", 12))
    with open(f"{dir_path}/resources/style/style.qss") as qss:
        qapp.setStyleSheet(qss.read())
    win = MainWindow()
    win.show()
    sys.exit(qapp.exec_())
