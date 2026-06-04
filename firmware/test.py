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
time.sleep(2)          # Wait for the response
response = ser.read_all().decode('utf-8')  # Read the response
print("Response",response)
#print(response[3])
if(response[0:2]=='DD'):
    print("hii")
    ser.write(b'235 0 0 1 35')
    time.sleep(2)
    response= response = ser.read_all().decode('utf-8')  # Read the response
    if(response[0:2]=='DD'):
        ser.write(b'235 157 0 1 35')
        time.sleep(2)
        response=ser.read_all().decode('utf-8')
        if(response[0:2]=='DD'):
            ser.write(b'235 157 150 1 35')
            time.sleep(2)
            response=ser.read_all().decode('utf-8')
            ser.write(b'235 157 150 0 35')
            time.sleep(2)
            response=ser.read_all().decode('utf-8')
            if(response[0:2]=='DD'):
                ser.write(b'235 157 50 0 35')
                time.sleep(2)
                response=ser.read_all().decode('utf-8')
                if(response[0:2]=='DD'):
                    ser.write(b'444 158 50 0 35')
                    time.sleep(2)
                    ser.write(b'444 164 50 0 35')
                    time.sleep(2)
                    ser.write(b'444 164 150 0 35')
                    time.sleep(2)
                    ser.write(b'444 164 150 1 35')
                    time.sleep(2)
                    ser.write(b'444 164 50 1 35')


# Close the serial connection
ser.close()
