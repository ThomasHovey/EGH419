import serial
import time
from classes.State import State
from classes.IMU import IMU
from classes.Compass import Compass

def Serial_init():
    global startMarker, endMarker, ArduinoSer
    startMarker = 60
    endMarker = 62
    ArduinoSer = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
##    waitForArduino()
    print("Serial ready!")
    ArduinoSer.flushInput()

def sendToArduino(sendStr):
    checksum = 0
    for i in sendStr:
        if ord(i) != startMarker and ord(i) != endMarker:
            checksum = checksum + ord(i.encode())
##            print("Sending " + i + " with ASCII value: " + str(ord(i.encode())) + " checksum: " + str(checksum%128))
    checksum = checksum % 128
    print("Sent data with CS value: " + str(checksum) + " which is: " + str(chr(checksum)))
    checksum_c = chr(checksum)
    sendStr = sendStr + checksum_c
    ArduinoSer.write(sendStr.encode())
    print("Checksum added to data: " + sendStr)

def recvFromArduino():
    global startMarker, endMarker, ArduinoSer

    message = ""
    message_sum = 0
    readCheckSum = 0
    Recieve_checksum = 0
    readInProgress = 0
    x = "z" # any value that is not an endMarker or startMarker

    # wait for the start character
    while  ord(x) != startMarker: # while x is not a startMarker, keep reading
        x = ArduinoSer.read()

    # Found startMarker, loop through and save data until the end marker is found
    readInProgress = 1
    while readInProgress:
        x = ArduinoSer.read()
        if readCheckSum == 1:
            Recieve_checksum = ord(x)
            checksum_result = message_sum%128 - Recieve_checksum
            return(message,checksum_result)
        if ord(x) == endMarker: # if x is a endMarker, move to read check sum
            readCheckSum = 1
        else: # x is not a endMarker, keep saving data
            message = message + x
            message_sum = message_sum + ord(x)
            
                
def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker, ArduinoSer
    
    msg = ""
    while msg.find("Arduino is ready") == -1:
        while ArduinoSer.inWaiting() == 0:
            pass
        msg,cs_error = recvFromArduino()
        print(msg + ", Pi CS error: " + str(cs_error))
def SerialSendCommand(State, cmd):
    waitingForReply = False
    # Send command to Arduino
    if waitingForReply == False:
        sendToArduino(cmd)
        waitingForReply = True
    # Wait for Arduino to respond
    while waitingForReply:
        while ArduinoSer.inWaiting() == 0:
            pass    
        dataRecvd,checksum_error = recvFromArduino()
        print("Arduino replied: " + dataRecvd + ", Pi CS error: " + str(checksum_error))
        if ArduinoSer.inWaiting() < 10: 
            ArduinoSer.flushInput()
            waitingForReply = False
##        if checksum_error!=0:
##            print("Checksum error occured!")
##            pass
    # Spilt data base on command
    if cmd=="<ECD:>":
        L_Encoder,R_Encoder = dataRecvd.split(" ")
        print("L_Encoder: " + L_Encoder + ",R_Encoder: " + R_Encoder)
        State.LeftDistance = float(L_Encoder)/5.456 # in mm, 5.456 is counts/mm constance
        State.RightDistance = float(R_Encoder)/5.456 # in mm, 5.456 is counts/mm constance
    elif cmd=="<IMU:>":
        Ax,Ay,Az,Gx,Gy,Gz = dataRecvd.split(" ")
        print("Ax: " + Ax + ", Ay: " + Ay + ", Az: " + Az + ", Gx: " + Gx + ", Gy: " + Gy + ", Gz: " + Gz)
        Acc_x = float(Ax)*0.061/1000 # in g, 0.061 is scale factor
        Acc_y = float(Ay)*0.061/1000 # in g, 0.061 is scale factor
        Acc_z = float(Az)*0.061/1000 # in g, 0.061 is scale factor
        Gyr_x = float(Gx)*4.375/1000 # in dps, 4.375 is scale factor
        Gyr_y = float(Gy)*4.375/1000 # in dps, 4.375 is scale factor
        Gyr_z = float(Gz)*4.375/1000 # in dps, 4.375 is scale factor
        State.IMU = IMU(Acc_x,Acc_y,Acc_z,Gyr_x,Gyr_y,Gyr_z)
    elif cmd=="<MAG:>":
        Mx,My,Mz = dataRecvd.split(" ")
        print("Mx: " + Mx + ", My: " + My + ", Mz: " + Mz)
        Mag_x = Mx/6842 # in gauss, 6842 is scale factor
        Mag_y = My/6842 # in gauss, 6842 is scale factor
        Mag_z = Mz/6842 # in gauss, 6842 is scale factor
        State.Compass = Compass(Mag_x,Mag_y,Mag_z)
    else:
        pass
    return State
    




