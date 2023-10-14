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
import time

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
# if display.rotation % 180 == 90:
# height = display.width  
# width = display.height
# else:
    # width = display.width
    # height = display.height
image = Image.new("RGB", (240, 135))

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Sound initialization
pygame.mixer.init()
alert_sound = pygame.mixer.Sound('/home/joncaceres/Interactive-Lab-Hub/Lab 4/bender_home_security/media/kill_all_humans.wav')

last_time_played = 0  # Global variable to store the last time the audio was played
COOLDOWN = 5  # Time (in seconds) to wait before playing the sound again

# YOLO Initialization
net = cv2.dnn.readNet("yolov4-tiny.weights", "/home/joncaceres/Interactive-Lab-Hub/Lab 4/bender_home_security/darknet/cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
print("pooop")
print(net.getUnconnectedOutLayers())
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def test_camera_with_detection():
    global last_time_played
    cap = cv2.VideoCapture(0)
    sound_played = False  # Initialize the flag
    while True:
        ret, frame = cap.read()
        height, width, channels = frame.shape

        # Detect objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        human_detected = False  # Flag to check if human is detected in current frame

        # Process detected objects
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                current_time = time.time()
                if confidence > 0.5 and class_id == 0:  # Class ID 0 is for person in the coco dataset
                    human_detected = True
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    if human_detected and (current_time - last_time_played > COOLDOWN):
                        alert_sound.play()
                        last_time_played = current_time

        frame = cv2.resize(frame, (240, 135))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_pil = frame_pil.rotate(90, expand=1)
        display.image(frame_pil)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

# ... [rest of your functions remain unchanged] ...

if __name__ == "__main__":
    backlight.value = True
    try:
        while True:
            test_camera_with_detection()
    except KeyboardInterrupt:
        print("Script terminated by user.")
        backlight.value = False
        cv2.destroyAllWindows()
