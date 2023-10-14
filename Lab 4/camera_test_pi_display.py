# --- Start of combined script ---

import cv2
import pyaudio
import wave
import pygame
import digitalio
import board
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Display Initialization

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if display.rotation % 180 == 90:
    height = display.width  # we swap height/width to rotate it to landscape!
    width = display.height
else:
    width = display.width  # we swap height/width to rotate it to landscape!
    height = display.height
image = Image.new("RGB", (width, height))


image = Image.new("RGB", (width, height))

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

def test_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (135, 240))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        display.image(frame_pil)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

# ... [rest of your functions remain unchanged] ...

if __name__ == "__main__":
    while True:
        if buttonA.value and buttonB.value:
            backlight.value = False
        else:
            backlight.value = True

        if buttonB.value and not buttonA.value:
            display.fill(color565(255, 255, 255))
        elif buttonA.value and not buttonB.value:
            test_camera()
        elif not buttonA.value and not buttonB.value:
            display.fill(color565(0, 255, 0))

# --- End of combined script ---
