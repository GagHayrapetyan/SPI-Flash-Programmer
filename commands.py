from typing import Optional
from abc import ABC, abstractmethod

from connection import Connection

CMD_HELLO = 'h'
CMD_SEND_ADDRESS = 'a'
CMD_SEND_DATA = 's'
CMD_RECV_DATA = 'r'
CMD_READ = 'd'
CMD_WRITE = 'w'
CMD_ERASE = 'e'
CMD_ERASE_4K = 'b'
CMD_ERASE_32K = 'v'
CMD_ERASE_64K = 'n'


class CommandInterface(ABC):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def _wait_for_response(self, msg: str) -> None:
        if not self._conn.wait_for_msg(msg):
            raise 'Failed'

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class SendCommand(CommandInterface):
    def __init__(self, sock: Connection, cmd: str) -> None:
        self._cmd = cmd
        super().__init__(sock)

    def execute(self):
        self._conn.command(self._cmd)
        self._wait_for_response(self._cmd)


class SendAddress(CommandInterface):
    def execute(self, address: int):
        self._conn.command(CMD_SEND_ADDRESS)
        self._conn.write(address.to_bytes(4, byteorder='little'))
        self._wait_for_response(CMD_SEND_ADDRESS)


class SendData(CommandInterface):
    def execute(self, data: bytes):
        self._conn.command(CMD_SEND_DATA)
        self._conn.write(data)
        self._wait_for_response(CMD_SEND_DATA)


class RecvData(CommandInterface):
    def execute(self, length: int) -> Optional[bytes]:
        self._conn.command(CMD_RECV_DATA)
        data = self._conn.read(length)
        self._wait_for_response(CMD_RECV_DATA)

        return data
