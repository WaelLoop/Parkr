import serial



def trigger(input):

    arduinoData = serial.Serial('/dev/cu.usbmodem14401', 9600)

    # led1 off
    if input == 0:
        arduinoData.write('0'.encode())
    # led1 on
    elif input == 1:
        arduinoData.write('1'.encode())
    # led2 off
    elif input == 2:
        arduinoData.write('2'.encode())
    # led2 on
    elif input == 3:
        arduinoData.write('3'.encode())
    # led3 off
    elif input == 4:
        arduinoData.write('4'.encode())
    # led3 on
    elif input == 5:
        arduinoData.write('5'.encode())

