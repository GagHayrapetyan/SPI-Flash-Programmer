//
// Created by Gag Hayrapetyan on 11.08.2022.
//

#if ARDUINO >= 100
#include <Arduino.h>
#else
#include <wiring.h>
#include "pins_arduino.h"
#endif

#include <SPI.h>

#ifndef SPI_FLASH_PROGRAMMER_SPI_H
#define SPI_FLASH_PROGRAMMER_SPI_H

#define PAGE_SIZE 128

#define SPIFLASH_WRITEENABLE      0x06        // write enable
#define SPIFLASH_WRITEDISABLE     0x04        // write disable
#define SPIFLASH_BLOCKERASE_4K    0x20        // erase one 4K block of flash memory
#define SPIFLASH_BLOCKERASE_32K   0x52        // erase one 32K block of flash memory
#define SPIFLASH_BLOCKERASE_64K   0xD8        // erase one 64K block of flash memory
#define SPIFLASH_CHIPERASE        0x60        // chip erase (may take several seconds depending on size)

// but no actual need to wait for completion (instead need to check the status register BUSY bit)
#define SPIFLASH_STATUSREAD       0x05        // read status register
#define SPIFLASH_STATUSWRITE      0x01        // write status register
#define SPIFLASH_ARRAYREAD        0x0B        // read array (fast, need to add 1 dummy byte after 3 address bytes)
#define SPIFLASH_ARRAYREADLOWFREQ 0x03        // read array (low frequency)
#define SPIFLASH_SLEEP            0xB9        // deep power down
#define SPIFLASH_WAKE             0xAB        // deep power wake up
#define SPIFLASH_BYTEPAGEPROGRAM  0x02        // write (1 to 256bytes)
#define SPIFLASH_IDREAD           0x9F        // read JEDEC manufacturer and device ID (2 bytes, specific bytes for each manufacturer and device)


class SPIFlash {
private:
    byte _cs_pin; // chip select

    void _select() const;

    void _unselect() const;

    void _command(byte cmd, boolean is_write = false);

    boolean _busy();

    byte _read_status();

public:
    SPIFlash(byte cs_pin);

    void initialize();

    void chip_erase();

    byte read_byte(uint32_t addr);

    uint32_t read_bytes(uint32_t addr, void *buf, uint16_t len);

    void write_byte(uint32_t addr, byte value);

    uint32_t write_bytes(uint32_t addr, const void *buf, byte len);

};

#endif //SPI_FLASH_PROGRAMMER_SPI_H
