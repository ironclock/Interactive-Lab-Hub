import time
from adafruit_servokit import ServoKit
import numpy as np

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.servo[0]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo.set_pulse_width_range(500, 2500)

def oscillate_move():
    """Oscillate the servo between defined angles, stopping in between."""
    while True:
        # Move from 100 to 105
        for angle in range(100, 106, 1):
            print("forward : ", angle)
            servo.angle = angle
            time.sleep(0.5)

        # Stop by setting to 90
        servo.angle = 90
        time.sleep(0.5)  # Pause

        # Set to 80
        # servo.angle = 80
        # time.sleep(0.5)  # Allow the servo to settle at 80

        # Move from 80 to 75
        for angle in np.arange(80, 78, -0.5):
            print("reverse : ", angle)
            servo.angle = angle
            time.sleep(0.5)

        # Stop by setting to 90
        servo.angle = 90
        time.sleep(0.5)  # Pause before next loop iteration

while True:
    try:
        oscillate_move()
        # gradual_move(105)
        # # time.sleep(2)  # Wait before moving again
        # print("reversing")
        # # Move back to 0 degrees and wait for completion
        # gradual_move(100, False)
        # # time.sleep(2)
        
    except KeyboardInterrupt:
        # Once interrupted, set the servo back to 0 degree position
        servo.angle = 90
        time.sleep(0.5)
        break
