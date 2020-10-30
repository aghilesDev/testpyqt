from PyQt5 import QtWidgets, uic, QtSerialPort,QtCore
from PyQt5.QtCore import QThreadPool, pyqtSlot
from factory import Container
from DataLayer.serialManager import SerialManager
from DataLayer.SerialThread import SerialThread
import sys


class Ui(QtWidgets.QDialog):

    def __init__(self):
        container = Container()
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('./view/main.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.serialThread = SerialThread()
        self.serialManager = SerialManager()
        self.serialManager.moveToThread(self.serialThread)
        self.serialManager.signal.readData.connect(self.display_data)
        self.text = self.findChild(QtWidgets.QLabel, 'label')
        self.frame = self.findChild(QtWidgets.QFrame, 'frameLabel')
        self.data_input = self.findChild(QtWidgets.QLineEdit, 'inputFrame')
        self.button = self.findChild(QtWidgets.QPushButton, 'sendFrameButton')
        self.button.clicked.connect(self.sendFrame)
        self.serialThread.start()

    @pyqtSlot(str)
    def receive(self):
        data = ""
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            data = data+text
            self.text.setText(text)

    @pyqtSlot()
    def sendFrame(self):
        print('sent')
        data = self.data_input.text()
        self.serialManager.signal.writeData.emit(data)

    @pyqtSlot(str)
    def display_data(self, data):
        print(data)
        self.text.setText(data)


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
# app.exec_() # Start the application
