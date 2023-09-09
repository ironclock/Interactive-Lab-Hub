# Copyright Shai Aarons, Ariana Bhigroog, Jon Caceres, Rachel Minkowitz, Amando Xu

from PIL import Image, ImageDraw
import datetime

# Define the Zodiac signs and their respective days
ZODIAC_SIGNS = [
    ("Aries", (21, 3), (19, 4)),
    ("Taurus", (20, 4), (20, 5)),
    ("Gemini", (21, 5), (20, 6)),
    ("Cancer", (21, 6), (22, 7)),
    ("Leo", (23, 7), (22, 8)),
    ("Virgo", (23, 8), (22, 9)),
    ("Libra", (23, 9), (22, 10)),
    ("Scorpio", (23, 10), (21, 11)),
    ("Sagittarius", (22, 11), (21, 12)),
    ("Capricorn", (22, 12), (19, 1)),
    ("Aquarius", (20, 1), (18, 2)),
    ("Pisces", (19, 2), (20, 3))
]

# Fetch the current zodiac sign and the progress through it
def get_current_zodiac(simulate_time_passing, increment):
    if simulate_time_passing:
        now = datetime.datetime.now() + datetime.timedelta(days=increment)
    else:
        now = datetime.datetime.now()
    for sign, start, end in ZODIAC_SIGNS:
        start_date = datetime.datetime(now.year, start[1], start[0])
        end_date = datetime.datetime(now.year, end[1], end[0])
        if start_date <= now <= end_date:
            days_in_sign = (end_date - start_date).days + 1
            day_of_sign = (now - start_date).days
            progress = day_of_sign / days_in_sign
            return sign, progress

    # Default return if no zodiac range matches.
    return "Unknown", 0.0

# Create the clock image
def create_astrology_clock(simulate_time_passing, increment):
    width, height = 240, 135

    # Load zodiac signs
    zodiac_background = Image.open("nightsky_fifty.jpg") # You should have this image
    earth = Image.open("earth.png")  # This should be a small image of Earth
    # earth = earth.resize((100, 100))

    # Calculate rotation based on current zodiac and progress
    _, progress = get_current_zodiac(simulate_time_passing, increment)
    rotation = 278 + (360 * progress)

    # Rotate zodiac
    zodiac_background = zodiac_background.rotate(rotation)

    # Create base image
    base = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    base.paste(zodiac_background, (-190, -80))
    
    # Draw earth and line
    earth_position = ((width - earth.width) // 2, height - earth.height)
    base.paste(earth, earth_position, earth)  # Using earth as mask for transparency

    draw = ImageDraw.Draw(base)
    line_start = (width // 2, earth_position[1])
    line_end = (width // 2, 0)
    draw.line([line_start, line_end], fill="red", width=2)

    # Save the resulting image
    base = base.convert('RGB')  # Ensure it's in RGB mode
    base = base.quantize(colors=128).convert('RGB')  # Quantize and then convert back to 'RGB'

    base = base.rotate(90, expand=True)

    base.save('astrology_clock.png')

if __name__ == "__main__":
    create_astrology_clock()