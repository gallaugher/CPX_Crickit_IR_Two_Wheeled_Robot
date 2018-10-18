# CPX_Crickit_IR_Two_Wheeled_Robot
Code to power a two-wheeled DC motors robot w/Adafruit Circuit Playground Express, Crickit, and CircuitPython, powered by an infrared remote

Hardware:
CircuitPlayground Express
Crickit for CircuitPlayground Express
Adafruit Two Wheeled Robot Chassis w/DC Motors included: https://www.adafruit.com/product/3244
It should work with this one, which has one less "layer" but is $5 chepaer: https://www.adafruit.com/product/3216
Elegoo Remote - I got this in a kit, but you should be able to use any infrared remote.
NOTE: You'll likely have to identify your codes, but you can easily do this by following instructions at:
https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python?view=all#ir-test-with-remote

Just use this code, then run on your CPX, point your IR remote at the CPX, and write down the 4 digit array that prints out for each character press. My remote uses four buttons in an configuration:
        Up
 left  Stop  right
       Down
       
They are listed on the remote (and in code.py) as:
       Vol +
RWD    Play   FWD
       Vol -
