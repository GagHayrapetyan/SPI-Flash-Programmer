[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/GagHayrapetyan/SPI-Flash-Programmer/blob/main/LICENSE)
# SPI Flash Programmer
Simple Arduino sketch and Python 3 client to program SPI flash chips.

## Usage 
 - Program the Arduino with sketch
 - Connect the SPI flash chip 
 - Run python client
 
## Arduino 
In the sketch, the output of CS is 8.

## Python client

### Requirements
```
pip install requirements.txt
```

### Command list
 | Commands | Description |
| :---: | :---: |
| ports | Listing serial ports | 
| write | Write flash | 
| read | Read flash | 
| chip_erase | Erase flash | 
| erase_4K | Erase flash 4K block | 
| erase_32K | Erase flash 32K block | 
| erase_64K | Erase flash 64K block | 

### Optional arguments
| Argument | Prefix | Description |
| :---: | :---: | :---: |
| device | -d | serial port to communicate with |
| filename | -f | file to read from / write to |
| length | -l | length to read/write in bytes |
| flash_offset | --flash-offset | offset for flash read/write/erase in bytes |
| file_offset | --file-offset | offset for file read/write in bytes |
| baud_rate | --rate | baud-rate of serial connection |

## Example
```
# Listing serial ports
python3 main.py ports

# Write flash
python3 main.py -d COM1 -f xXx.bin --flash_offset 0 --file_offset 0 write

# Read flash
python3 main.py -d COM1 -f xXx.bin --flash_offset 0 -l 4096 write

# Erase flash
python3 main.py -d COM1 erase
```
