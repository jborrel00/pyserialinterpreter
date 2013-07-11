#notes on the program and the processes happening behind it:

#10 lines of communitcation total from Arduino to Pi
"""if you're off and there is serial output that would've already been sent,
were the Arduino not attached to the Pi, it will show up the next time you call
ser.readline() until you clear that old text out"""

################################################################################

import serial
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from time import sleep
class HD44780:

    def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18]): #pins db provide data writing, all other connections are for power

        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=pins_db

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT) #sets up each GPIO pin to digitalWrite out

        self.clear()

    def clear(self):
        """ Blank / Reset LCD """

        self.cmd(0x33) # $33 8-bit mode
        self.cmd(0x32) # $32 8-bit mode
        self.cmd(0x28) # $28 8-bit mode
        self.cmd(0x0C) # $0C 8-bit mode
        self.cmd(0x06) # $06 8-bit mode
        self.cmd(0x01) # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)


        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def message(self, text):
        """ Send string to LCD."""

        for char in text:
            if char == '\2':
                self.cmd(0xC0) #2nd line
            elif char == '\3':
                self.cmd(0x94) #3rd line
            elif char == '\4':
                self.cmd(0xD4) #4th line
            else:
                self.cmd(ord(char),True)
                
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
GPIO.output(5,1) 
sleep(.1)
GPIO.output(5,0)
sleep(.1)
GPIO.output(5,1) #start high to allow arduino to run program
sleep(.1)
ser = serial.Serial('/dev/ttyACM0',115200)#can also be ACM1
#would like to be able to address that at some point and allow the program to check for both options without returning an error for the wrong one
print "ready"
s=[]#array that will hold the Serial output
for i in range(10):
    r=ser.readline()
    s.append(r)
print "successfully read"
if s==['\n', 'pick a side\r\n', 'left\r\n', 'Waiting for an ISO14443A Card ...\r\n', 'Hello \r\n', 'Laurence\r\n', 'next player log in\r\n', 'Hello \r\n', 'Rob\r\n', 'You may only have 2 players at a time\r\n']:
    print "Laurence & Rob are playing a game. Laurence is on the left and Rob is on the right."
    if __name__ == '__main__':
        lcd = HD44780()
        lcd.message(" Laurence v. Rob\2 Laurence(Left)\3 versus\4 Rob(Right)")
        print "message sent to lcd"
"""GPIO.output(5,0) #resetting to ensure proper Serial display
sleep(.1)
GPIO.output(5,1)
sleep(.1)"""
