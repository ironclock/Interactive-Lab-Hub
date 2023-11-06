import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_servokit import ServoKit
import smbus

# Servo setup for the light switch
kit = ServoKit(channels=16)
light_servo = kit.servo[11]
light_servo.set_pulse_width_range(500, 2500)
light_servo.angle = 60  # Starting position

# Servo setup for the water spray
water_servo = kit.servo[0]
water_servo.set_pulse_width_range(500, 2500)

# Light sensor setup
DEVICE_ADDRESS = 0x10  # 7-bit address
ALS_CONF = 0x00  # ALS Configuration Register
ALS = 0x04  # ALS high resolution output data
light_bus = smbus.SMBus(1)

# I2C bus setup for moisture sensor
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)

# Light sensor configuration
light_bus.write_word_data(DEVICE_ADDRESS, ALS_CONF, 0x1800)

# Moisture sensor calibration values (replace with your calibration values)
dry_value = 20000
wet_value = 8000

def read_light():
    data = light_bus.read_word_data(DEVICE_ADDRESS, ALS)
    lux = data  # Placeholder for the actual formula to calculate lux
    return lux

def flip_light_switch(on):
    if on:
        light_servo.angle = 0  # Angle for 'on' position
    else:
        light_servo.angle = 60  # Angle for 'off' position
    time.sleep(0.5)

def get_moisture_percentage():
    sensor_value = chan.value
    return ((dry_value - sensor_value) / (dry_value - wet_value)) * 100

def spray_water(on):
    if on:
        water_servo.angle = 180  # Angle for spraying water
    else:
        water_servo.angle = 90  # Angle for stopping water spray
    time.sleep(0.5)

# Main loop
try:
    while True:
        # Check the light level
        lux = read_light()
        print(f"Ambient Light: {lux} Lux")
        if lux < 50:
            print("It's dark, flipping light switch on!")
            flip_light_switch(True)
        else:
            print("Light detected, flipping light switch off!")
            flip_light_switch(False)

        # Check the moisture level
        moisture_percentage = get_moisture_percentage()
        print('Moisture Percentage: {:.2f}%'.format(moisture_percentage))
        if moisture_percentage < 55:
            print("Moisture is below 55%, activating water spray.")
            spray_water(True)
        else:
            print("Moisture is above 55%, stopping water spray.")
            spray_water(False)

        time.sleep(2)  # Delay for the loop

except KeyboardInterrupt:
    # Cleanup actions
    print("Program interrupted by user. Turning off devices and exiting.")
    flip_light_switch(False)  # Turn off light switch
    spray_water(False)  # Stop spraying water
