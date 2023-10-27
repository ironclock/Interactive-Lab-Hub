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
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.servo[0]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo.set_pulse_width_range(500, 2500)

# Display Initialization

GPIO.setmode(GPIO.BCM)
LASER_1_PIN = 16
LASER_2_PIN = 26

GPIO.setup(LASER_1_PIN, GPIO.OUT)
GPIO.setup(LASER_2_PIN, GPIO.OUT)

def turn_on_laser(pin):
    GPIO.output(pin, True)

def turn_off_laser(pin):
    GPIO.output(pin, False)

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
alert_sound = pygame.mixer.Sound('/home/joncaceres/Interactive-Lab-Hub/Lab 4/bender_home_security/media/kill_all_humans_loud_2.wav')
alert_sound.set_volume(1.0)

last_time_played = 0  # Global variable to store the last time the audio was played
COOLDOWN = 5  # Time (in seconds) to wait before playing the sound again

# YOLO Initialization
net = cv2.dnn.readNet("yolov4-tiny.weights", "/home/joncaceres/Interactive-Lab-Hub/Lab 4/bender_home_security/darknet/cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
print("pooop")
print(net.getUnconnectedOutLayers())
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def oscillate_move(stop_event):
    """Oscillate the servo between defined angles, stopping in between."""
    while not stop_event.is_set():
        # Move from 100 to 105
        for angle in range(100, 106, 1):
            if stop_event.is_set():
                servo.angle = 90
                return
            print("forward : ", angle)
            servo.angle = angle
            time.sleep(0.5)

        # Stop by setting to 90
        servo.angle = 90
        time.sleep(0.5)  # Pause

        # Move from 80 to 75
        for angle in np.arange(80, 78, -0.5):
            if stop_event.is_set():
                servo.angle = 90
                return
            print("reverse : ", angle)
            servo.angle = angle
            time.sleep(0.5)

        # Stop by setting to 90
        servo.angle = 90
        time.sleep(0.5)  # Pause before next loop iteration

def test_camera_with_detection():
    import threading

    stop_event = threading.Event()  # This will help us control the oscillate_move function

    # Start the servo oscillation in a separate thread
    servo_thread = threading.Thread(target=oscillate_move, args=(stop_event,))
    servo_thread.start()

    global last_time_played
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    sound_played = False  # Initialize the flag

    while True:
        ret, frame = cap.read()
        height, width, channels = frame.shape

        # Detect objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (288, 288), (0, 0, 0), True, crop=False)
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

                    # If human is detected, set the stop event
                    stop_event.set()

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
                        turn_on_laser(LASER_1_PIN)
                        turn_on_laser(LASER_2_PIN)
                        last_time_played = current_time
                        stop_event.set()  # Ensure the oscillate_move function is stopped when exiting
                        servo_thread.join()
                        break

        frame = cv2.resize(frame, (240, 135))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_pil = frame_pil.rotate(90, expand=1)
        display.image(frame_pil)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            servo.angle = 90
            servo.angle = 90
            servo.angle = 90
            servo.angle = 90
            stop_event.set()  # Ensure the oscillate_move function is stopped when exiting
            servo_thread.join()
            break

    cap.release()

if __name__ == "__main__":
    backlight.value = True
    try:
        while True:
            test_camera_with_detection()
    except KeyboardInterrupt:
        servo.angle = 90
        servo.angle = 90
        servo.angle = 90
        servo.angle = 90
        servo.angle = 90
        print("Script terminated by user.")
        turn_off_laser(LASER_1_PIN)
        turn_off_laser(LASER_2_PIN)

        backlight.value = False
        cv2.destroyAllWindows()
