import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_servokit import ServoKit
import smbus

# Computer vision and OLED imports
import subprocess
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from keras.models import load_model

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

# Disable scientific notation for clarity - computer vision
np.set_printoptions(suppress=True)

# Load the model - computer vision
model = load_model("keras_Model.h5", compile=False)

# Load the labels - computer vision
class_names = [line.strip() for line in open("labels.txt", "r").readlines()]

# Create the SSD1306 OLED class. Make sure to use the correct width and height - computer vision
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Load default font - computer vision
font = ImageFont.load_default()

# Create blank image for drawing - computer vision
image = Image.new('1', (oled.width, oled.height))

# Get drawing object to draw on image - computer vision
draw = ImageDraw.Draw(image)

# Change the camera selection here - computer vision
camera = cv2.VideoCapture('/dev/video0')
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

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

def update_oled(class_name):
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # Print prediction to OLED
    draw.text((0, 0), f"Status: {class_name}", font=font, fill=255)
    # Display image.
    oled.image(image)
    oled.show()

def get_plant_health():
    # Grab the camera's image.
    ret, image_cam = camera.read()
    if not ret:
        print("Failed to grab image")
        return "Error"

    # Resize the raw image into (224x224) pixels
    image_resized = cv2.resize(image_cam, (224, 224), interpolation=cv2.INTER_AREA)
    # Prepare the image for prediction
    image_array = np.asarray(image_resized, dtype=np.float32)
    image_array = (image_array / 127.5) - 1
    image_array = np.expand_dims(image_array, axis=0)
    # Predicts the model
    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    return class_names[index]

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
        
        # Computer vision for plant health
        plant_health = get_plant_health()
        update_oled(plant_health)
        print(f"Plant Health: {plant_health}")

        time.sleep(2)  # Delay for the loop

except KeyboardInterrupt:
    # Cleanup actions
    print("Program interrupted by user. Turning off devices and exiting.")
    flip_light_switch(False)  # Turn off light switch
    spray_water(False)  # Stop spraying water
    camera.release()
    oled.fill(0)
    oled.show()
    print("Cleaned up and exited.")
