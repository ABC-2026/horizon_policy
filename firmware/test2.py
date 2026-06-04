import serial
import time

# Set up the serial connection
ser = serial.Serial(
    port='COM15',        # Replace with the correct port
    baudrate=115200,      # Match the baudrate with your microcontroller
    timeout=1           # Set a read timeout
)

time.sleep(2)  # Give the microcontroller time to reset

# Send a command and read response
ser.write(b'-1 -1 -1 2 0 ;\n')  # Send command
time.sleep(1)          # Wait for the response
response = ser.read_all().decode('utf-8')  # Read the response
print("Response type ",type(response))
#print(response[3])
if(response[0:2]=='DD'):
    print("hii")
    ser.write(b'240 0 0 0 35 ;')
    time.sleep(1)
    ser.write(b'240 340 148 0 35 ;')
    time.sleep(0.5)
    ser.write(b'290 340 148 0 35 ;')
    time.sleep(0.5)
    ser.write(b'290 390 148 0 35 ;')
    time.sleep(0.5)
    ser.write(b'240 390 148 0 35 ;')
    time.sleep(0.5)
    ser.write(b'240 340 148 0 35 ;')



# Close the serial connection
ser.close()
