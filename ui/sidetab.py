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

from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, Qt, pyqtSignal


class TabButton(QtWidgets.QPushButton):
    on_clicked = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(TabButton, self).__init__(*args, **kwargs)
        self.clicked.connect(lambda: self.on_clicked.emit(self.text()))


class SideTab(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(SideTab, self).__init__()
        self.setParent(parent)
        self.setWidgetResizable(True)
        self.setObjectName("sidetab")

        self.scrollwidget = QtWidgets.QWidget()
        self.scrollwidget.setObjectName("scrolltabwidget")
        self.verticalScrollBar().setObjectName("tabscrollbar")
        self.widgetLayout = QtWidgets.QVBoxLayout(self.scrollwidget)
        self.searchbar = QtWidgets.QLineEdit(self)
        self.tabs = {}

    def addTabs(self, tabNames, height=50):
        self.widgetLayout.addStretch()
        self.searchbar.setFixedHeight(35)
        self.searchbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.searchbar.setPlaceholderText("Search")
        self.widgetLayout.addWidget(self.searchbar)
        self.widgetLayout.addSpacing(14)
        for tabName in tabNames:
            tabButton = TabButton(tabName, self)
            tabButton.setFixedHeight(height)
            tabButton.setIconSize(QSize(25, 25))
            self.tabs[tabName] = tabButton
            self.widgetLayout.addWidget(tabButton)
        self.widgetLayout.addStretch()
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetLayout.setSpacing(0)
        self.setWidget(self.scrollwidget)
