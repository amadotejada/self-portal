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
