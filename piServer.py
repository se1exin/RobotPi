import socket
import sys
#import piSerialHelper
import argparse
import RPi.GPIO as GPIO

parser = argparse.ArgumentParser(description='Desc.')
parser.add_argument('-l', action='store', dest='HOST', help='The address to listen on')
parser.add_argument('-p', action='store', dest='PORT', type=int, help='The port to listen on')

args = parser.parse_args()


HOST = ''
PORT = 8888

if(args.HOST != None):
    HOST = args.HOST

if(args.PORT != None):
    PORT = args.PORT

print("Starting Server [HOST="+HOST+"] [PORT="+str(PORT)+"]")

''' GPIO SETUP '''
GPIO.setmode(GPIO.BCM)

pinM1Speed = 18
pinM2Speed = 23
pinM1Direction = 24
pinM2Direction = 25

GPIO.setup(pinM1Speed, GPIO.OUT)  # Motor 1 PWM
GPIO.setup(pinM2Speed, GPIO.OUT)  # Motor 2 PWM
GPIO.setup(pinM1Direction, GPIO.OUT)  # Motor 1 Direction
GPIO.setup(pinM2Direction, GPIO.OUT)  # Motor 2 Direction


# Set up and start our GPIO PWM pin (motor 1)
gpioM1 = GPIO.PWM(pinM1Speed, 50)
gpioM1.start(0)

# Set up and start our GPIO PWM pin (motor 2)
gpioM2 = GPIO.PWM(pinM2Speed, 50)
gpioM2.start(0)

#serWrite = piSerialHelper.piSerial(DEVICE, BAUD, True)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket created on '+socket.gethostbyname(socket.gethostname()))

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(0)
while 1:
    # if(serWrite.isReady()):
    #     serWrite.sendMotorValues(0, 0, 0, 0)
    # else:
    #     print("Serial Not Ready")
    conn, addr = s.accept()
    try:
        #begin accepting and parsing data
        try:
            data = conn.recv(128)
            print("Motor Values [MS1],[MS2],[MD1],[MD2]: " + data)
            data = data.split(',')
            speedM1 = data[0]
            speedM2 = data[1]
            directionM1 = int(data[2])
            directionM2 = int(data[3])

            # Update motor 1's speed
            gpioM1.ChangeDutyCycle(float(speedM1))

            # Update motor 2's speed
            gpioM2.ChangeDutyCycle(float(speedM2))

            # Set Motor directions
            GPIO.output(pinM1Direction, directionM1)
            GPIO.output(pinM2Direction, directionM2)
        except Exception, msg:
            print("Error receiving data from client:" + str(msg[0]))

        # try:
        #     if(serWrite.isReady()):
        #         serWrite.sendMotorValues(int(speedM1), int(speedM2), int(directionM1), int(directionM2))
        #     else:
        #         print("Serial Not Ready")
        # except Exception, msg:
        #     print("Error sending data via serial: "+str(msg[0]))

    except KeyboardInterrupt:
        print("Closing Connections")
        conn.close()
        s.close()
print("Exit loop")
conn.close()
s.close()
gpioM1.stop()
gpioM2.stop()
GPIO.cleanup()
