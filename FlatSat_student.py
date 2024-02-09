#!/usr/bin/ python3
"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

# AUTHOR: @Earl Chan, @Hudson Hilal
# DATE: 2/18/2024

# import libraries
import time
import board
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2
import random

from datetime import date
import datetime

# VARIABLES
THRESHOLD = 20  # Any desired value from the accelerometer
# Your github repo path: ex. /home/pi/FlatSatChallenge
REPO_PATH = "/home/pi/Projects/Winton-Satalite-Squad"
FOLDER_PATH = "Images"  # Your image folder path in your GitHub repo: ex. /Images

# imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

def mock_name_gen(name):
    return "3982157o2uyhjfnds.jpg"


def img_name_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    
    t = datetime.datetime.now().isoformat()
    imgname = (f'{FOLDER_PATH}/{name}_{t}.jpg')
    return imgname

def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """
    '''
    accelx, accely, accelz = accel_gyro.acceleration
    print(str(accelx) + " " + str(accely) + " " + str(accelz))
    accelmagnitude = math.sqrt(accelx**2 + accely**2 + accelz**2)

    '''
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)
    picam2.options["quality"] = 95
    picam2.start()
    picam2.capture_file(img_name_gen("KatieK"))
    picam2.stop()

def take_photo_imu():
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        print(f"accel x:{accelx} y:{accely} z{accelz}")
        accelmagnitude = math.sqrt(accelx**2 + accely**2 + accelz**2)

        if accelmagnitude > THRESHOLD:
            print(f"taking photo, mag: {accelmagnitude}")
            take_photo()
            break

def main():
    take_photo()
    take_photo_imu()


if __name__ == '__main__':
    main()
