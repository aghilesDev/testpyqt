from PyQt5.QtCore import QObject, QIODevice, pyqtSlot,pyqtSignal
from PyQt5 import QtSerialPort


class SerialInterface(QObject):
    readData = pyqtSignal(str)
    writeData = pyqtSignal(str)


class SerialManager(QObject):

    def __init__(self):
        super(SerialManager, self).__init__()
        self.serial = QtSerialPort.QSerialPort("/dev/pts/2", baudRate=QtSerialPort.QSerialPort.Baud115200, readyRead=self.receive)
        self.signal = SerialInterface()

        self.connect()
        self.signal.writeData.connect(self.on_write_data)

    def connect(self):
        print(self.serial.open(QIODevice.ReadWrite))

    @pyqtSlot()
    def receive(self):
        data = ""
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            data = data+text
            self.signal.readData.emit(text)

    def moveToThread(self, thread: 'QThread') -> None:
        super(SerialManager, self).moveToThread(thread)
        self.serial.moveToThread(thread)

    @pyqtSlot(str)
    def on_write_data(self,data):
        self.serial.write(data.encode())
