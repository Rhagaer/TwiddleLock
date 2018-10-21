import time
from datetime import datetime
import os
from symbol import Symbol
from code import Code
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

# constants
ADC_VARIATION_RANGE = 20
CODE = Code(symbols=[Symbol("L", 2), Symbol("R", 2), Symbol("L", 3)])
TIME_INTERVAL = 1
STOP_TIME = 3


S_LINE = 21
L_LINE = 20
U_LINE = 16

# STATE
listening = False
input_code = Code()
num_intervals_static = 0
locked = True
secure_mode = True


def toggleListening(channel=False):
    global listening
    global input_code
    global num_intervals_static

    input_code.reset()
    num_intervals_static = 0
    listening = not listening
    if(listening):
        print("NOW LISTENING, secure mode:", secure_mode)
    else:
        print("NOT LISTENING")


def setup():
    # SETUP
    GPIO.setmode(GPIO.BCM)
    CLK = 18
    MISO = 23
    MOSI = 24  # C-Line
    CS = 25
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    GPIO.setup(S_LINE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(S_LINE, GPIO.RISING,
                          callback=toggleListening, bouncetime=300)

    GPIO.setup(L_LINE, GPIO.OUT)
    GPIO.setup(U_LINE, GPIO.OUT)

    return mcp


def on_adc_read(val_1, val_2):
    direction = determine_direction(val_1, val_2)
    global input_code
    if len(input_code.symbols) == 0:
        # Just started
        print("Waiting to start")
        if direction != "N":
            print("Starting")
            input_code.symbols.append(Symbol(direction, 1))
    else:
        last_direction = input_code.symbols[-1].direction
        print(input_code.symbols[-1])
        if direction == last_direction:

            input_code.symbols[-1].duration += 1
        elif direction != "N":

            input_code.symbols.append(Symbol(direction, 1))


def determine_direction(val_1, val_2):
    global num_intervals_static
    if val_2-ADC_VARIATION_RANGE <= val_1 <= val_2+ADC_VARIATION_RANGE:
        num_intervals_static += 1
        return "N"  # no change

    elif val_1 > val_2:
        num_intervals_static = 0
        return "R"  # right
    else:
        num_intervals_static = 0
        return "L"  # left


def code_is_valid():
    if secure_mode:
        return input_code == CODE
    else:
        return input_code.unsecure_equals(CODE)


def compare_codes():
    global locked
    if code_is_valid():
        if locked:
            print("Unlocking")
            GPIO.output(U_LINE, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(U_LINE, GPIO.LOW)
        else:
            print("Locking")
            GPIO.output(L_LINE, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(L_LINE, GPIO.LOW)

        locked = not locked

    else:
        print("Invalid Code")

    toggleListening()


def main():
    mcp = setup()
    global listening
    global TIME_INTERVAL
    global num_intervals_static
    global input_code
    global STOP_TIME

    try:
        while True:

            if(listening):
                # if the wait time has exceed or it has not started yet
                if num_intervals_static < STOP_TIME or len(input_code.symbols) == 0:
                    val_1 = mcp.read_adc(0)
                    time.sleep(TIME_INTERVAL)
                    val_2 = mcp.read_adc(0)
                    on_adc_read(val_1, val_2)
                else:
                    print("***** START OF INPUTED CODE ****")
                    print(input_code)
                    print("***** END OF CODE ****")
                    compare_codes()

            else:
                time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
