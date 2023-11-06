import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS1115 ADC instance and set the gain
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Create an analog input channel on pin A0
chan = AnalogIn(ads, ADS.P0)

dry_value = 20000  # Replace with your value for dry soil
wet_value = 8000

while True:
    # Read the sensor
    sensor_value = chan.value

    # Convert the sensor reading to a percentage
    moisture_percentage = ((dry_value - sensor_value) / (dry_value - wet_value)) * 100

    # Make sure the percentage is within the bounds of 0 to 100
    moisture_percentage = max(min(moisture_percentage, 100), 0)

    # Print out the value
    print('Moisture Percentage: {:.2f}%'.format(moisture_percentage))
    time.sleep(1)
