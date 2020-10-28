from DataLayer.Gateway import run
import threading
from singleton import QueueSingleton
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from DataLayer.repository import ControllerRepository, UIRepository

class WorkerSignals(QObject):
    result = pyqtSignal(object)

class SendFrameWorker(QRunnable):
    def __init__(self, data):
        super(SendFrameWorker, self).__init__()
        self.send_queue = QueueSingleton.get_queue_send()
        self.data = data

    @pyqtSlot()
    def run(self):
        print(self.data)
        self.send_queue.put(self.data)
