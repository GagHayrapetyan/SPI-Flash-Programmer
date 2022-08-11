#include "spi.h"


#define CMD_ERASE 'e'
#define CMD_READ 'r'
#define CMD_WRITE 'w'
#define CMD_BUFFER_LOAD 'l'
#define CMD_BUFFER_STORE 's'


#define SERIAL_BAUD 115200

SPIFlash flash(8);
byte buf[1024];


void setup() {
    Serial.begin(SERIAL_BAUD);
    Serial2.begin(SERIAL_BAUD);
    while (!Serial2) delay(100);

    pinMode(SS, OUTPUT);
    digitalWrite(SS, HIGH);
    flash.initialize();

    delay(1000);
}

void loop() {

    while (Serial2.available() == 0) {

    }

    int cmd = Serial2.read();
    switch (cmd) {
        case CMD_ERASE:
            Serial.println('CMD_ERASE');
            break;

        case CMD_READ:
            break;

        case CMD_WRITE:
            break;

        case CMD_BUFFER_LOAD:
            break;

        case CMD_BUFFER_STORE:
            break;

        default:
            break;
    }
}