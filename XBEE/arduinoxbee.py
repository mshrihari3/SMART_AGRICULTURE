import serial
import time

port="/dev/ttyACM1"
serialFromArduino=serial.Serial(port,9600)
serialFromArduino.flushInput()
while True:
	if(serialFromArduino.inWaiting()):
		input=serialFromArduino.read(14)
		print(input)
	time.sleep(2)
