import time
import RPi.GPIO as GPIO
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

direction = 0

try:
    while 1:
        print('Setting low')
        GPIO.output(pinM1Direction, direction)
        GPIO.output(pinM2Direction, direction)
        
        if direction == 0:
            direction = 1
        else:
            direction = 0

        for dc in range(0, 101, 5):
            print(dc)
            gpioM1.ChangeDutyCycle(dc)
            gpioM2.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            print(dc)
            gpioM1.ChangeDutyCycle(dc)
            gpioM2.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
gpioM1.stop()
gpioM2.stop()
GPIO.cleanup()
