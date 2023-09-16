import time
import subprocess
import digitalio
import board
import threading
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
font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        
rotation = 0
imageTwo = Image.new("RGB", (135, 240))

zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
current_index = 0

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

desired_width = 26
wrapper = textwrap.TextWrapper(width=desired_width)

def get_horoscope(sign):
    global stop_loading
    stop_loading = False
    loading_thread = threading.Thread(target=display_loading_screen)
    loading_thread.start()
    URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" + \
    str(signs[sign.lower()])
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    container = soup.find("p")
    result = wrapper.fill(container.text.strip())

    stop_loading = True
    loading_thread.join()

    return result

def display_loading_screen():
    loading_image = Image.open("media/loading.png")
    angle = 0

    while not stop_loading:
        draw_two = ImageDraw.Draw(imageTwo)
        draw_two.rectangle((0, 0, width, height), outline=3, fill=0)

        # rotate the loading image
        rotated_loading = loading_image.rotate(angle, resample=Image.BICUBIC, center=(loading_image.width/2, loading_image.height/2))
        
        # position the loading image in the center
        x = (width - rotated_loading.width) // 2
        y = (height - rotated_loading.height) // 2

        imageTwo.paste(rotated_loading, (x, y), rotated_loading)

        disp.image(imageTwo, rotation)
        
        angle += -20  # adjust for the speed of the rotation. higher value = faster spinning
        time.sleep(0.1)  # adjust sleep duration to control refresh rate of the spinning

stop_loading = False

current_index = 0
    
def display_horoscope(horoscope):
    width = 240

    temp_image = Image.new('RGB', (width, 1), (0, 0, 0))
    draw_temp = ImageDraw.Draw(temp_image)
    
    text_width, text_height = draw_temp.textsize(horoscope, font=font_small)
    
    height = text_height + 10
    base = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(base)
    x_position = 0
    y_position = 0
    draw.text((x_position, y_position), horoscope, font=font_small, fill="white")
    base.save('horoscope_display.png')
    
    image = Image.open("horoscope_display.png")
    current_y = 0
    step_size = 10

    def update_display():
        cropped = image.crop((0, current_y, 240, current_y + 135))
        disp.image(cropped, 90)

    update_display()
    display = True

    while display:
        if not buttonA.value and buttonB.value:  # Move up
            current_y = max(0, current_y - step_size)
            update_display()
            time.sleep(0.1)
        elif buttonA.value and not buttonB.value:  # Move down
            max_y = image.height - 135
            current_y = min(max_y, current_y + step_size)
            update_display()
            time.sleep(0.1)
        elif not buttonA.value and not buttonB.value:  # Select
            display = False
            time.sleep(0.5)
            show_list()
            break

# show the zodiac list that the user can scroll through
def show_list():
    global current_index
    draw_two = ImageDraw.Draw(imageTwo)
    draw_two.rectangle((0, 0, width, height), outline=0, fill=0)

    while True:
        # draw a black filled box to clear the image
        image_path = f"zodiac_list/zodiac_list_{current_index}.png"
        image = Image.open(image_path)

        # scale, crop, and center the image here
        image = image.resize((240, 135), Image.BICUBIC)
        disp.image(image, 90)

        if buttonA.value and not buttonB.value:  # move up
            current_index = min(current_index + 1, 11)  # increment the index but don't exceed 11
            time.sleep(0.1)
        elif not buttonA.value and buttonB.value:  # move down
            current_index = max(current_index - 1, 0)  # decrement the index but don't go below 0
            time.sleep(0.1)
        elif not buttonA.value and not buttonB.value:  # select
            time.sleep(0.5)
            horoscope = get_horoscope(zodiac_signs[current_index])
            display_horoscope(horoscope)
            break

# main logic
while True:
    if buttonA.value and not buttonB.value or not buttonA.value and buttonB.value:  # press any button
        disp.fill(color565(0, 0, 0))  # set the screen to black
        show_list()
        break
    
    # draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=400)

    astrology_clock.create_astrology_clock()

    image = Image.open("astrology_clock.png")

    # scale, crop, and center the image here
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
    
    # display astrology clcok image
    disp.image(image)
    
    time.sleep(0.1)  # wait before next iteration