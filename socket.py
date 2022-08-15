from typing import Optional, Union
import serial


class Socket:
    def __init__(self, sock: serial.Serial) -> None:
        self._sock = sock
        self._tries = 3

    def write(self, data: bytes) -> None:
        self._sock.write(data)
        self._sock.flush()

    def command(self, cmd: str) -> None:
        self.write(cmd.encode())

    def read(self, length: int) -> Optional[bytes]:
        data = b''
        tryed = 0

        while len(data) < length and tryed < self._tries:
            res = self._sock.read(length - len(data))

            if len(res) == 0:
                tryed += 1
                continue

            data += res

        if len(data) != length:
            return None

        return data

    def wait_for_msg(self, msg: str, max_length: int = 100) -> bool:
        data = b''

        while True:
            res = self._sock.read(len(msg) - len(data))

            if res == b'':
                continue

            max_length -= len(res)
            if max_length < 0:
                return False

            data = (data + res)[-len(msg):]

            if msg == data.decode():
                return True

        return False
