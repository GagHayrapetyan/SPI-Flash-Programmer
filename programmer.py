from typing import Optional
import serial
from time import sleep

CMD_HELLO = '>'
CMD_POST_BUFFER = 'p'
CMD_POST_BUFFER_ADDRESS = 'a'
CMD_GET_BUFFER = 'g'


class Programmer:
    def __init__(self, port: str, baud_rate: int, page_size: int) -> None:
        self._arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)
        self._page_size = page_size
        self._tyies = 3

    def _command(self, cmd: str) -> None:
        self._arduino.write(cmd.encode())
        self._arduino.flush()

    def _read(self, length: int) -> Optional[bytes]:
        tryed = 0
        data = b''

        while len(data) < length and tryed < self._tyies:
            res = self._arduino.read(length - len(data))

            if len(res) == 0:
                tryed += 1
                continue

            data += res

        if len(data) != length:
            return None

        return data

    def _wait_for(self, msg: bytes, max_len: int = 100) -> bool:
        tryed = 0
        data = b''

        while tryed < self._tyies:
            res = self._arduino.read(max(len(msg) - len(data), 1))

            if len(res) == 0:
                tryed += 1
                continue

            max_len -= len(res)
            if max_len <= 0:
                return False

            data = (data + res)[-len(msg):]

            if msg == data:
                return True

        print(data)

        return False

    def _wait_for_msg(self, msg: str) -> bool:
        data = msg.encode()

        return self._wait_for(data)

    def hello(self):
        self._command(CMD_HELLO)

        if not self._wait_for_msg(CMD_HELLO):
            raise "blya"

        self._arduino.readall()

    def post_buffer_address(self, addres: int):
        self._command(CMD_POST_BUFFER_ADDRESS)
        self._arduino.write(addres)

        if not self._wait_for_msg(CMD_POST_BUFFER_ADDRESS):
            raise "blya"


    def post_buffer(self):
        self._command(CMD_POST_BUFFER + 'assds')

        if not self._wait_for_msg(CMD_POST_BUFFER):
            raise "blya"

    def get_buffer(self):
        self._command(CMD_GET_BUFFER)

        if not self._wait_for_msg(CMD_GET_BUFFER):
            raise "blya"

        data = self._read(5)
        print(data)
        if data is None:
            raise "blya"

        if not self._wait_for_msg(CMD_GET_BUFFER):
            raise "blya"


if __name__ == '__main__':
    p = Programmer('COM3', 115200, 128)

    p.hello()
    p.post_buffer_address(chr(11).encode())
    p.post_buffer_address(chr(22).encode())
