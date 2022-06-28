
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

import datetime
import glob
import json
import os
import subprocess
import sys
import time
from shutil import which

from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog, QFrame,
                             QHBoxLayout, QLabel, QMessageBox, QPushButton,
                             QRadioButton, QTextBrowser, QVBoxLayout, QWidget,
                             QWizard, QWizardPage)

from ui.scrollable import Scrollable
from ui.tasking import Task, TaskManager, TaskSignals
from ui.widgets import AppWidget, SideFrame

from platform import system

dir_path = os.path.dirname(os.path.abspath(__file__))

IS_WINDOWS = system() == "Windows"
IS_MAC = system() == "Darwin"
IS_LINUX = system() == "Linux"

class Signal(TaskSignals):
    installCompleted = pyqtSignal()
    installFailed = pyqtSignal()
    installerror = pyqtSignal()
    installLog = pyqtSignal(str)

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
        try:
            with open(f"{dir_path}/conf/conf.json", "r+") as cfile:
                conf = json.load(cfile)
                if which(conf["client"]):
                    process = subprocess.Popen(
                        self.bashcmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

                    def check_io():
                        while True:
                            output = process.stdout.readline().decode()
                            if output:
                                self.signal.installLog.emit(output)
                            else:
                                break

                    while process.poll() is None:
                        check_io()
                    rc = process.poll()  # rc = return code
                    if rc == 0:
                        self.signal.installCompleted.emit()
                    else:
                        self.signal.installFailed.emit()
                else:
                    self.signal.installerror.emit()

        except Exception as e:
            print(e)


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
                time.sleep(0.02)


class MainPage(QFrame):
    def __init__(self, parent=None):
        super(MainPage, self).__init__()
        self.setParent(parent)
        self.flay = Scrollable(self)
        self.apps = []
        for jsonfile in glob.glob(f"{dir_path}/resources/apps/*json"):
            with open(jsonfile, encoding="utf-8") as file:
                data = json.load(file)

            appwidget = AppWidget(
                self, data["icon"], data["name"], data["category"], data["description"], data["bashcmd"])

            self.flay.addApp(appwidget)
            self.apps.append(appwidget)
            appwidget.signal.appdesc.connect(self.parent().sideframe.appdesc.setText)
            appwidget.signal.appname.connect(self.parent().sideframe.apptitle.setText)
            appwidget.signal.download.connect(self.parent().initiateBashInstall)

    def resizeEvent(self, e):
        self.flay.resize(self.width() - 5, self.height())


class WizardAbout(QWizardPage):
    def __init__(self):
        super(WizardAbout, self).__init__()
        self.vlay = QVBoxLayout(self)

        self.setTitle("Welcome!")

        self.about = QLabel(self)
        self.about.setText(
            "Hello, this is a placeholder text!"
            "\n"
        )

        self.vlay.addWidget(self.about)


class WizardImageContainer(QLabel):
    onClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(WizardImageContainer, self).__init__(*args, **kwargs)

    def mousePressEvent(self, ev) -> None:
        self.onClicked.emit()
        QLabel.mousePressEvent(self, ev)


class ThemeWizard(QWizardPage):
    def __init__(self):
        super(ThemeWizard, self).__init__()
        self.vlay = QVBoxLayout(self)
        self.hlay = QHBoxLayout()
        self.light_lay = QVBoxLayout()
        self.dark_lay = QVBoxLayout()

        self.setTitle("Select Theme")

        self.light_image = WizardImageContainer(self)
        self.light_image.onClicked.connect(lambda: self.light_radio.setChecked(True))
        self.light_image.setPixmap(QPixmap(f"{dir_path}/resources/light.png")
                                   .scaled(int(1047 / 3), int(667 / 3), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.light_radio = QRadioButton("Light", self)
        self.light_lay.addWidget(self.light_image)
        self.light_lay.addWidget(self.light_radio, alignment=Qt.AlignCenter)

        self.dark_image = WizardImageContainer(self)
        self.dark_image.onClicked.connect(lambda: self.dark_radio.setChecked(True))
        self.dark_image.setPixmap(QPixmap(f"{dir_path}/resources/dark.png")
                                  .scaled(int(1047 / 3), int(667 / 3), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.dark_radio = QRadioButton("Dark", self)
        self.dark_lay.addWidget(self.dark_image)
        self.dark_lay.addWidget(self.dark_radio, alignment=Qt.AlignCenter)

        self.dark_radio.setChecked(True)    # default to dark mode

        self.hlay.addLayout(self.light_lay)
        self.hlay.addLayout(self.dark_lay)
        self.vlay.addLayout(self.hlay)


class Header(QFrame):
    def __init__(self, p, image, icon):
        super(Header, self).__init__(p)
        self.px = QPixmap(image)
        self.setFixedHeight(135)
        self.painter = QPainter(self)
        self.dark_overlay = QFrame(self)
        self.dark_overlay.setStyleSheet("background: rgba(0, 0, 0, 128)")
        self.hbox = QHBoxLayout(self)
        self.hbox.setAlignment(Qt.AlignLeft)

        self.icon = QLabel(self)
        self.icon.setPixmap(QPixmap(icon).scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label = QLabel("Company Name", self)
        self.label.setObjectName("header-label")

        self.hbox.addWidget(self.icon)
        self.hbox.addWidget(self.label)

    def resizeEvent(self, a0) -> None:
        self.dark_overlay.resize(self.size())
        QFrame.resizeEvent(self, a0)

    def paintEvent(self, a0) -> None:
        image = self.px
        painter = QPainter(self)
        s = image.size()
        s.scale(self.width(), self.height(), Qt.KeepAspectRatioByExpanding)
        r = QRect()
        r.setSize(s)
        painter.drawPixmap(r, image.scaled(self.width(), self.height(),
                                           Qt.KeepAspectRatioByExpanding,
                                           Qt.SmoothTransformation))
        QFrame.paintEvent(self, a0)


class LogViewer(QDialog):
    def __init__(self, p):
        super(LogViewer, self).__init__(p)
        self.vlay = QVBoxLayout(self)
        self.setWindowTitle("Installer Log Viewer")
        self.resize(600, 400)

        self.viewer = QTextBrowser(self)
        self.close_button = QPushButton("Close", self)
        self.close_button.setFixedSize(100, 35)
        self.close_button.setFocus()
        self.close_button.clicked.connect(self.hide)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.vlay.addWidget(self.viewer)
        self.vlay.addWidget(self.close_button, alignment=Qt.AlignRight)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(f"{dir_path}/resources/appicon.svg"))  # change the path to your own icon
        self.setObjectName("window")
        self.setWindowTitle("Self Portal")
        self.resize(1100, 660)  # set the starting window size
        self.centerWindow()  # center the window
        self.vlay = QVBoxLayout(self)
        self.vlay.setSpacing(0)
        self.hlay = QHBoxLayout()
        self.vlay.setContentsMargins(0, 0, 0, 0)
        self.hlay.setContentsMargins(0, 0, 0, 0)
        self.is_dark = None

        self.installer_log = LogViewer(self)

        self.initial_wizard = QWizard(self)
        self.initial_wizard.resize(724, 460)
        self.initial_wizard.setWizardStyle(QWizard.ModernStyle)
        self.initial_wizard.setWindowTitle("Self Portal Startup")
        # self.initial_wizard.addPage(WizardAbout())
        self.initial_wizard.addPage(ThemeWizard())

        self.check_fresh()  # check if it's the first time launching the app
        self.raise_window()

        self.header = Header(self, image=f"{dir_path}/resources/header.png", icon=f"{dir_path}/resources/appicon.svg")

        self.sideframe = SideFrame(self)
        self.sideframe.setFixedWidth(250)
        self.mainframe = MainPage(self)
        self.mainframe.move(255, 0)

        aboutMsg = "Self Portal is a cross-platform desktop app to deploy software via Chef\n\nVersion 1.0"
        informativeMsg = "By: Amado Tejada" \
                         "<a href='https://github.com/amadotejada/self-portal'><br/><br/>GitHub</a>"
        self.aboutwindow = QMessageBox(self)
        aboutIcon = QPixmap(f"{dir_path}/resources/appicon.svg")
        self.aboutwindow.setIconPixmap(aboutIcon.scaled(100, 100, transformMode=Qt.SmoothTransformation))
        self.aboutwindow.setWindowTitle("About")
        self.aboutwindow.setText(aboutMsg)
        self.aboutwindow.setInformativeText(informativeMsg)

        self.sideframe.moremenu.addAction("Change Theme", self.change_theme)
        self.sideframe.moremenu.addAction("Show installer logs", self.installer_log.show)
        self.sideframe.moremenu.addAction("About Self Portal", self.aboutwindow.show)
        self.sideframe.tab.searchbar.textChanged.connect(self.search)
        self.taskmanager = TaskManager()

        self.load_categories()
        self.load_configuration()

        self.hlay.addWidget(self.sideframe)
        self.hlay.addSpacing(5)
        self.hlay.addWidget(self.mainframe)
        self.vlay.addWidget(self.header)
        self.vlay.addLayout(self.hlay)

    def raise_window(self):
        if IS_LINUX:
            self.show()
        elif IS_MAC:
            self.raise_()
        elif IS_WINDOWS:
            self.activateWindow()
        else:
            self.setWindowState(Qt.WindowState.WindowActive)

    def check_fresh(self):
        with open(f"{dir_path}/conf/conf.json", "r+") as cfile:
            conf = json.load(cfile)
            if conf["fresh"]:
                self.initial_wizard.exec_()  # launch wizard if fresh
                if self.initial_wizard.page(0).dark_radio.isChecked():  # check if dark theme is selected
                    conf["dark"] = True
                else:
                    conf["dark"] = False
                conf["fresh"] = False
                cfile.seek(0)
                cfile.truncate(0)
                json.dump(conf, cfile, indent=2)

    def change_theme(self):
        with open(f"{dir_path}/conf/conf.json", "r+") as cfile:
            if self.is_dark:
                self.set_dark(False)
            else:
                self.set_dark(True)
            val = json.load(cfile)
            val["dark"] = self.is_dark
            cfile.seek(0)
            cfile.truncate(0)
            json.dump(val, cfile, indent=2)

    def load_configuration(self):   # load configurations and load previous logs
        with open(f"{dir_path}/conf/conf.json") as cfile:
            conf = json.load(cfile)
            self.set_dark(conf["dark"])

        try:
            size = os.path.getsize(f"{dir_path}/conf/log.txt")
            if size > 102400000:
                with open(f"{dir_path}conf/log.txt", "w") as log_file:
                    log_file.seek(0)
                    log_file.truncate(0)
            else:
                with open(f"{dir_path}/conf/log.txt", "r") as log_file:
                    self.installer_log.viewer.append(log_file.read())
        except FileNotFoundError:
            pass

    def set_dark(self, on: bool):
        if on:
            with open(f"{dir_path}/resources/style/dark.qss") as qss:
                self.setStyleSheet(qss.read())
                self.is_dark = True
        else:
            with open(f"{dir_path}/resources/style/light.qss") as qss:
                self.setStyleSheet(qss.read())
                self.is_dark = False

    def load_categories(self):
        with open(f"{dir_path}/conf/categories.json") as catfile:
            categories = json.load(catfile)["categories"]
            self.sideframe.tab.addTabs(categories)
            for category in categories:
                self.sideframe.tab.tabs[category].on_clicked.connect(self.showSpecificCategory)

    def centerWindow(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def search(self, term):
        task = Search(self.mainframe.apps, term)
        task.signal.showApp.connect(lambda app: app.show())

        def function(app):
            return app.hide()

        task.signal.hideApp.connect(function)
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

    def initiateBashInstall(self, bashcmd, app: AppWidget):
        app.downloadbutton.hide()
        app.statuslabel.show()

        dt = datetime.datetime.now()
        _date = dt.date()
        _time = dt.time()

        self.installer_log.viewer.append(f"========== Installing {app.name} ==========")
        self.installer_log.viewer.append(f"Client: {bashcmd}")
        self.installer_log.viewer.append(f"Date: {_date}")
        self.installer_log.viewer.append(f"Time: {_time}")
        self.installer_log.viewer.append("")

        installTask = BashInstall(bashcmd)
        self.taskmanager.start(installTask)

        installTask.signal.installLog.connect(self.installer_log.viewer.append)

        installTask.signal.installCompleted.connect(app.downloadbutton.show)
        installTask.signal.installCompleted.connect(app.statuslabel.hide)
        installTask.signal.installCompleted.connect(lambda: app.downloadbutton.setText("Reinstall"))

        installTask.signal.installFailed.connect(app.downloadbutton.show)
        installTask.signal.installFailed.connect(app.statuslabel.hide)
        installTask.signal.installFailed.connect(lambda: app.downloadbutton.setText("Failed"))

        installTask.signal.installerror.connect(app.downloadbutton.show)
        installTask.signal.installerror.connect(app.statuslabel.hide)
        installTask.signal.installerror.connect(lambda: app.downloadbutton.setText("Client not found"))

    def showSpecificCategory(self, category):
        category = category.lower()
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

    def closeEvent(self, a0) -> None:
        with open(f"{dir_path}/conf/log.txt", "a") as log_file:
            log_file.seek(0)
            log_file.truncate(0)
            log_file.write(self.installer_log.viewer.toPlainText())
        QWidget.closeEvent(self, a0)


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(f"{dir_path}/resources/fonts/Roboto.ttf")
    qapp.setFont(QFont("Roboto", 12))
    win = MainWindow()
    win.show()
    win.raise_window()
    sys.exit(qapp.exec_())
