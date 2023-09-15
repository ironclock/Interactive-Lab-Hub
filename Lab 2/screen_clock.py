import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import astrology_clock
import textwrap


from bs4 import BeautifulSoup
import requests

from adafruit_rgb_display.rgb import color565

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
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
# draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image)

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

days_passed = 0
SIMULATE_TIME_PASSING = True

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        
rotation = 0
imageTwo = Image.new("RGB", (135, 240))

# zodiacString = ">> Aries\nTaurus\nGemini\nCancer\nLeo\nVirgo\nLibra\nScorpio\nSagittarius\nCapricorn\nAquarius\nPisces\n"

zodiacSigns = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
currentIndex = 0

signs = {
    "aries": 1,
    "taurus": 2,
    "gemini": 3,
    "cancer": 4,
    "leo": 5,
    "virgo": 6,
    "libra": 7,
    "scorpio": 8,
    "sagittarius": 9,
    "capricorn": 10,
    "aquarius": 11,
    "pisces": 12,
}

given_sign = "aries"

URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" + \
    str(signs[given_sign])

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')

container = soup.find("p")

print('test - ', container.text.strip())

desired_width = 50
wrapper = textwrap.TextWrapper(width=desired_width)
# wrapped_text = wrapper.fill(long_string)

def getHoroscope(sign):
    # Here, you can fetch the horoscope for the given sign.
    # For now, I'll return a dummy horoscope.
    URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" + \
    str(signs[sign.lower()])
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    container = soup.find("p")
    return wrapper.fill(container.text.strip())

    # return f"Today's horoscope for {sign}: Stay positive and good things will come your way."
    
def displayHoroscope(horoscope):
    # This function will display the horoscope for the selected zodiac sign.
    drawTwo = ImageDraw.Draw(imageTwo)
    drawTwo.rectangle((0, 0, width, height), outline=3, fill=0)
    temp_image = Image.new("RGB", (width, height))
    temp_draw = ImageDraw.Draw(temp_image)
    temp_draw.text((0, 0), horoscope, font=font, fill="#FF0000")
    # Rotate the temporary image
    rotated_image = temp_image.rotate(90, expand=True)
    # Paste the rotated image onto imageTwo
    imageTwo.paste(rotated_image, (0,70))
    disp.image(imageTwo, rotation)

def showList():
    global currentIndex
    drawTwo = ImageDraw.Draw(imageTwo)
    
    arrow_x_position = -10
    arrow_y_position = 70  # Adjust this for where you want the arrow to appear on screen
    space_for_arrow = 35  # Width in pixels that the arrow occupies

    while True:
        # Draw a black filled box to clear the image.
        drawTwo.rectangle((0, 0, width, height), outline=0, fill=0)
        temp_image = Image.new("RGB", (width, height))
        temp_draw = ImageDraw.Draw(temp_image)

        # Adjust the starting y_position based on currentIndex
        starting_y = arrow_y_position - (currentIndex * 20)

        for i, sign in enumerate(zodiacSigns):
            y_position = starting_y + (i * 20)  # Adjust this value based on your font size
            temp_draw.text((arrow_x_position + space_for_arrow, y_position), sign, font=font, fill="#FF0000")
        
        # Draw arrow on the temp image
        temp_draw.text((arrow_x_position, arrow_y_position), "->", font=font, fill="#FFFFFF")
        
        # Rotate the temporary image
        rotated_image = temp_image.rotate(90, expand=True)
        
        # Paste the rotated image onto imageTwo
        imageTwo.paste(rotated_image, (0, 70))
        
        disp.image(imageTwo, rotation)

        if not buttonA.value and buttonB.value:  # Move up
            currentIndex = (currentIndex - 1) % len(zodiacSigns)
            time.sleep(0.1)
        elif buttonA.value and not buttonB.value:  # Move down
            currentIndex = (currentIndex + 1) % len(zodiacSigns)
            time.sleep(0.1)
        elif not buttonA.value and not buttonB.value:  # Select
            horoscope = getHoroscope(zodiacSigns[currentIndex])
            displayHoroscope(horoscope)
            break


while True:
    if buttonA.value and not buttonB.value or not buttonA.value and buttonB.value:  # just button A
        disp.fill(color565(0, 0, 0))  # set the screen to black
        showList()
        break
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=400)

    days_passed += 0.6
    astrology_clock.create_astrology_clock()

    image = Image.open("astrology_clock.png")

    # Scale, crop, and center the image here
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
    
    # time.sleep(1)  # wait before next iteration