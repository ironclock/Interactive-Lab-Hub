import smbus
import time

# Define some constants from the datasheet
DEVICE_ADDRESS = 0x10  # 7-bit address (will be left-shifted to add the read/write bit)
ALS_CONF = 0x00  # Ambient Light Sensing (ALS) Configuration Register
ALS = 0x04  # ALS high resolution output data

# Initialize the I2C bus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# Configure the sensor
# For example, gain = 1/8, integration time = 25 ms
bus.write_word_data(DEVICE_ADDRESS, ALS_CONF, 0x1800)

def read_light():
    # Read data from I2C interface
    data = bus.read_word_data(DEVICE_ADDRESS, ALS)
    # The data might need some processing here depending on the configuration
    lux = data  # Placeholder for processing formula
    return lux

try:
    while True:
        lux = read_light()
        print(f"Ambient Light: {lux} Lux")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
