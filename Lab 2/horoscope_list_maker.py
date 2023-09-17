# Copyright Shai Aarons, Ariana Bhigroog, Jon Caceres, Rachel Minkowitz, Amando Xu
# This file was only used to generate the zodiac list images

from PIL import Image, ImageDraw, ImageFont
import datetime

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# define the Zodiac signs and their respective days
ZODIAC_SIGNS = [
    (0, "Aries", (21, 3), (19, 4), "\u2648"),
    (1, "Taurus", (20, 4), (20, 5), "\u2649"),
    (2, "Gemini", (21, 5), (20, 6), "\u264A"),
    (3, "Cancer", (21, 6), (22, 7), "\u264B"),
    (4,"Leo", (23, 7), (22, 8), "\u264C"),
    (5, "Virgo", (23, 8), (22, 9), "\u264D"),
    (6, "Libra", (23, 9), (22, 10), "\u264E"),
    (7, "Scorpio", (23, 10), (21, 11), "\u264F"),
    (8, "Sagittarius", (22, 11), (21, 12), "\u2650"),
    (9, "Capricorn", (22, 12), (19, 1), "\u2651"),
    (10, "Aquarius", (20, 1), (18, 2), "\u2652"),
    (11, "Pisces", (19, 2), (20, 3), "\u2653"),
    (12, "Go back to clock", (0, 0), (0, 0), ">")
]

# create a list of the zodiac signs
def create_zodiac_list_image():
    width, height = 240, 135

    # load zodiac signs
    base = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    
    draw = ImageDraw.Draw(base)
    
    y_position = -110
    for idx, sign, start, end, symbol in ZODIAC_SIGNS:
        text = ""
        if idx == 12:
            text = f"{symbol} - {sign}"
        else:
            text = f"{symbol} - {sign}: {start[1]}/{start[0]} to {end[1]}/{end[0]}"
        color = "red" if idx == 11 else "white"
        draw.text((10, y_position), text, font=font, fill=color)
        y_position += 20  # Move down 20 pixels for the next text

    # save the resulting image
    base = base.convert('RGB')  # ensure it's in RGB mode
    base = base.quantize(colors=128).convert('RGB')  # quantize and then convert back to 'RGB'

    base.save('zodiac_list_11.png')

if __name__ == "__main__":
    create_zodiac_list_image()