from socket import Socket
from abc import ABC, abstractmethod


class CommandInterface(ABC):
    def __init__(self, sock: Socket) -> None:
        self._sock = sock

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
