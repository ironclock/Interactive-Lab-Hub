from PIL import Image, ImageDraw, ImageFont
import digitalio
import board
import cv2
import time
import vlc
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

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

unicode_font = ImageFont.truetype(r"/home/joncaceres/Interactive-Lab-Hub/Lab 3/spotipi/resources/apple_emoji.ttc", 160)

def draw_emoji(emoji):    
    display_width = 240
    display_height = 135
    back_ground_color = (0, 0, 0)
    unicode_text = emoji
    
    im = Image.new("RGB", (display_width, display_height), back_ground_color)

    emoji_img = Image.new("RGB", (160, 160), back_ground_color)
    emoji_draw = ImageDraw.Draw(emoji_img)
    emoji_draw.text((0, 0), unicode_text, font=unicode_font, embedded_color=True)
    emoji_img = emoji_img.resize((135, 135))
    
    x_pos = (im.width - emoji_img.width) // 2
    y_pos = (im.height - emoji_img.height) // 2
    
    # Paste the resized emoji onto the main image at the calculated position
    im.paste(emoji_img, (x_pos, y_pos))
    im.save('centered_emoji.png')

    def update_display():
        disp.image(im, 90)  # Directly display the main image

    update_display()
    display = True

def compute_speedup(target_fps):
    FPS_1 = 30
    Speedup_1 = 1.4
    FPS_2 = 23.976023976023978
    Speedup_2 = 1.1

    m = (Speedup_2 - Speedup_1) / (FPS_2 - FPS_1)
    c = Speedup_1 - m * FPS_1

    return m * target_fps + c

def play_video(video_path, start_event):
    start_event.wait()  # Wait for the event signaling to start
    cap = cv2.VideoCapture(video_path)

    # Get the original video's FPS
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    speedup_factor = compute_speedup(original_fps)
    print(f"speed up factor - {speedup_factor}")
    print(f"Original FPS: {original_fps}")

    frame_count = 0
    display_count = 0  # to keep track of displayed frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Only display the frame if the ratio of displayed frames to read frames is less than the inverse of speedup_factor
        if (display_count / (frame_count + 1)) < (1 / speedup_factor):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            im = im.resize((240, 135))
            disp.image(im, 90)
            display_count += 1

        frame_count += 1

    cap.release()


def play_audio(url, start_event):
  # Create a new VLC instance
  instance = vlc.Instance()
  
  # Create a new VLC player
  player = instance.media_player_new()

  # Set media to player
  media = instance.media_new(url)
  player.set_media(media)

  start_event.set()  # Signal the video to start playing
  player.play()

  # Monitor the vlc player's state until it stops.
  while player.get_state() != vlc.State.Ended:
      time.sleep(0.1)

  player.stop()