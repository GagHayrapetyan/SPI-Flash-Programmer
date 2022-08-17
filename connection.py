from typing import Optional
import serial


class Connection:
    def __init__(self, serial_conn: serial.Serial) -> None:
        self._serial = serial_conn
        self._tries = 3

    def write(self, data: bytes) -> None:
        self._serial.write(data)
        self._serial.flush()

    def command(self, cmd: str) -> None:
        self.write(cmd.encode())

    def read(self, length: int) -> Optional[bytes]:
        data = b''
        tried = 0

        while len(data) < length and tried < self._tries:
            res = self._serial.read(length - len(data))

            if len(res) == 0:
                tried += 1
                continue

            data += res

        if len(data) != length:
            data = None

        return data

    def wait_for_msg(self, msg: str, max_length: int = 100) -> bool:
        data = b''

        while True:
            res = self._serial.read(len(msg) - len(data))

            if res == b'':
                continue

            max_length -= len(res)
            if max_length < 0:
                return False

            data = (data + res)[-len(msg):]

            if msg == data.decode():
                return True

        return False
