# Copyright Shai Aarons, Ariana Bhigroog, Jon Caceres, Rachel Minkowitz, Amando Xu

from PIL import Image, ImageDraw, ImageFont
import datetime

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# define the Zodiac signs and their respective days
ZODIAC_SIGNS = [
    (0, "Aries", (21, 3), (19, 4)),
    (1, "Taurus", (20, 4), (20, 5)),
    (2, "Gemini", (21, 5), (20, 6)),
    (3, "Cancer", (21, 6), (22, 7)),
    (4,"Leo", (23, 7), (22, 8)),
    (5, "Virgo", (23, 8), (22, 9)),
    (6, "Libra", (23, 9), (22, 10)),
    (7, "Scorpio", (23, 10), (21, 11)),
    (8, "Sagittarius", (22, 11), (21, 12)),
    (9, "Capricorn", (22, 12), (19, 1)),
    (10, "Aquarius", (20, 1), (18, 2)),
    (11, "Pisces", (19, 2), (20, 3))
]

# fetch the current zodiac sign and the progress through it
def get_current_zodiac():
    now = datetime.datetime.now()
    for idx, sign, start, end in ZODIAC_SIGNS:
        start_date = datetime.datetime(now.year, start[1], start[0])
        if idx < 11:
            next_object = ZODIAC_SIGNS[idx+1]
        else:
            next_object = ZODIAC_SIGNS[0]
        next_start_date = datetime.datetime(now.year, next_object[2][1], next_object[2][0])
        end_date = datetime.datetime(now.year, end[1], end[0])
        # print('end date - ', end_date)
        if start_date <= now < end_date:
            total_seconds_in_sign = (end_date - start_date).total_seconds()
            seconds_passed = (now - start_date).total_seconds()
            progress = seconds_passed / total_seconds_in_sign
            return sign, progress
        elif end_date <= now <= next_start_date:
            total_seconds_in_sign = (end_date - start_date).total_seconds()
            seconds_passed = total_seconds_in_sign + (now - end_date).total_seconds()
            progress = seconds_passed / total_seconds_in_sign
            return sign, progress

    # default return if no zodiac range matches
    return "Unknown", 0.0

# create the clock image
def create_astrology_clock():
    width, height = 240, 135

    # load zodiac signs
    zodiac_background = Image.open("nightsky_fifty.jpg") # our night sky image :)
    earth = Image.open("earth.png")  # this should be a small image of Earth

    # calculate rotation based on current zodiac and progress
    sign, progress = get_current_zodiac()
    rotation = 90 + ((360 / 12) * progress)

    # rotate zodiac
    zodiac_background = zodiac_background.rotate(rotation)

    # create base image
    base = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    base.paste(zodiac_background, (-190, -80))
    
    # draw earth and line
    earth_position = ((width - earth.width) // 2, height - earth.height)
    base.paste(earth, earth_position, earth)  # using earth as mask for transparency

    draw = ImageDraw.Draw(base)
    line_start = (width // 2, earth_position[1])
    line_end = (width // 2, 0)
    draw.line([line_start, line_end], fill="red", width=2)

    progress_text = f"Progress\n{sign} - {progress*100:.4f}%"
    progress_text_position = (10, height - 40) 

    outline_thickness = 1
    for x in range(-outline_thickness, outline_thickness + 1):
        for y in range(-outline_thickness, outline_thickness + 1):
            draw.text((progress_text_position[0] + x, progress_text_position[1] + y), progress_text, font=font, fill="black")

    draw.text(progress_text_position, progress_text, font=font, fill="white")

    press_any_button = f"Press any button \nto continue"
    button_text_position = (10, 5) 

    for x in range(-outline_thickness, outline_thickness + 1):
        for y in range(-outline_thickness, outline_thickness + 1):
            draw.text((button_text_position[0] + x, button_text_position[1] + y), press_any_button, font=font, fill="black")

    draw.text(button_text_position, press_any_button, font=font, fill="white")

    # save the resulting image
    base = base.convert('RGB')  # ensure it's in RGB mode
    base = base.quantize(colors=128).convert('RGB')  # quantize and then convert back to 'RGB'

    base = base.rotate(90, expand=True)

    base.save('astrology_clock.png')

if __name__ == "__main__":
    create_astrology_clock()