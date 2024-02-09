from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

picam2.configure(picam2.create_still_configuration())

picam2.start()

picam2.capture_file("test.jpg")

picam2.stop()