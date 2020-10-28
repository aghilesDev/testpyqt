import queue


class QueueSingleton:

    queue_receive = None
    queue_send = None

    @classmethod
    def get_queue_receive(cls):
        if cls.queue_receive is None:
            cls.queue_receive = queue.Queue()
        return cls.queue_receive

    @classmethod
    def get_queue_send(cls):
        if cls.queue_send is None:
            cls.queue_send = queue.Queue()
        return cls.queue_send
