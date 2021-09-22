import RPi.GPIO as GPIO
import collections
from time import sleep

### GLOBALS
GPIO.setmode(GPIO.BCM)
box_width = 40
gpios = []
wires = []
for gpio in range(0,40):
    gpios.append(gpio)
for wire in range(1,41):
    wires.append(wire)
gpio_translate = dict(zip(wires,gpios))

print(gpio_translate)

### formatting overrides
def f_h_border():
    print("|=", "".ljust(box_width, '='), "=|", sep='')
def fprint(message):
    print("| ",message.ljust(box_width, ' ')," |", sep='')
def finput(message):
    print("| ", end="")
    thing = input(message.ljust(box_width, ' '))
    return thing

def get_gpio(pin):
    return gpio_translate[pin]

### choose which harness
def choose_harness():
    fprint("")
    fprint("Please choose which harness you are using:")
    fprint("1: gen 2, 7 & 10 inch")
    fprint("2: gen 2, 12 inch")
    choice = finput("Please input: [1, 2, 3, 4, 5, 6]")

    harness = collections.OrderedDict()
    if choice == "1": #gen 2 - 7"/10"
        harness["Reader"] = [4,14,16,3]
        harness["Barrel"] = [5,7]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]
        harness["MIC"] = [12,13]
        harness["Motion"] = [17,18,19]
        harness["HDMI DIM"] = [20,21]
        harness["Button 1"] = [22,23]
        harness["Button 2"] = [24,25]
        harness["Keypad"] = [29,30,31,32]
        harness["Camera"] = [37,38,39,40]

    if choice == "2": #gen 2, 12 inch
        harness["Reader"] = [3,4,14,16]
        harness["Barrel"] = [1,2]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]


    print(harness)
    print(harness["Reader"])
    for peripheral in harness:
        print(peripheral)
        for pin in harness[peripheral]:
            print(pin)

    return harness

def flash_led(gpio, period):
    GPIO.output(gpio, GPIO.HIGH)
    time.sleep(period)
    GPIO.output(gpio, GPIO.LOW)

### initialize all P8 pins as gpio
def setup_gpios():
    f_h_border()
    fprint("Setting up GPIOs...")
    GPIO.setup(gpios, GPIO.OUT)

    for i in range(38):
        gpio1 = i
        gpio2 = i + 1
        gpio3 = i + 2
        GPIO.output([gpio1,gpio2,gpio3], GPIO.HIGH)
        if i > 0:
            GPIO.output((i-1), GPIO.LOW)
        sleep(0.1)
    GPIO.output(gpios, GPIO.LOW)

def manual_test():
    f_h_border()
    fprint("Starting Manual test")
    fprint("")
    while True:
        test_pin = finput("Which pin to test? (0 to stop)")
        if test_pin == '0':
            break
        gpio = get_gpio(int(test_pin))
        fprint("Testing %s" % gpio)
        GPIO.output(gpio, GPIO.HIGH)
        sleep(3)
        GPIO.output(gpio, GPIO.LOW)

def flash_led(gpio, time, hertz=2):
    reps = time * hertz
    for i in range(reps):
        GPIO.output(gpio, GPIO.HIGH)
        sleep(1/(hertz*2))
        GPIO.output(gpio, GPIO.LOW)
        sleep(1/(hertz*2))

def pinwise_test():
    f_h_border()
    fprint("Pin-by-pin test")
    time = 5
    for wire, gpio in gpio_translate.items():
        fprint("Now testing wire %i (%s)" % (wire, gpio))
        flash_led(gpio, time)

def peripheral_test(harness):
    f_h_border()
    fprint("Peripheral-by-peripheral test")
    for peripheral in harness:
        fprint(peripheral)
        for wire in harness[peripheral]:
            print(wire)
            gpio = get_gpio(wire)
            GPIO.output(gpio, GPIO.HIGH)
            sleep(3)
            GPIO.output(gpio, GPIO.LOW)



############
### main ###
############
def main():
    print("Starting main function")
    f_h_border()
    #automatic_test()
    setup_gpios() #set up gpio pins
    harness = choose_harness()
    #automatic_test()
    peripheral_test(harness)
    manual_test()





if __name__ == "__main__":
    main()
