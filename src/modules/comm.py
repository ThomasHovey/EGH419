import serial
import time
from classes.State import State

##print('Python version:',serial.__version__)

##arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
##arduinoSerialData.flushInput()
##while True:
##    variable = input('What is your command? ')
##    arduinoSerialData.write(variable.encode()+'\n'.encode('ascii'))
##    time.sleep(0.05)
##    print()
##    
##    start_time = time.time()
##    while(arduinoSerialData.inWaiting()!=0):
##        read_serial=arduinoSerialData.readline()
##        print(read_serial)
##    end_time = time.time()
##    print("Total time taken this loop: {0:.3f}s.".format(end_time - start_time))

def Serial_init():
    global startMarker, endMarker
    startMarker = 60
    endMarker = 62
    ArduinoSer = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
    waitForArduino()
    ArduinoSer.flushInput()

def sendToArduino(sendStr):
    ArduinoSer.write(sendStr)

def recvFromArduino():
    global startMarker, endMarker

    message = ""
    x = "z" # any value that is not an endMarker or startMarker
    byteCount = -1 # to account for the byte of startMarker

    # wait for the start character
    while  ord(x) != startMarker: # while x is not a startMarker, keep reading
        x = ArduinoSer.read()

    # Found startMarker, loop through and save data until the end marker is found
    while ord(x) != endMarker: # while x is not a endMarker, keep reading
        if ord(x) != startMarker: # avoild taking endMarker and startMarker
            message = message + x 
            byteCount += 1
        x = ArduinoSer.read()
    return(message)

def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:
        while ser.inWaiting() == 0:
            pass
        msg = recvFromArduino()
        print msg
        print

def SerialSendCommand(State,cmd):
    # Send command to Arduino 
    sendToArduino(cmd)
    # Wait for Arduino to respond
    while ArduinoSer.inWaiting() == 0:
        pass    
    dataRecvd = recvFromArduino()
    # Spilt data base on command
    if cmd=="ECD:":
        L_Encoder,R_Encoder = dataRecvd.split(" ")
        State.LeftDistance = L_Encoder/5.456 # in mm, 5.456 is counts/mm constance
        State.RightDistance = R_Encoder/5.456 # in mm, 5.456 is counts/mm constance
    elif cmd=="IMU:":
        Ax,Ay,Az,Gx,Gy,Gz = dataRecvd.split(" ")
        State.Acc_x = Ax*0.061/1000 # in g, 0.061 is scale factor
        State.Acc_y = Ay*0.061/1000 # in g, 0.061 is scale factor
        State.Acc_z = Az*0.061/1000 # in g, 0.061 is scale factor
        State.Gyr_x = Gx*4.375/1000 # in dps, 4.375 is scale factor
        State.Gyr_y = Gy*4.375/1000 # in dps, 4.375 is scale factor
        State.Gyr_z = Gz*4.375/1000 # in dps, 4.375 is scale factor
    elif cmd=="MAG:":
        Mx,My,Mz = dataRecvd.split(" ")
        State.Mag_x = Mx/6842 # in gauss, 6842 is scale factor
        State.Mag_y = My/6842 # in gauss, 6842 is scale factor
        State.Mag_z = Mz/6842 # in gauss, 6842 is scale factor
    else:
        pass
    return State
    
    



