import os
import math
from abc import ABC, abstractmethod
from enum import Enum

from tqdm import tqdm
from crc import CrcCalculator, Crc8

from connection import Connection
from commands import (
    SendCommand,
    SendData,
    SendAddress,
    RecvData,

    CMD_HELLO,
    CMD_READ,
    CMD_WRITE,
    CMD_ERASE,
    CMD_ERASE_64K,
    CMD_ERASE_4K,
    CMD_ERASE_32K
)

PAGE_SIZE = 128


def get_file_size(file_path: str) -> int:
    file = os.stat(file_path)

    return file.st_size


class ProgrammerCommandInterface(ABC):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class EraseCMD(Enum):
    ALL = CMD_ERASE
    K4 = CMD_ERASE_4K
    K32 = CMD_ERASE_32K
    K64 = CMD_ERASE_64K


class ProgrammerChipErase(ProgrammerCommandInterface):
    def __init__(self, conn: Connection, cmd: EraseCMD) -> None:
        self._cmd = cmd
        super().__init__(conn)

    def execute(self, address: int = 0) -> None:
        pbar = tqdm(total=1)
        SendCommand(self._conn, CMD_HELLO).execute()
        SendAddress(self._conn).execute(address)
        SendCommand(self._conn, self._cmd.value).execute()
        pbar.update(1)
        pbar.close()


class ProgrammerWrite(ProgrammerCommandInterface):
    def __init__(self, conn: Connection) -> None:
        self._crc = CrcCalculator(Crc8.CCITT)
        self._stop_write = False
        self._address = 0

        self._cmd_hello = SendCommand(conn, CMD_HELLO)
        self._cmd_read = SendCommand(conn, CMD_READ)
        self._cmd_write = SendCommand(conn, CMD_WRITE)
        self._cmd_write_address = SendAddress(conn)
        self._cmd_write_data = SendData(conn)
        self._cmd_read_data = RecvData(conn)

        super().__init__(conn)

    def _read_file(self, file_path: str) -> None:
        pbar = tqdm(total=math.ceil(get_file_size(file_path) / PAGE_SIZE))

        with open(file_path, 'rb') as f:
            while not self._stop_write:
                data = f.read(PAGE_SIZE)
                self._write(data)

                pbar.update(1)
        pbar.close()

    def _write(self, data: bytes) -> None:
        data = self._correct_data(data)
        self._cmd_write_address.execute(self._address)
        self._try_write(data)
        self._address += PAGE_SIZE

    def _correct_data(self, data: bytes) -> bytes:
        if len(data) < PAGE_SIZE:
            self._stop_write = True
            data += bytearray([255] * (PAGE_SIZE - len(data)))

        return data

    def _try_write(self, data: bytes) -> None:
        while True:
            self._cmd_write_data.execute(data)
            self._cmd_write.execute()
            self._cmd_read.execute()
            recv_data = self._cmd_read_data.execute(PAGE_SIZE)

            if self._checksum(data, recv_data):
                break

    def _checksum(self, data: bytes, recv_data: bytes) -> bool:
        return self._crc.calculate_checksum(data) == self._crc.calculate_checksum(recv_data)

    def execute(self, file_path: str, address: int = 0) -> None:
        self._address = address
        self._cmd_hello.execute()
        self._read_file(file_path)


class ProgrammerRead(ProgrammerCommandInterface):
    def __init__(self, conn: Connection) -> None:
        self._crc = CrcCalculator(Crc8.CCITT)
        self._address = 0

        self._cmd_hello = SendCommand(conn, CMD_HELLO)
        self._cmd_read = SendCommand(conn, CMD_READ)
        self._cmd_write_address = SendAddress(conn)
        self._cmd_read_data = RecvData(conn)

        super().__init__(conn)

    def _write_file(self, file_path: str, length: int):
        pbar = tqdm(total=math.ceil(length / PAGE_SIZE))

        with open(file_path, 'wb') as f:
            while self._address < length:
                f.write(self._read())
                pbar.update(1)

        pbar.close()

    def _read(self) -> bytes:
        self._cmd_write_address.execute(self._address)
        data = self._try_read_block()
        self._address += PAGE_SIZE

        return data

    def _try_read_block(self) -> bytes:
        data = None

        while True:
            for i in range(3):
                self._cmd_read.execute()

                if data is None:
                    data = self._cmd_read_data.execute(PAGE_SIZE)
                    continue

                if not self._checksum(data, self._cmd_read_data.execute(PAGE_SIZE)):
                    data = None
                    break
            if data is not None:
                return data

    def _checksum(self, data: bytes, data_new: bytes) -> bool:
        return self._crc.calculate_checksum(data) == self._crc.calculate_checksum(data_new)

    def execute(self, file_path: str, address: int = 0, length: int = PAGE_SIZE) -> None:
        self._address = address
        self._cmd_hello.execute()
        self._write_file(file_path, length)
