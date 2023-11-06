import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.servo[11]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
servo.set_pulse_width_range(500, 2500)

# Start at 0 degree
servo.angle = 60
time.sleep(2)

try:
    # Initially, we set the direction to clockwise (1) or counter-clockwise (-1)
    direction = -1
    # Start the loop
    while True:
        if direction == 1:
            # Move 5 degrees clockwise
            new_angle = servo.angle + 60
            # Ensure that we do not go over 180 degrees
            if new_angle > 180:
                new_angle = 180
            servo.angle = new_angle
            print("New angle - ", servo.angle)
            time.sleep(2)  # Wait for 2 seconds
            # Change direction to counter-clockwise
            direction = -1
        
        elif direction == -1:
            # Move 10 degrees counter-clockwise
            new_angle = servo.angle - 60
            # Ensure that we do not go below 0 degrees
            if new_angle < 0:
                new_angle = 0
            servo.angle = new_angle
            print("New angle - ", servo.angle)
            time.sleep(2)  # Wait for 2 seconds
            # Change direction to clockwise
            direction = 1

except KeyboardInterrupt:
    # Once interrupted, set the servo back to 0 degree position
    servo.angle = 60
    time.sleep(0.5)
