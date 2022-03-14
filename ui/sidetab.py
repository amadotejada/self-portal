from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt


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
        self.searchbar.setAlignment(Qt.AlignCenter)
        self.searchbar.setPlaceholderText("Search")
        self.widgetLayout.addWidget(self.searchbar)
        self.widgetLayout.addSpacing(14)
        for tabName in tabNames:
            tabButton = QtWidgets.QPushButton(tabName, self)
            tabButton.setFixedHeight(height)
            tabButton.setIconSize(QSize(25, 25))
            self.tabs[tabName] = tabButton
            self.widgetLayout.addWidget(tabButton)
        self.widgetLayout.addStretch()
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetLayout.setSpacing(0)
        self.setWidget(self.scrollwidget)
