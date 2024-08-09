# libraries
# test VNC
import time
import RPi.GPIO as GPIO
from motor import StepperMotor
from programation import Prog
# Use BCM GPIO references
# Instead of physical pin numbers

GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use Pins 18,22,24,26 GPIO24,GPIO25,GPIO8,GPIO7
StepPins = [24,25,8,7]
StepPins2 = [17,27,22,10]
CaptPin = 19
GPIO.setup(CaptPin,GPIO.IN)
a = GPIO.input(CaptPin)

M1= StepperMotor(StepPins,2048);
M2 = StepperMotor(StepPins2,1024,"bound")
#M2 = MoteurPAPV(2048);

p = Prog([M1,M2],[16,256]);
#p.start()
#M1.steps(2048);
M1.off()
M2.off()

#GPIO.cleanup()