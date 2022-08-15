import serial
from socket import Socket
import command.command as CMD
from command.implementation import SendCommand, SendAddress, SendData, RecvData
from crc import CrcCalculator, Crc8

ser = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
s = Socket(ser)


def print_data(data: bytes):
    res = ''

    for i, b in enumerate(data):
        if i % 16 == 0:
            res += '\n'

        res += "%02x " % b

    print(res)


crc_calculator = CrcCalculator(Crc8.CCITT)

SendCommand(s, CMD.HELLO).execute()
SendAddress(s).execute(0)
d = bytearray(range(128))
SendData(s).execute(d)
SendCommand(s, CMD.WRITE).execute()
SendCommand(s, CMD.READ).execute()
x = RecvData(s).execute(128)

print_data(x)
print(crc_calculator.calculate_checksum(x) == crc_calculator.calculate_checksum(d))
