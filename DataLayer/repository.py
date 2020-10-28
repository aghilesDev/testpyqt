from singleton import QueueSingleton
class BaseControllerRepository:

    def __init__(self):
        pass

    def get_data(self):
        pass

    def send_data(self, data):
        pass


class ControllerRepository:

    def __init__(self):
        self.received_queue = QueueSingleton.get_queue_receive()
        self.send_queue = QueueSingleton.get_queue_send()

    def get_data(self):
        return self.received_queue.get()

    def send_data(self, data):
        self.send_queue.put(data)


class BaseUIRepository:

    def __init__(self):
        pass

    def get_data(self):
        pass

    def send_data(self, data):
        pass


class UIRepository(BaseUIRepository):

    def __init__(self, signal):
        self.signal = signal

    def get_data(self):
        pass

    def send_data(self, data):
        self.signal.emit(data)
        pass
