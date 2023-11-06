import time
from adafruit_servokit import ServoKit
import smbus

# Set up the servo
kit = ServoKit(channels=16)
servo = kit.servo[11]
servo.set_pulse_width_range(500, 2500)
servo.angle = 60  # Starting position

# Light sensor setup
DEVICE_ADDRESS = 0x10  # 7-bit address (will be left-shifted to add the read/write bit)
ALS_CONF = 0x00  # ALS Configuration Register
ALS = 0x04  # ALS high resolution output data
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
bus.write_word_data(DEVICE_ADDRESS, ALS_CONF, 0x1800)

def read_light():
    data = bus.read_word_data(DEVICE_ADDRESS, ALS)
    lux = data  # Placeholder for the actual formula to calculate lux
    return lux

def flip_switch(on):
    if on:
        servo.angle = 0  # Angle for 'on' position
    else:
        servo.angle = 60  # Angle for 'off' position
    time.sleep(0.5)

try:
    while True:
        lux = read_light()
        print(f"Ambient Light: {lux} Lux")

        # Decide whether to flip on or off based on light reading
        # Assuming a threshold value of 10 for whether it's dark enough to require light
        if lux < 50:
            print("It's dark, flipping switch on!")
            flip_switch(True)
        else:
            print("Light detected, flipping switch off!")
            flip_switch(False)

        time.sleep(2)  # Adjust the delay as needed

except KeyboardInterrupt:
    # Once interrupted, set the servo back to 'off' position
    print("Program interrupted by user. Turning off switch and exiting.")
    flip_switch(False)
