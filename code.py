from adafruit_crickit import crickit
import pulseio
import board
import digitalio
import adafruit_irremote
import audioio

motor_left = crickit.dc_motor_1
motor_right = crickit.dc_motor_2

red_led = digitalio.DigitalInOut(board.D13)
red_led.direction = digitalio.Direction.OUTPUT

pulsein = pulseio.PulseIn(board.REMOTEIN, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
print("Everything configured & ready to run!")

def get_IR_code():
    red_led.value = False  # turn off red_led at D13
    try:
        pulses = decoder.read_pulses(pulsein)
    except MemoryError as e:
        print("Memory error: ", e)
        return None
    red_led.value = True  # Got this far? Show no errors & light red_led
    try:
        ir_code = decoder.decode_bits(pulses, debug=False)
        print("Decoded:", ir_code)
    except adafruit_irremote.IRNECRepeatException as e:  # unusual short code!
        print("Repeated Code Error:", e.args)
        return None
    except adafruit_irremote.IRDecodeException as e:  # failed to decode
        print("Failed to decode:", e.args)
        return None
    except MemoryError as e:
        print("Memory error: ", e.args)
        return None
    red_led.value = False  # turn off red_led since command successfully received.
    print("NEC Infrared code received: ", ir_code)
    return ir_code

def play_sound(wavfile):
    f = open(wavfile, "rb")
    wav = audioio.WaveFile(f)
    a = audioio.AudioOut(board.A0)
    a.play(wav)

while True:
    received_code = get_IR_code()
    if not received_code: # if no proper code received, restart while loop
        continue
    
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
        play_sound("rimshot.wav")
    elif received_code == [255, 0, 221, 34]:
        print("Turn Left!")  # RWD
        motor_left.throttle = 0.3  # left
        motor_right.throttle = 0.3
    elif received_code == [255, 0, 61, 194]:
        print("Turn Right!")  # FWD
        motor_left.throttle = -0.3  # right
        motor_right.throttle = -0.3
