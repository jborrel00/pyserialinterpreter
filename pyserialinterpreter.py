#notes on the program and the processes happening behind it:

#10 lines of communitcation total from Arduino to Pi
"""['\n', 'pick a side\r\n', 'left\r\n', 'Waiting for an ISO14443A Card ...\r\n', 'Hello \r\n', 'Laurence\r\n', 'next player log in\r\n', 'Hello \r\n', 'Rob\r\n', 'You may only have 2 players at a time\r\n']"""
#the important pieces of info are: which side (assigned to first sign-in), who's the first sign-in an who's the second
#this is lines s[2], s[5] and s[8]

#important pieces of info for sending hex data to pi for comparison against a database are, side and players (in hex)
#s[2], s[4], s[8]
#just the hex data can be removed from these dictionaries by saving them as their own variable and then selecting the desired characters - [0:47], contains all 16 bits of info from the card
"""if you're off and there is serial output that would've already been sent,
were the Arduino not attached to the Pi, it will show up the next time you call
ser.readline() until you clear that old text out"""

################################################################################

import serial
import MySQLdb as mysqldb
import glob
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from time import sleep
class HD44780:

    def __init__(self, pin_rs=26, pin_e=24, pins_db=[22, 18, 16, 12]): #pins db provide data writing, all other connections are for power

        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=pins_db

        GPIO.setmode(GPIO.BOARD)
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
a=1
while a==1:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(5,GPIO.OUT)
    GPIO.output(5,1) 
    sleep(.1)
    GPIO.output(5,0)
    sleep(.1)
    GPIO.output(5,1) #start high to allow arduino to run program
    sleep(.1)
    dev = glob.glob('/dev/tty*')
    if '/dev/ttyACM1' in dev:
    ser = serial.Serial('/dev/ttyACM1',115200)
    else:
    	ser = serial.Serial('/dev/ttyACM0',115200)
    print "ready"
    s=[]#array that will hold the Serial output
    for i in range(11):
        r=ser.readline()
        print r #for serial output debugging
        s.append(r)
        if __name__ == '__main__':
            lcd = HD44780()
            lcd.message(str(r))
    #print "successfully read"
    if s[1]=='left\r\n' or 'right\r\n':
        if s[5]=='Laurence\r\n' or'Rob\r\n' or 'Joe\r\n' or 'James\r\n' or 'Sloan\r\n' or 'Joelle\r\n' or 'Bob\r\n' or 'Christina\r\n' or 'Colleen\r\n' or 'Nae\r\n':
            if s[9]=='Laurence\r\n' or'Rob\r\n' or 'Joe\r\n' or 'James\r\n' or 'Sloan\r\n' or 'Joelle\r\n' or 'Bob\r\n' or 'Christina\r\n' or 'Colleen\r\n' or 'Nae\r\n':
                if s[5]==s[9]:
                    print 'You cannot play yourself!'
                    a=2
                else:
                    print s[5]+" & "+s[9]+" are playing a game. "+s[5]+" is on the "+s[1]
                    if __name__ == '__main__':
                        lcd = HD44780()
                        lcd.message(str(s[5])+"\2 versus \3"+str(s[9])+"\4 ***")
                        print "message sent to lcd"
    p1=s[3]
    p2=s[7]
    p1h=p1[0:47]
    p2h=p2[0:47]
    print "player 1  hex code: ", p1h
    print "player 2 hex code: ", p2h
    if s[2] != 'Waiting for an ISO14443A Card ...\r\n' or s[10] != 'You may only have 2 players at a time\r\n':
        print s
        print 'invalid read, please try again'
        GPIO.output(5,0)
        sleep(.1)
        GPIO.output(5,1)
        print 'program reset, please try again'
    else:
        a=2
print 'program end'

