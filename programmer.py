import os
import serial
from crc import CrcCalculator, Crc8
from time import sleep

from socket import Socket
from command import SendCommand, SendData, SendAddress, RecvData
from command import commands as CMD

PAGE_SIZE = 128


def write(path: str, s: Socket) -> None:
    file = os.stat(path)
    file_size = file.st_size

    address = 0
    iteration = 0
    crc_calculator = CrcCalculator(Crc8.CCITT)

    SendCommand(s, CMD.HELLO).execute()
    SendCommand(s, CMD.ERASE).execute()

    with open(path, 'rb') as f:
        stop = False

        while not stop:
            data = f.read(PAGE_SIZE)

            if len(data) < PAGE_SIZE:
                stop = True
                data += bytearray([255] * (PAGE_SIZE - len(data)))

            SendAddress(s).execute(address)

            while True:
                SendData(s).execute(data)
                SendCommand(s, CMD.WRITE).execute()
                SendCommand(s, CMD.READ).execute()
                recv_data = RecvData(s).execute(PAGE_SIZE)

                if crc_calculator.calculate_checksum(recv_data) == crc_calculator.calculate_checksum(data):
                    break

            address += PAGE_SIZE

            print(iteration, (file_size / PAGE_SIZE) - iteration)
            iteration += 1


def read(path: str, flash_size: int, s: Socket) -> None:
    address = 0
    iteration = 0
    alrady_read = 0

    SendCommand(s, CMD.HELLO).execute()

    with open(path, 'wb') as f:
        while alrady_read < flash_size:
            SendAddress(s).execute(address)
            SendCommand(s, CMD.READ).execute()
            address += PAGE_SIZE
            recv_data = RecvData(s).execute(PAGE_SIZE)
            f.write(recv_data)

            print(iteration, (flash_size / PAGE_SIZE) - iteration)
            iteration += 1
            alrady_read += PAGE_SIZE


if __name__ == '__main__':
    serial_sock = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
    sock = Socket(serial_sock)

    # write('u-boot.bin', sock)
    read('u-boot_r.bin', 232192, sock)
