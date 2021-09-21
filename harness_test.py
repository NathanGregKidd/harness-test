import Adafruit_BBIO.GPIO as GPIO
import collections
from time import sleep

### GLOBALS
box_width = 40
gpio_translate = {}
for i in range(40):
    pin_num = 46 - i
    gpio_translate[i+1] = "P8_%s" % pin_num

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
        harness["Reader"] = [3,4,14,16]
        harness["Barrel"] = [5,7]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]

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

### initialize all P8 pins as gpio
def setup_p8():
    f_h_border()
    p8_pins = 46
    non_configurable_pins = 2
    for i in range(p8_pins - non_configurable_pins):
        pin_num = i + 3 # start at pin number 3, pins 1 and 2 are DGND and non-configurable.
        pin = "P8_%s" % pin_num
        fprint("Setting up %s" % pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    for i in range(40):
        pin = i + 1
        gpio = get_gpio(pin)
        GPIO.output(gpio, GPIO.HIGH)
        sleep(0.1)
    for i in range(40):
        pin = i + 1
        gpio = get_gpio(pin)
        GPIO.output(gpio, GPIO.LOW)
        sleep(0.1)

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
            sleep(5)
            GPIO.output(gpio, GPIO.LOW)



############
### main ###
############
def main():
    print("Starting main function")
    f_h_border()
    #automatic_test()
    setup_p8() #set up p8 pins as gpio
    harness = choose_harness()
    #automatic_test()
    peripheral_test(harness)
    manual_test()





if __name__ == "__main__":
    main()
