import os
import board
import busio
import adafruit_ssd1306
from adafruit_bitmap_font import bitmap_font

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Load the font file
font_path = os.path.join(os.path.dirname(__file__), 'font5x8.bin')
font = bitmap_font.load_font(font_path)

# Clear display.
oled.fill(0)
oled.show()

# Text display parameters
x = 0  # X position of the start of the text.
y = 15  # Y position of the start of the text (centers it on the screen vertically if the screen is 32 pixels in height).

# Write text on the screen using the loaded font
oled.text('Unhealthy', x, y, 1, font=font)

# Display what's drawn on the screen
oled.show()
