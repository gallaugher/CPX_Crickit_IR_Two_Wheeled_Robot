#  IMPORTANT: Code below uses an ELEGOO mini-rmote I had.
#  Adafruit code at the URL below can be used to find the
#  precise key codes for most infrared remotes, and Adafruit sells a $5 NEC code model, too.
#  https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python?view=all#ir-test-with-remote
#  More info in the README.md
#  Adapted from several examples form Adafruit Industries, including:
#  IR code from Remote Controlled IR Tree Ornament with CPX:
#  https://learn.adafruit.com/remote-control-tree-ornament-with-circuit-playground-express/overview
#  CircuitPython and DC Motors:
#  https://learn.adafruit.com/adafruit-crickit-creative-robotic-interactive-construction-kit/circuitpython-dc-motors
#  And robot assembly from:
#  https://learn.adafruit.com/adabox002/assembling-your-robot
#  I also glued a cool 3D printed Crickit mount from the Ruiz brothers:
#  https://www.thingiverse.com/thing:2998716
#  I'll post videos & more details when I get this working.
#  Problem with current code or IR hardware is I get glitchy Repeated Code Errors or Memory Errors
#  at random times when pressing buttons on my IR remote, however remote & code does work - sometimes requires
#  more than one press to register (sometimes a few more).
#  Know how to fix this? Suggestions welcome!

from adafruit_crickit import crickit
import pulseio
import board
import digitalio
import adafruit_irremote

motor_left = crickit.dc_motor_1
motor_right = crickit.dc_motor_2

red_led = digitalio.DigitalInOut(board.D13)
red_led.direction = digitalio.Direction.OUTPUT

pulsein = pulseio.PulseIn(board.REMOTEIN, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
received_code = bytearray(4)
last_command = None
print("Blrop!")

while True:
    red_led.value = False  # turn off red_led at D13
    try:
        pulses = decoder.read_pulses(pulsein)
    except MemoryError as e:
        print("Memory error: ", e)
        continue
    red_led.value = True  # Got this far? Show no errors & light red_led
    command = None
    try:
        code = decoder.decode_bits(pulses, debug=False)
        if len(code) > 3:
            command = code[2]
        print("Decoded:", code)
    except adafruit_irremote.IRNECRepeatException as e:  # unusual short code!
        print("Repeated Code Error:", e.args)
        command = last_command
    except adafruit_irremote.IRDecodeException as e:  # failed to decode
        print("Failed to decode:", e.args)
    except MemoryError as e:
        print("Memory error: ", e.args)

    if not command:
        continue
    last_command = command
    red_led.value = False

    received_code = code
    print("NEC Infrared code received: ", received_code)
        
    if received_code == [255, 0, 157, 98]:
        print("Go Forward!")  # Vol +
        motor_left.throttle = -0.5  # full speed!
        motor_right.throttle = 0.5
    elif received_code == [255, 0, 87, 168]:
        print("Go Backward!")  # Vol -
        motor_left.throttle = 0.5  # reverse full speed!
        motor_right.throttle = -0.5
    elif received_code == [255, 0, 253, 2]:
        print("Stop!")  # Play
        motor_left.throttle = 0.0  # stop
        motor_right.throttle = 0.0
    elif received_code == [255, 0, 221, 34]:
        print("Turn Left!")  # RWD
        motor_left.throttle = 0.3  # left
        motor_right.throttle = 0.3
    elif received_code == [255, 0, 61, 194]:
        print("Turn Right!")  # FWD
        motor_left.throttle = -0.3  # right
        motor_right.throttle = -0.3
    
