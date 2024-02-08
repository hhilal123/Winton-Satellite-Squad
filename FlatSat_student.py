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

# AUTHOR:
# DATE:

# import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

from datetime import date

# VARIABLES
THRESHOLD = 5  # Any desired value from the accelerometer
# Your github repo path: ex. /home/pi/FlatSatChallenge
REPO_PATH = "/home/pi/Projects/Winton-Satalite-Squad"
FOLDER_PATH = "/Images"  # Your image folder path in your GitHub repo: ex. /Images

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


def img_name_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    return imgname

def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """

    #Index 0 is the count since last photo, and index 1 is for lastest, index 2 is for second latest, etc etc. 
    lastphoto = [0,-1,-1,-1]
    
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        print(accelx + " " + accely + " " + accelz)
        acceltotal = accelx + accely + accelz
        if (acceltotal > THRESHOLD):
            camera_config = Picamera2.create_still_configuration
            picam2.configure(camera_config)
            picam2.capture_file(img_name_gen(str(date.today())))
            
            lastphoto[0] = 0
            lastphoto[3] = lastphoto[2]
            lastphoto[2] = lastphoto[1]
            lastphoto[1] = 0
        time.sleep(1)

        #Meant to check if a slot is active/if a 1st second or third latest photo have been taken
        for index, x in enumerate(lastphoto):
            if x >= 0 
                lastphoto[index] = lastphoto[index] + 1

        #Checks if the average time between the last three photos was equal to or less than 2 second.
        if (lastphoto[3] != -1 and (lastphoto[0] - lastphoto[1] - lastphoto[2] - lastphoto[3]) / 4 <= 2) :
            print("Abnormal amount of photos taken within a couple second. Please update Threshold or check on SAT")
        

def main():
    take_photo()


if __name__ == '__main__':
    main()
