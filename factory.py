from dependency_injector import containers, providers
from logic.RunnableLogic import Worker
from logic.sendFrameLogic import SendFrameWorker
from DataLayer.repository import ControllerRepository
from singleton import QueueSingleton


class Container(containers.DeclarativeContainer):
    controller_repository = providers.Singleton(ControllerRepository)
    worker_logic = providers.Singleton(Worker, controller_repository=controller_repository)
    send_frame_logic = providers.Factory(SendFrameWorker)

