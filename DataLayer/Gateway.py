from DataLayer.serialHandler import SerialHandler
import asyncio
from singleton import QueueSingleton
import concurrent.futures

list_queue=None
#make a file for ip Server and ip in config directory
ip="http://127.0.0.1/"

serialData = None
#with open("../config/serialContextConfig.json", "r") as file:
 #   serialData=json.load(file)
serialData = {"path": "/dev/pts/4",
              "option": {
                  "baudRate": 115200
                  }
              }

serialHandler = SerialHandler(serialData)


def read_data_to_receive(receiveList, data):
    receiveList.put(data)


async def sendToServer(data, receiveList=QueueSingleton.get_queue_receive()):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        await loop.run_in_executor(
            pool, read_data_to_receive, receiveList, data)


def read_data_to_send(sendList):
    print('sednding data')
    data = sendList.get()
    return data

async def sendToController(sendList):
    loop = asyncio.get_running_loop()
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            result = await loop.run_in_executor(
                pool, read_data_to_send, sendList)
            await serialHandler.sendSerialData(result)


async def main(frames):
    global list_queue
    list_queue = QueueSingleton.get_queue_receive()
    # set serial listner
    await serialHandler.setSerialListner(sendToServer)
    await serialHandler.serialConnect()
    print('Test passed')
    send_queue = QueueSingleton.get_queue_send()
    task1 = asyncio.create_task(sendToController(send_queue))
    task2 = asyncio.create_task(serialHandler.listenToSerial())
    await task1
    await task2


def run(frames):
    asyncio.run(main(frames))
