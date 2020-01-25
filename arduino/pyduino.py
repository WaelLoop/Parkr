import serial


arduinoData = serial.Serial('com3', 9600)

def led_on():
    arduinoData.write('1'.encode())

def led_off():
    arduinoData.write('0'.encode())

def trigger(number):
    if number == 1:
        led_on()
    else:
        led_off()

if __name__ == '__main__':
    trigger(1)