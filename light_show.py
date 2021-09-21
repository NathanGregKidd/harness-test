import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# define how the wires match up to the gpios
wires = []
gpios = []
for wire in range(1,41):
    wires.append(wire)
for gpio in range(1,41):
    gpios.append(gpio)
wire_gpio_matchup = dict(zip(wires, gpios))
#
#set up all gpios that are connected to wires and turn everything off
print("setting up the following GPIOs:\n", gpios)
GPIO.setup(gpios, GPIO.OUT)
GPIO.output(gpios, GPIO.LOW)

def get_gpio(wire):
    gpio = wire_gpio_matchup[wire]
    return gpio

def arpeggio_up(wires, period):
    for wire in wires:
        gpio = get_gpio(wire)
        GPIO.output(gpio, GPIO.HIGH)
        time.sleep(period)
        GPIO.output(gpio, GPIO.LOW)


def main():
    arpeggio_up(wires, 0.1)

if __name__ == "__main__":
    main()


