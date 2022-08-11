import serial

CMD_ERASE = 'e'
CMD_READ = 'r'
CMD_WRITE = 'w'
CMD_BUFFER_LOAD = 'l'
CMD_BUFFER_STORE = 's'


class Programmer:
    def __init__(self, port: str, baud_rate: int, page_size: int) -> None:
        self._arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)
        self._page_size = page_size

    def _command(self, cmd: str) -> None:
        self._arduino.write(cmd)
        self._arduino.flush()

    def erase(self) -> None:
        self._command(CMD_ERASE)

