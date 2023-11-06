import time
import subprocess
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from keras.models import load_model

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = [line.strip() for line in open("labels.txt", "r").readlines()]

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class. Make sure to use the correct width and height.
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Load default font.
font = ImageFont.load_default()

# Create blank image for drawing.
image = Image.new('1', (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Change the camera selection here
camera = cv2.VideoCapture('/dev/video0')
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # Grab the camera's image.
        ret, image_cam = camera.read()

        if not ret:
            print("Failed to grab image")
            break

        # Resize the raw image into (224x224) pixels
        image_resized = cv2.resize(image_cam, (224, 224), interpolation=cv2.INTER_AREA)

        # Prepare the image for prediction
        image_array = np.asarray(image_resized, dtype=np.float32)
        image_array = (image_array / 127.5) - 1
        image_array = np.expand_dims(image_array, axis=0)

        # Predicts the model
        prediction = model.predict(image_array)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score to OLED
        draw.text((0, 0), f"Status: {class_name}", font=font, fill=255)
        # draw.text((0, 8), f"Confidence: {np.round(confidence_score * 100, 2)}%", font=font, fill=255)

        # Display image.
        oled.image(image)
        oled.show()

        time.sleep(0.5)  # Refresh rate

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    camera.release()
    # Clear the display.
    oled.fill(0)
    oled.show()
    print("Cleaned up and exited.")
