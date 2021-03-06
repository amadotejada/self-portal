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

# noinspection PyUnresolvedReferences
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot


class TaskManager(QThreadPool):
    def __init__(self):
        super(TaskManager, self).__init__()


class TaskSignals(QObject):
    pass


class Task(QRunnable):
    def __init__(self):
        super(Task, self).__init__()

    @pyqtSlot()
    def run(self) -> None:
        pass
