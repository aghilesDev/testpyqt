import asyncio
import aioserial




class BaseSerialHandler:
    def __init__(self, serialData):
        # init serial
        self.serialData = serialData
        ## initialization of the state of the serial connection
        self.serialIsConnected: bool = False
        self.serialIsConnecting: bool = False
        self.serial = None

        pass

    # serial methods:
    async def serialConnected(self):
        return self.serial is not None and self.serialIsConnected

    async def serialConnect(self):
        # init serial
        self.serialIsConnecting = True
        self.serialIsConnected = False
        while self.serialIsConnected == False:
            try:
                print("... Waiting for serial Connection to {}".format(self.serialData['path']))
                self.serial = aioserial.AioSerial(port=self.serialData['path'],
                                                  baudrate=self.serialData['option']['baudRate'])
                self.serialIsConnected = True
                self.serialIsConnecting = False
                print("... Serial Connected")
            except:
                print("Serial Connection Failed")
                self.serialIsConnected = False
                await asyncio.sleep(2)
        return

    async def listenToSerial(self):
        print("reader ready")
        while True:
            try:
                data = await self.serial.readline_async()
                if (self.callback != None):
                    await self.callback(data.decode("ascii"))
            except UnicodeDecodeError:
                print("Error Format Decode")
            except:
                print("Error connection ")
                self.serial.close()
                await self.serialConnect()

    async def setSerialListner(self, listner):
        self.callback = listner
        return

    async def sendSerialData(self, data):
        print("DATA FROM SERVER: {}".format(data))
        try:
            await self.serial.write_async(data.encode())
        except:
            print('Writing on serial port failed ...')
            await self.serialConnect()
        return




class SerialHandler(BaseSerialHandler):
    pass
