# Importing Libraries
import serial
import time
DEFAULT_BAUDRATE = 115200
arduino = serial.Serial(port='COM5', baudrate=DEFAULT_BAUDRATE, timeout=.1)
def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))
    time.sleep(0.005)
    data = arduino.readline()
    return data
    
def write_arduino(x):
    arduino.write(bytes(str(x), "utf-8"))
    time.sleep(0.05)
