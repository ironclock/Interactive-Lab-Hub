# Copyright Shai Aarons, Ariana Bhigroog, Jon Caceres, Rachel Minkowitz, Amando Xu

from PIL import Image, ImageDraw, ImageFont
import datetime

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# define the Zodiac signs and their respective days
ZODIAC_SIGNS = [
    (0, "Aries", (21, 3), (19, 4, 23, 59, 59)),
    (1, "Taurus", (20, 4), (20, 5, 23, 59, 59)),
    (2, "Gemini", (21, 5), (20, 6, 23, 59, 59)),
    (3, "Cancer", (21, 6), (22, 7, 23, 59, 59)),
    (4, "Leo", (23, 7), (22, 8, 23, 59, 59)),
    (5, "Virgo", (23, 8), (22, 9, 23, 59, 59)),
    (6, "Libra", (23, 9), (22, 10, 23, 59, 59)),
    (7, "Scorpio", (23, 10), (21, 11, 23, 59, 59)),
    (8, "Sagittarius", (22, 11), (21, 12, 23, 59, 59)),
    (9, "Capricorn", (22, 12), (19, 1, 23, 59, 59)),
    (10, "Aquarius", (20, 1), (18, 2, 23, 59, 59)),
    (11, "Pisces", (19, 2), (20, 3, 23, 59, 59))
]

INITIAL_IMAGE_OFFSET = 60

# Global variables
speed_up = False
virtual_time_offset = datetime.timedelta(0)  # initialized to zero

def get_current_zodiac():
    global virtual_time_offset

    # Get current real-world time
    real_time_now = datetime.datetime.now()

    # Calculate the offset based on speed_up
    if speed_up:
        virtual_time_offset += datetime.timedelta(seconds=90000)

    # Adjusted virtual time
    now = real_time_now + virtual_time_offset

    current_year = now.year
    
    for idx, sign, start, end in ZODIAC_SIGNS:
        start_year = now.year
        end_year = now.year
        
        if (now.month, now.day) < (start[1], start[0]) and start[1] > end[1]:
            end_year = now.year
        elif (now.month, now.day) >= (start[1], start[0]) and start[1] > end[1]:
            end_year += 1

        start_date = datetime.datetime(start_year, start[1], start[0])
        end_date = datetime.datetime(end_year, end[1], end[0], *end[2:]) if len(end) > 2 else datetime.datetime(end_year, end[1], end[0])

        if start_date <= now < end_date:
            print(f"For {sign}, Start Date: {start_date}, End Date: {end_date}, Now: {now}")
        
        if start_date <= now < end_date:  # Check if the current date falls within the sign's range
            total_seconds_in_sign = (end_date - start_date).total_seconds()
            seconds_passed = (now - start_date).total_seconds()

            progress = seconds_passed / total_seconds_in_sign
            return sign, progress
        
        # Adjust for zodiac signs that span two years
        if start[1] > end[1]:  # Sign spans two years
            start_date = datetime.datetime(start_year - 1, start[1], start[0])
            if start_date <= now < end_date:
                total_seconds_in_sign = (end_date - start_date).total_seconds()
                seconds_passed = (now - start_date).total_seconds()

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

    sign, progress = get_current_zodiac()
    zodiac_index = [zodiac[1] for zodiac in ZODIAC_SIGNS].index(sign)

    # Determine the angle needed to place the end of the current zodiac at the top center of the screen.
    rotation_offset = 30 * (zodiac_index - 4)  # Adjusting the subtraction to 4 to correct the rotation.

    # Adjust for the progress through the current zodiac sign
    rotation_progress = 30 * progress

    # Combine all angles: start with the image's initial offset, then apply the rotation for the current zodiac, and finally adjust for the progress through the zodiac.
    rotation = INITIAL_IMAGE_OFFSET + rotation_offset + rotation_progress

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