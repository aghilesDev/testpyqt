from dependency_injector import containers, providers
from DataLayer.serialManager import SerialManager
from DataLayer.MThread import MThread


class Container(containers.DeclarativeContainer):
    serialManager = providers.Factory(SerialManager)
    serialThread = providers.Factory(MThread)



