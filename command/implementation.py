from typing import Optional

import command.command as CMD
from command.interface import CommandInterface, Socket


class SendCommand(CommandInterface):
    def __init__(self, sock: Socket, cmd: str) -> None:
        self._cmd = cmd
        super().__init__(sock)

    def execute(self):
        self._sock.command(self._cmd)
        self.wait_for_response(self._cmd)


class SendAddress(CommandInterface):
    def execute(self, address: int):
        self._sock.command(CMD.SEND_ADDRESS)
        self._sock.write(address.to_bytes(4, byteorder='little'))
        self.wait_for_response(CMD.SEND_ADDRESS)


class SendData(CommandInterface):
    def execute(self, data: bytes):
        self._sock.command(CMD.SEND_DATA)
        self._sock.write(data)
        self.wait_for_response(CMD.SEND_DATA)


class RecvData(CommandInterface):
    def execute(self, length: int) -> Optional[bytes]:
        self._sock.command(CMD.RECV_DATA)
        data = self._sock.read(length)
        self.wait_for_response(CMD.RECV_DATA)

        return data
