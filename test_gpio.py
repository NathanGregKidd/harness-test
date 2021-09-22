import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def main():
    while True:
        gpio = int(input("What gpio to test? [0-45]: "))
        GPIO.setup(gpio, GPIO.OUT)
        print("testing", gpio)
        GPIO.output(gpio, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(gpio, GPIO.LOW)

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
