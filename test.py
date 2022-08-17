import serial
from connection import Connection
from programmer import ProgrammerErase, ProgrammerWrite

if __name__ == '__main__':
    serial_conn = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
    conn = Connection(serial_conn)

    print('Erase')
    ProgrammerErase(conn).execute()
    print('Loader')
    ProgrammerWrite(conn).execute('iW_RainboW_G22M_SPI_LOADER_V020_DDR3.bin', 0)
    print('U-boot')
    ProgrammerWrite(conn).execute('u-boot.bin', 131072)
