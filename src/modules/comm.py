import serial
import time
from classes.State import State
from classes.IMU import IMU
from classes.Compass import Compass

def Serial_init():
    global startMarker, endMarker, ArduinoSer
    startMarker = 60
    endMarker = 62
    print("Serial initialization...")
    ArduinoSer = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
    waitForArduino()
    print("Serial ready!!!")
    ArduinoSer.flushInput()

def sendToArduino(sendStr):
    checksum = 0
    for i in sendStr:
        if ord(i) != startMarker and ord(i) != endMarker:
            checksum = checksum + ord(i.encode())
    checksum = checksum % 128
    checksum_c = chr(checksum)
    sendStr = sendStr + checksum_c
    ArduinoSer.write(sendStr.encode())

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
        if not x:
            x = "z"

    # Found startMarker, loop through and save data until the end marker is found
    readInProgress = 1
    while readInProgress:
        if ord(x) != startMarker: # if x is a endMarker, move to read check sum
            if readCheckSum == 1:
                Recieve_checksum = ord(x)
                checksum_result = message_sum%128 - Recieve_checksum
                return(message,checksum_result)
            if ord(x) == endMarker: # if x is a endMarker, move to read check sum
                readCheckSum = 1
            else: # x is not a endMarker, keep saving data
                message = message + x
                message_sum = message_sum + ord(x)
        x = ArduinoSer.read()
            
                
def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker, ArduinoSer
    
    msg = ""
    while msg.find("Arduino is ready") == -1:
        while ArduinoSer.inWaiting() == 0:
            pass
        msg,cs_error = recvFromArduino()
        print(msg)
        
def updateData(State):
    cmdData = []
    cmdData.append("<IMU:>")
    cmdData.append("<ECD:>")
    cmdData.append("<MAG:>")
    n = 0
    splitData_En = 0;
    maxTrial = 5;
    nTrial = 0;
    MaxTimeOut = 0.2
    while n < len(cmdData):
        cmd = cmdData[n]
        waitingForReply = False
        # Send command to Arduino
        if waitingForReply == False:
            sendToArduino(cmd)
            waitingForReply = True
        # Wait for Arduino to respond
        while waitingForReply:
            start_waiting = time.time()
            while ArduinoSer.inWaiting() == 0:
                curr_waiting = time.time()
                if (curr_waiting-start_waiting)>MaxTimeOut:
                    waitingForReply = False
                    n = len(cmdData) + 1 # Do this to exit the loop
                    print("[ERROR] Transmission time out ! Data update failed!")
                pass    
            dataRecvd,checksum_error = recvFromArduino()
            # Checksum
            if checksum_error != 0:
                print("[ERROR] Pi CheckSum error, trying again...")
                nTrial +=1
                splitData_En = 0
                waitingForReply = False
                if nTrial>maxTrial:
                    n = len(cmdData) + 1 # Do this to exit the loop
                    print("[ERROR] Pi CheckSum error, runout of trials! Data update failed!")
            elif dataRecvd == "Er": # Pi checksum pass but Arduino checksum is not correct
                print("[ERROR] Arduino CheckSum error, trying again...")
                nTrial +=1
                splitData_En = 0
                waitingForReply = False
                if nTrial>maxTrial:
                    n = len(cmdData) + 1 # Do this to exit the loop
                    print("[ERROR] Arduino CheckSum error, runout of trials! Data update failed!")
            else:
                splitData_En = 1
            ArduinoSer.flushInput()
            waitingForReply = False

        if splitData_En:    
            # Spilt data base on command
            if cmd=="<ECD:>":
                try:
                    split_data = dataRecvd.split(" ")
                    L_Encoder,R_Encoder = split_data
                    State.LeftDistance = float(L_Encoder)/5.456 # in mm, 5.456 is counts/mm constance
                    State.RightDistance = float(R_Encoder)/5.456 # in mm, 5.456 is counts/mm constance
                except ValueError as error:
                    print("[WARNING] Arduino returned invalid ECD data, state elements unchanged.")
                    print("Data received: " + dataRecvd)
            elif cmd=="<IMU:>":
                try:
                    split_data = dataRecvd.split(" ")
                    Ax,Ay,Az,Gx,Gy,Gz = split_data
                    Acc_x = float(Ax)*0.061/1000 # in g, 0.061 is scale factor
                    Acc_y = float(Ay)*0.061/1000 # in g, 0.061 is scale factor
                    Acc_z = float(Az)*0.061/1000 # in g, 0.061 is scale factor
                    Gyr_x = float(Gx)*4.375/1000 # in dps, 4.375 is scale factor
                    Gyr_y = float(Gy)*4.375/1000 # in dps, 4.375 is scale factor
                    Gyr_z = float(Gz)*4.375/1000 # in dps, 4.375 is scale factor 
                    State.IMU = IMU(Acc_x,Acc_y,Acc_z,Gyr_x,Gyr_y,Gyr_z)
                except ValueError as error:
                    print("[WARNING] Arduino returned invalid IMU data, state elements unchanged.")
                    print("Data received: " + dataRecvd)
            elif cmd=="<MAG:>":
                try:
                    split_data = dataRecvd.split(" ")
                    Mx,My,Mz = split_data
                    Mag_x = float(Mx)/6842 # in gauss, 6842 is scale factor
                    Mag_y = float(My)/6842 # in gauss, 6842 is scale factor
                    Mag_z = float(Mz)/6842 # in gauss, 6842 is scale factor  
                    State.Compass = Compass(Mag_x,Mag_y,Mag_z)
                except ValueError as error:
                    print("[WARNING] Arduino returned invalid Compass data, state elements unchanged.")
                    print("Data received: " + dataRecvd)
            n += 1
    return State
    
