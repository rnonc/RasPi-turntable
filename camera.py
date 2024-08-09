from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO

camera = PiCamera()
camera.start_preview()
sleep(0.1)
camera.capture('/home/pi/Desktop/image.png')
camera.stop_preview()