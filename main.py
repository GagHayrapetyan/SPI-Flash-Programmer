import argparse
import serial
import serial.tools.list_ports as list_ports

from connection import Connection
from commands import EraseCMD
from programmer import (
    ProgrammerRead,
    ProgrammerWrite,
    ProgrammerChipErase
)


def print_com_ports():
    print('Available COM ports:')

    for i, port in enumerate(list_ports.comports()):
        print('%d: %s' % (i + 1, port.device))

    print('Done')


def main():
    def hex_dec(x):
        return int(x, 0)

    parser = argparse.ArgumentParser(description='Interface with an Arduino-based SPI flash programmer')
    parser.add_argument('-d', dest='device', default='COM1', help='serial port to communicate with')
    parser.add_argument('-f', dest='filename', default='flash.bin', help='file to read from / write to')
    parser.add_argument('-l', type=hex_dec, dest='length', default=128, help='length to read/write in bytes')

    parser.add_argument('--flash-offset', type=hex_dec, dest='flash_offset', default=0,
                        help='offset for flash read/write/erase in bytes')
    parser.add_argument('--file-offset', type=hex_dec, dest='file_offset', default=0,
                        help='offset for file read/write in bytes')
    parser.add_argument('--rate', type=int, dest='baud_rate', default=115200, help='baud-rate of serial connection')

    parser.add_argument('command', choices=('ports', 'write', 'read', 'chip_erase', 'erase_4K', 'erase_32K', 'erase_64K'),
                        help='command to execute')

    args = parser.parse_args()
    if args.command == 'ports':
        print_com_ports()
        return

    ser = None
    try:
        ser = serial.Serial(port=args.device, baudrate=args.baud_rate, timeout=1)
    except serial.SerialException:
        print('Could not connect to serial port %s' % args.device)

    conn = Connection(ser)

    if args.command == 'write':
        ProgrammerWrite(conn).execute(args.filename, args.flash_offset, args.file_offset)
    elif args.command == 'read':
        ProgrammerRead(conn).execute(args.filename, args.flash_offset, args.length)
    elif args.command == 'chip_erase':
        ProgrammerChipErase(conn, EraseCMD.ALL).execute(args.flash_offset)
    elif args.command == 'erase_4K':
        ProgrammerChipErase(conn, EraseCMD.K4).execute(args.flash_offset)
    elif args.command == 'erase_32K':
        ProgrammerChipErase(conn, EraseCMD.K32).execute(args.flash_offset)
    elif args.command == 'erase_64K':
        ProgrammerChipErase(conn, EraseCMD.K64).execute(args.flash_offset)


if __name__ == '__main__':
    main()
