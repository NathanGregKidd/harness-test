import RPi.GPIO as GPIO
import collections
import asyncio
from time import sleep

### GLOBALS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
box_width = 50
gpios = []
wires = []
for gpio in range(0,41): #"One too many" because 1 pin is skipped over
    if gpio == 4: #exclude GPIO 4 because it acts strangely.
        continue
    gpios.append(gpio)
for wire in range(1,41):
    wires.append(wire)
gpio_translate = dict(zip(wires,gpios))

#print(gpio_translate)

### formatting overrides
def f_h_border():
    print("|=", "".ljust(box_width, '='), "=|", sep='')
def fprint(message):
    message = str(message)
    print("| ",message.ljust(box_width, ' ')," |", sep='')
def finput(message):
    message = str(message)
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
    fprint("2: gen 2, atom 7 inch")
    fprint("3: gen 2, atom 10 inch")
    fprint("4: gen 2, atom 12 inch")
    fprint("5: gen 3, prototype 7 inch")
    fprint("6: gen 3, prototype 10 inch")
    fprint("7: gen 3, prototype 12 inch")
    choice = finput("Please input: [1, 2, 3, 4, 5, 6, 7]")

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

    if choice == "2": #gen 2, atom 7 inch
        harness["Reader"] = [4,14,16,3]
        harness["Barrel"] = [5,7]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]
        harness["MIC"] = [12,13]
        harness["Motion"] = [17,18,19]
        harness["HDMI DIM"] = [20,21]
        harness["Button"] = [1,6]
        harness["Button 1"] = [22,23]
        harness["Button 2"] = [24,25]
        harness["Keypad"] = [30,32,29,31]
        harness["Camera"] = [39,38,40,37]
    
    if choice == "3": #gen 2, atom 10 inch
        harness["Reader"] = [4,14,16,3] 
        harness["Barrel"] = [1,2] 
        harness["Speaker1"] = [8,9] 
        harness["Speaker2"] = [10,11] 
        harness["MIC"] = [12,13] 
        harness["Motion"] = [17,18,19] 
        harness["HDMI DIM"] = [20,21] 
        harness["Button"] = [5,6] 
        harness["Button 1"] = [22,23]
        harness["Button 2"] = [24,25] 
        harness["Keypad"] = [29,30,31,32] 
        harness["Camera"] = [37,38,39,40] 
    
    if choice == "4": #gen 2, atom 12 inch
        harness["Reader"] = [4,14,16,3] 
        harness["Barrel"] = [1,2] 
        harness["Speaker1"] = [8,9] 
        harness["Speaker2"] = [10,11] 
        harness["MIC"] = [12,13] 
        harness["Motion"] = [17,18,19] 
        harness["HDMI DIM"] = [20,21] 
        harness["Keypad"] = [33,34,35,36] 
        harness["Camera"] = [37,38,39,40] 

    if choice == "5": #Gen 3, 7 inch prototype
        harness["Reader"] = [4,14,16,3,26,28]
        harness["Barrel"] = [5,7]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]
        harness["MIC"] = [12,13]
        harness["Motion"] = [17,18,19]
        harness["HDMI DIM"] = [20,21]
        harness["Button"] = [1,6]
        harness["Button 1"] = [22,23]
        harness["Button 2"] = [24,25]

    if choice == "6": #Gen 3, 10 inch prototype
        harness["Reader"] = [4,14,16,3,26,28]
        harness["Barrel"] = [1,2]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]
        harness["MIC"] = [12,13]
        harness["Motion"] = [17,18,19]
        harness["HDMI DIM"] = [20,21]
        harness["Button"] = [5,6]
        harness["Button 1"] = [22,23]
        harness["Button 2"] = [24,25] 

    if choice == "7": #Gen 3, 12 inch prototype
        harness["Reader"] = [4,14,16,3,26,28]
        harness["Barrel"] = [1,2]
        harness["Speaker1"] = [8,9]
        harness["Speaker2"] = [10,11]
        harness["MIC"] = [12,13]
        harness["Motion"] = [17,18,19]
        harness["HDMI DIM"] = [20,21]
    
    #troubleshooting
#    print(harness)
#    print(harness["Reader"])
#    for peripheral in harness:
#        print(peripheral)
#        for pin in harness[peripheral]:
#            print(pin)
#
    return harness

#def flash_led(gpio, period):
#    GPIO.output(gpio, GPIO.HIGH)
#    time.sleep(period)
#    GPIO.output(gpio, GPIO.LOW)

### initialize all P8 pins as gpio
def setup_gpios():
    f_h_border()
    fprint("Setting up GPIOs...")
    GPIO.setup(gpios, GPIO.OUT)

    for i in range(len(gpios)-2):
        gpio1 = gpios[i]
        gpio2 = gpios[i + 1]
        gpio3 = gpios[i + 2]
        GPIO.output([gpio1,gpio2,gpio3], GPIO.HIGH)
        if i > 0:
            GPIO.output(gpios[i-1], GPIO.LOW)
        sleep(0.1)
    GPIO.output(gpios, GPIO.LOW)

def manual_test():
    f_h_border()
    fprint("Starting Manual test")
    fprint("")
    while True:
        test_pin = finput("Which wire to test? (0 to stop)")
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

def wirewise_test(harness):
    f_h_border()
    fprint("wire-by-wire test")
    fprint("")
    ordered_gpios = []
    for peripheral in harness:
        for wire in harness[peripheral]:
            ordered_gpios.append(get_gpio(wire))
    for gpio in ordered_gpios:
        GPIO.output(gpio, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(gpio, GPIO.LOW)
    
def test_infinite(harness):
    for i in range(3):
        ordered_gpios = []
        for peripheral in harness:
            for wire in harness[peripheral]:
                ordered_gpios.append(get_gpio(wire))
        for gpio in ordered_gpios:
            GPIO.output(gpio, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(gpio, GPIO.LOW)

    for peripheral in harness:
        p_gpios = []
        for wire in harness[peripheral]:
            p_gpios.append(get_gpio(wire))
        flash_led(p_gpios, 2)
        for wire in harness[peripheral]:
            #print(harness[peripheral])
            #flash_led(harness[peripheral], 2)
            gpio = get_gpio(wire)
            GPIO.output(gpio, GPIO.HIGH)
            sleep(1.5)
            GPIO.output(gpio, GPIO.LOW)


def peripheral_test(harness):
    f_h_border()
    fprint("Peripheral-by-peripheral test")
    fprint("")
    for peripheral in harness:
        fprint("== %s ==" % peripheral)
        p_gpios = []
        for wire in harness[peripheral]:
            p_gpios.append(get_gpio(wire))
        flash_led(p_gpios, 2)
        for wire in harness[peripheral]:
            #print(harness[peripheral])
            #flash_led(harness[peripheral], 2)
            fprint("     %s" % wire)
            gpio = get_gpio(wire)
            GPIO.output(gpio, GPIO.HIGH)
            sleep(1.5)
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
    wirewise_test(harness)
    peripheral_test(harness)
    manual_test()

    #start ending forever-test:
    f_h_border()
    fprint("Starting wire-wise test and peripheral test")
    fprint("This will repeat forever, and the test is")
    fprint("now over. Close down the program to end")
    test_infinite(harness)


if __name__ == "__main__":
    main()
