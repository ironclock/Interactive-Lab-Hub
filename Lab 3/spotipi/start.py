# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import
import listener
import api
import json
import time
import subprocess
import re
import ast
from enum import Enum
from io import BytesIO
import helper

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

image = Image.open("template.jpg")
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Scale the image to the smaller screen dimension
image_ratio = image.width / image.height
screen_ratio = width / height
if screen_ratio < image_ratio:
    scaled_width = image.width * height // image.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = image.height * width // image.width
image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image = image.crop((x, y, x + width, y + height))

# Display image.
disp.image(image)

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

with open("instructions.json", "r") as file:
    INSTRUCTIONS = json.load(file)

QUESTION = "Tell me how you are feeling today or request a song you'd like to here" # misspelled intentionally to correct pronunciation
MOOD_QUESTION = "Do you want to feel different or continue feeling the same?"

class INSTRUCTION_TYPE(Enum):
   FIRST = "FIRST"
   SECOND = "SECOND"

def speak(message):
    formatted_message = "echo \"" + message + "\" | festival --tts"
    subprocess.run(['/bin/bash', '-c', formatted_message])

def ask_question(command):
    speak(command)
    helper.draw_emoji("🤔")
    return listener.start()
    
def handle_flow_1(content):
    print('flow 1')
    print(content)
    response_content = content
    if 'flow_1' in content:
        response_content = content['flow_1']
        query = f"{response_content['song_name']} by {response_content['artist_name']}"
        print(query)
        result = api.search_youtube(query, max_results = 1)
        now_playing = "Now playing " + str(response_content['song_name']) + " by " + str(response_content['artist_name'])
        print(now_playing)
        speak(now_playing)
        time.sleep(3)
        # helper.draw_emoji("🎶")
        api.playYoutubeVideo(result)
        time.sleep(90)
    else:
        print("Error: flow_1 key not found in content.")
        handle_flow_3(content)

def handle_flow_2(content):
    print('flow 2')
    emoji = content['flow_2']['emoji']
    if emoji:
        helper.draw_emoji(emoji)
    message = ask_question(MOOD_QUESTION)
    r = api.callGPT(message, instruction_type = INSTRUCTION_TYPE.SECOND.value, mood = content['flow_2']['mood'], emoji = content['flow_2']['emoji'])
    print(r)
    response_content = json.loads(r)
    query = f"{ response_content['song_name'] } by { response_content['artist_name'] }"

    result = api.search_youtube(query, max_results = 1)
    now_playing = "Now playing " + str(response_content['song_name']) + " by " + str(response_content['artist_name'])
    print(now_playing)
    speak(now_playing)
    time.sleep(3)
    # helper.draw_emoji("🎶")
    api.playYoutubeVideo(result)

def handle_flow_3(content):
    print('error - flow 3')
    print(content)
    helper.draw_emoji("🤨")
    speak("I did not understand your request, please try again")
    # ask_question(QUESTION)

while True:
    helper.draw_emoji("😌")  # greeting face
    message = ask_question(QUESTION)
    # Adjusting the way we pass the instructions to callGPT()
    r = api.callGPT(message, instruction_type=INSTRUCTION_TYPE.FIRST.value, emoji="")
    print(r)
    
    # Try to evaluate the string
    try:
        ast.literal_eval(r)
    except (ValueError, SyntaxError):
        handle_flow_3({})
        continue

    content = {}
    try:
        content = json.loads(r)
    except json.JSONDecodeError:
        handle_flow_3({})
        continue

    if 'flow_1' in content:
        handle_flow_1(content)
        continue
    elif 'flow_2' in content:
        handle_flow_2(content)
    else:
        handle_flow_3(content)