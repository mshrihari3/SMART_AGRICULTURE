import time
import serial

ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

time.sleep(1)

try:
	while True:
		if ser.inWaiting()>0:
			data=ser.read()
			print (data.strip())

except KeyboardInterrup:
	print ("Exiting Program")

except:
	print ("Error Occurs, ExitingProgram")

finally:
	ser.close()
	pass
