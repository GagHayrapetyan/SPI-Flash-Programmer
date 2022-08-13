from typing import Optional

import command.command as CMD
from command.interface import CommandInterface, Socket


class SendCommand(CommandInterface):
    def __init__(self, sock: Socket, cmd: str) -> None:
        self._cmd = cmd
        super().__init__(sock)

    def execute(self):
        self._sock.command(self._cmd)
        self._sock.wait_for_msg(self._cmd)


class SendAddress(CommandInterface):
    def execute(self, address: int):
        self._sock.command(CMD.SEND_ADDRESS)
        self._sock.write(address.to_bytes(4, byteorder='big'))
        self._sock.wait_for_msg(CMD.SEND_ADDRESS)


class SendData(CommandInterface):
    def execute(self, data: bytes):
        self._sock.command(CMD.SEND_DATA)
        self._sock.write(data)
        self._sock.wait_for_msg(CMD.SEND_DATA)


class RecvData(CommandInterface):
    def execute(self) -> Optional[bytes]:
        self._sock.command(CMD.RECV_DATA)
        data = self._sock.read_page()
        self._sock.wait_for_msg(CMD.RECV_DATA)

        return data
