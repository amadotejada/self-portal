from PyQt5 import QtWidgets
from .flowlayout import FlowLayout


class Scrollable(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(Scrollable, self).__init__()
        self.setParent(parent)
        self.setWidgetResizable(True)
        self.setObjectName("scrollable")

        self.scrollwidget = QtWidgets.QWidget()
        self.scrollwidget.setObjectName("scrollablewidget")
        self.verticalScrollBar().setObjectName("scrollablescrollbar")
        self.widgetLayout = FlowLayout(self.scrollwidget)

    def addApp(self, tabButton, bottomButton=None, height=50):
        self.widgetLayout.addWidget(tabButton)
        self.widgetLayout.setSpacing(5)
        self.setWidget(self.scrollwidget)
