import serial
import time

port="/dev/ttyACM0"
serialFromArduino=serial.Serial(port,9600)
serialFromArduino.flushInput()
while True:
	if(serialFromArduino.inWaiting()):
		time.sleep(1)
		input=serialFromArduino.read(10)
		print(input)
