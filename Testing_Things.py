# import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2
i2c = board.I2C()
print(i2c)
accel_gyro = LSM6DS(i2c, 0x708)


