import serial
from connection import Connection
from programmer import ProgrammerChipErase, ProgrammerWrite, ProgrammerRead

if __name__ == '__main__':
    serial_conn = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
    conn = Connection(serial_conn)

    # print('Erase')
    # ProgrammerChipErase(conn).execute()
    # print('Loader')
    # ProgrammerWrite(conn).execute('iW_RainboW_G22M_SPI_LOADER_V020_DDR3.bin', 0)
    # print('U-boot')
    # ProgrammerWrite(conn).execute('u-boot.bin', 131072)

    ProgrammerRead(conn).execute('new.bin', 0, 1 << 21)
