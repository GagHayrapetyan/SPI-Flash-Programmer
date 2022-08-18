#include <SPIFlash.h>

#define SERIAL_RATE 115200
#define PAGE_SIZE 128

#define COMMAND_HELLO 'h'
#define COMMAND_SEND_ADDRESS 'a'
#define COMMAND_SEND_DATA 's'
#define COMMAND_RECV_DATA 'r'
#define COMMAND_READ 'd'
#define COMMAND_WRITE 'w'
#define COMMAND_ERASE 'e'
#define COMMAND_ERASE_4K 'b'
#define COMMAND_ERASE_32K 'v'
#define COMMAND_ERASE_64K 'n'


byte read_socket();
uint32_t get_address();
void get_data();
void print_data();
void post_data();


byte data[PAGE_SIZE];
uint32_t address=0;

uint16_t expectedDeviceID=0xEF30;
SPIFlash flash(8, expectedDeviceID);


void setup() {
  Serial2.begin(SERIAL_RATE);
  Serial.begin(SERIAL_RATE);

  while (!Serial || !Serial2);

  flash.initialize();

  // put your setup code here, to run once:

}

void loop() {
  while(Serial2.available() == 0);

  int cmd = Serial2.read();

  Serial.print("command: ");
  Serial.println(char(cmd));
  switch(cmd) {
     case COMMAND_HELLO:
       Serial2.print(COMMAND_HELLO);
       break;

     case COMMAND_SEND_ADDRESS:
       address = get_address();
       Serial2.print(COMMAND_SEND_ADDRESS);
       break;

     case COMMAND_SEND_DATA:
       get_data();
       Serial2.print(COMMAND_SEND_DATA);
       break;

     case COMMAND_RECV_DATA:
      post_data();
      Serial2.print(COMMAND_RECV_DATA);
      break;

     case COMMAND_ERASE:
      flash.chipErase();
      while(flash.busy());
      Serial2.print(COMMAND_ERASE);
      break;

     case COMMAND_ERASE_4K:
      flash.blockErase4K(address);
      while(flash.busy());
      Serial2.print(COMMAND_ERASE);
      break;

     case COMMAND_ERASE_32K:
      flash.blockErase32K(address);
      while(flash.busy());
      Serial2.print(COMMAND_ERASE);
      break;

     case COMMAND_ERASE_64K:
      flash.blockErase64K(address);
      while(flash.busy());
      Serial2.print(COMMAND_ERASE);
      break;


     case COMMAND_READ:
      memset(data, 0, PAGE_SIZE);
      flash.readBytes(address, data, PAGE_SIZE);
      Serial2.print(COMMAND_READ);
      break;

     case COMMAND_WRITE:
     flash.writeBytes(address, data, PAGE_SIZE);
     Serial2.print(COMMAND_WRITE);
      break;

  }

}


byte read_socket(){
  while(Serial2.available() == 0);

  return Serial2.read();
}

uint32_t get_address(){
  byte address_raw[4];

  for(int i=0;i<4;i++){
    address_raw[i]=read_socket();
  }

  return (address_raw[3] << 24) | (address_raw[2] << 16) | (address_raw[1] << 8) | (address_raw[0]);
}

void get_data(){
  for(int i=0;i<PAGE_SIZE;i++){
    data[i]=read_socket();
  }
}


void print_data(){
  for(int i=0;i<PAGE_SIZE;i++){
    Serial.println(data[i]);
  }

}

void post_data(){
  for(int i=0;i<PAGE_SIZE;i++){
    Serial2.write(data[i]);
  }
}