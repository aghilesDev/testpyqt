from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool, pyqtSlot
from factory import Container
import sys


class Ui(QtWidgets.QDialog):

    def __init__(self):
        container = Container()
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('./view/main.ui', self) # Load the .ui file
        self.show() # Show the GUI
        worker = Container.worker_logic()
        worker.frameSignal.result.connect(self.display_data)
        self.thread = QThreadPool()
        self.thread.start(worker)
        self.text = self.findChild(QtWidgets.QLabel, 'label')
        self.frame = self.findChild(QtWidgets.QFrame, 'frameLabel')
        self.data_input = self.findChild(QtWidgets.QLineEdit, 'inputFrame')
        self.button = self.findChild(QtWidgets.QPushButton, 'sendFrameButton')
        self.button.clicked.connect(self.sendFrame)

    def sendFrame(self):
        print('sent')
        data = self.data_input.text()
        self.thread.start(Container.send_frame_logic(data))

    @pyqtSlot(object)
    def display_data(self, data):
        print(data)
        self.text.setText(data)


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
# app.exec_() # Start the application
