

from PyQt5.QtCore import QThread


class SerialThread(QThread):
    def run(self):
        self.exec()
