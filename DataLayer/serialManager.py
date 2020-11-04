from PyQt5.QtCore import QObject, QIODevice, pyqtSlot, pyqtSignal, QTimer
from PyQt5 import QtSerialPort
from DataLayer.MThread import MThread


class SerialInterface(QObject):
    readData = pyqtSignal(str)
    writeData = pyqtSignal(str)
    connect = pyqtSignal()
    close = pyqtSignal()


class SerialManager(QObject):

    def __init__(self):
        super(SerialManager, self).__init__()
        self.serial = QtSerialPort.QSerialPort("/dev/pts/2", baudRate=QtSerialPort.QSerialPort.Baud115200, readyRead= self.receive)
        #self.serial.error.connect(self.error)
        self.serial.errorOccurred.connect(self.error)
        self.signal = SerialInterface()
        self.signal.writeData.connect(self.on_write_data)
        self.signal.connect.connect(self.connect)
        self.isConnected = False

    @pyqtSlot(QtSerialPort.QSerialPort.SerialPortError)
    def error(self, data: int):
        if (data == 9 or data == 8 or data == 1) and self.isConnected:
            print("ERROR occured: {}".format(data))
            self.isConnected = False
            self.serial.close()
            self.connect()

    @pyqtSlot()
    def connect(self):
        if not self.serial.open(QIODevice.ReadWrite):
            QTimer.singleShot(3000, self.connect)
            print("error")
        else:
            self.isConnected = True

    @pyqtSlot()
    def close(self):
        print("serial closed")
        self.serial.close()

    @pyqtSlot()
    def receive(self):
        print("maybe here")
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            self.signal.readData.emit(text)

    def moveToThread(self, thread: MThread) -> None:
        super(SerialManager, self).moveToThread(thread)
        self.serial.moveToThread(thread)
        self.signal.moveToThread(thread)
        thread.signals.aboutToStop.connect(self.close)


    @pyqtSlot(str)
    def on_write_data(self, data):
            print("write data: {}".format(data))
            self.serial.write(data.encode())

