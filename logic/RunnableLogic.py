from DataLayer.Gateway import run
import threading
from singleton import QueueSingleton
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from DataLayer.repository import ControllerRepository, UIRepository


class WorkerSignals(QObject):
    result = pyqtSignal(object)


class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, controller_repository: ControllerRepository):
        super(Worker, self).__init__()
        self.frameSignal = WorkerSignals()
        self.controllerRepository = controller_repository
        self.uiRepository = UIRepository(self.frameSignal.result)

    @pyqtSlot()
    def run(self):
        frame_list = QueueSingleton.get_queue_receive()
        threading.Thread(target=run, args=(frame_list,)).start()
        while True:
            data = self.controllerRepository.get_data()
            print("Frame received: ")
            if data is not None:
                self.uiRepository.send_data(data)
                print("ok")
