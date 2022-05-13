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

    def addApp(self, app):
        self.widgetLayout.addWidget(app)
        self.widgetLayout.setSpacing(5)
        self.setWidget(self.scrollwidget)
