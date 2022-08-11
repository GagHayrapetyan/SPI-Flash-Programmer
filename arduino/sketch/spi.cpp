#include "spi_flash.h"


SPIFlash::SPIFlash(byte cs_pin) : _cs_pin(cs_pin) {

}


void SPIFlash::initialize() {
    pinMode(_cs_pin, OUTPUT);
    _unselect();
    SPI.begin();
}


void SPIFlash::_select() const {
    noInterrupts();
    digitalWrite(_cs_pin, LOW);
}


void SPIFlash::_unselect() const {
    digitalWrite(_cs_pin, HIGH);
    interrupts();
}


void SPIFlash::_command(byte cmd, boolean is_write) {
    if (is_write) {
        _command(SPIFLASH_WRITEENABLE);
        _unselect();
    }

    while (_busy());
    _select();
    SPI.transfer(cmd);
}


boolean SPIFlash::_busy() {
    return _read_status() & 1;
}


byte SPIFlash::_read_status() {
    _select();
    SPI.transfer(SPIFLASH_STATUSREAD);
    byte status = SPI.transfer(0);
    _unselect();
    return status;
}


void SPIFlash::chip_erase() {
    _command(SPIFLASH_CHIPERASE, true);
    _unselect();
    _busy();
}


uint32_t SPIFlash::read_bytes(uint32_t addr, void *buf, uint16_t len) {
    uint32_t trust_len  = min(len, PAGE_SIZE);

    _command(SPIFLASH_ARRAYREAD);
    SPI.transfer(addr >> 16);
    SPI.transfer(addr >> 8);
    SPI.transfer(addr);
    SPI.transfer(0);

    for (uint16_t i = 0; i < len; ++i)
        ((uint8_t *) buf)[i] = SPI.transfer(0);

    _unselect();

    return trust_len;
}

byte SPIFlash::read_byte(uint32_t addr) {
    _command(SPIFLASH_ARRAYREADLOWFREQ);
    SPI.transfer(addr >> 16);
    SPI.transfer(addr >> 8);
    SPI.transfer(addr);
    byte result = SPI.transfer(0);
    _unselect();

    return result;
}

void SPIFlash::write_byte(uint32_t addr, byte value) {
    _command(SPIFLASH_BYTEPAGEPROGRAM, true);  // Byte/Page Program
    SPI.transfer(addr >> 16);
    SPI.transfer(addr >> 8);
    SPI.transfer(addr);
    SPI.transfer(value);
    _unselect();
}

uint32_t SPIFlash::write_bytes(uint32_t addr, const void *buf, byte len) {
    uint32_t trust_len  = min(len, PAGE_SIZE);

    _command(SPIFLASH_BYTEPAGEPROGRAM, true);  // Byte/Page Program
    SPI.transfer(addr >> 16);
    SPI.transfer(addr >> 8);
    SPI.transfer(addr);

    for (uint8_t i = 0; i < trust_len; i++)
        SPI.transfer(((byte *) buf)[i]);

    _unselect();

    return trust_len;
}





