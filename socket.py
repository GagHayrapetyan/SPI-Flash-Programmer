from typing import Optional, Union
import serial


class Socket:
    def __init__(self, sock: serial.Serial, page_size: int) -> None:
        self._sock = sock
        self._page_size = page_size
        self._tries = 3

    def write(self, msg: bytes) -> None:
        self._sock.write(msg)
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

    def wait_for_msg(self, msg: str, max_lenght: int = 100) -> bool:
        data = b''

        while True:
            res = self.read(len(msg) - len(data))

            if max_lenght <= 0 or res is None:
                return False
            else:
                max_lenght -= len(res)

            data = (data + res)[-len(msg):]

            if msg == data.decode():
                return True
