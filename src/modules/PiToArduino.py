import serial
import time

print('Python version:',serial.__version__)

arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
arduinoSerialData.flushInput()
while True:
    variable = input('What is your command? ')
    arduinoSerialData.write(variable.encode()+'\n'.encode('ascii'))
    time.sleep(0.05)
    print()
    
    start_time = time.time()
    while(arduinoSerialData.inWaiting()!=0):
        read_serial=arduinoSerialData.readline()
        print(read_serial)
    end_time = time.time()
    print("Total time taken this loop: {0:.3f}s.".format(end_time - start_time))
