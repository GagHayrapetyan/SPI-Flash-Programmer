from socket import Socket
from abc import ABC, abstractmethod


class CommandInterface(ABC):
    def __init__(self, sock: Socket) -> None:
        self._sock = sock

    def wait_for_response(self, msg: str) -> None:
        if not self._sock.wait_for_msg(msg):
            raise 'Failed'

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
