import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

pin1 = 23
pin2 = 24
GPIO.setup(pin1, GPIO.OUT)  # Motor 1 Direction
GPIO.setup(pin2, GPIO.OUT)  # Motor 1 Direction

try:
    while 1:
        print('Setting low')
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)
        time.sleep(0.2)

        print('Setting high')
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 1)
        time.sleep(0.2)
        # for dc in range(0, 101, 5):
        #     print(dc)
        #     p.ChangeDutyCycle(dc)
        #     time.sleep(0.1)
        # for dc in range(100, -1, -5):
        #     print(dc)
        #     p.ChangeDutyCycle(dc)
        #     time.sleep(0.1)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