def setMotorSpeed(State):
    ML = State.LeftMotorSpeed
    MR = State.RightMotorSpeed
    SENT_SPEED = "<MoSp:" + str(ML) + "," + str(MR) + ">"
    if abs(ML)>140 or abs(MR)>140:
        print("[ERROR] Maximum speed allowed is 140, please reduce the speed!")
    else:
        setSpeedDone = 0;
        maxTrial = 5;
        nTrial = 0;
        MaxTimeOut = 0.2
        time_out = 0
        while not setSpeedDone:
            waitingForReply = False
            # Send command to Arduino
            if waitingForReply == False:
                sendToArduino(SENT_SPEED)
                waitingForReply = True
            # Wait for Arduino to respond
            while waitingForReply:
                start_waiting = time.time() 
                while ArduinoSer.inWaiting() == 0:
                    curr_waiting = time.time()
                    if (curr_waiting-start_waiting)>MaxTimeOut:
                        waitingForReply = False
                        setSpeedDone = 1
                        time_out = 1
                        print("[ERROR] Transmission time out ! Data update failed!")
                    pass
                if time_out == 0:
                    dataRecvd,checksum_error = recvFromArduino()
    ##                checksum_error = 1
    ##                dataRecvd = "Er"
                    if checksum_error != 0: # Error occured
                        print("[ERROR] Pi CheckSum error, trying again...")
                        nTrial +=1
                        waitingForReply = False
                        if nTrial>maxTrial:
                            setSpeedDone = 1 # Do this to exit the loop
                            print("[ERROR] Pi CheckSum error, runout of trials! Speed may or may not set properly!")
                    elif dataRecvd=="Er": # Arduino send "Er" whenever the checksum on its side is wrong
                            print("[ERROR] Arduino CheckSum error, trying again...")
                            nTrial +=1
                            waitingForReply = False
                            if nTrial>maxTrial:
                                setSpeedDone = 1 # Do this to exit the loop
                                print("[ERROR] Arduino CheckSum error, runout of trials! Speed is not set!")
                    else:
                        print(dataRecvd)
                        setSpeedDone = 1
                ArduinoSer.flushInput()
                waitingForReply = False

def IMU_config():
    ax_list, ay_list, zg_list = []
    state = State()
    for i in range(50):
        # Read encoder data ect
        comm.updateData(state)
        ax_list.append(state.IMU.x_accel)
        ay_list.append(state.IMU.y_accel)
        zg_list.append(state.IMU.z_gyro)

    x_offset = sum(ax_list)/float(len(ax_list))
    y_offset = sum(ay_list)/float(len(ay_list))
    z_offset = sum(zg_list)/float(len(zg_list))
    
    print("X offset")
    print(x_offset)
    print("Y offset")
    print(y_offset)
    print("Z offset")
    print(z_offset)
    