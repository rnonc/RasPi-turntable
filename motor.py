import time
import RPi.GPIO as GPIO

allTypeMotor = ["default","bound"]

"""
StepperMotor : digital twin of a stepper motor
    StepPins : pins link to the motor
    nbStepMax : number of steps before a revolution
    typeMotor : -"default" accept revolution -"bound" not accept revolution
"""
class StepperMotor:
    def __init__(self,StepPins,nbStepsMax,typeMotor = "default"):
        self.seq = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.mod = 0
        self.stepPins = StepPins
        self.nbStepsMax =nbStepsMax
        self.stepCount = 4
        self.state = 0
        self.step = 0
        self.time = 0
        self.command = 0
        self.set = True
        self.waitTime = 0.005
        if(typeMotor in allTypeMotor):
            self.typeMotor = typeMotor
        else:
            self.typeMotor = allTypeMotor[0]
            print("this type doesn't exist, 'default' is attributed")
        for pin in StepPins:
            print("Setup pin {}".format(pin))
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
    # Turns off the motor
    def off(self):
        for xpin in self.stepPins:
            GPIO.output(xpin, False)
    # Activates the motor
    def active(self):
        for pin in range(4):
            xpin = self.stepPins[pin]
            if self.seq[self.state][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        self.time = time.time()
    # Sets a command
    def changeCommand(self,command):
        self.command = command
        self.set = False
    # Changes mode
    def changeMod(self):
        if(self.mod == 0):
            self.seq = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
            self.stepCount = 8
            self.mod = 1
            self.nbStepsMax *= 2
            self.step *= 2
            self.state = self.state*2
            self.waitTime /= 2
            print("half-step set!")
        elif(self.mod == 1):
            self.seq = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
            self.stepCount = 4
            self.mod = 0
            self.nbStepsMax = self.nbStepsMax //2
            self.step = self.step //2
            self.state = self.state //2
            self.waitTime *= 2
            print("classic step set!")
    # Go to the next step
    def nextStep(self,direction = "up",show = True):
        if(time.time()-self.time < self.waitTime):
            return
        if(direction in["down","d",-1]):
            sign = -1
        else:
            sign = 1
        if(self.step + sign == self.nbStepsMax):
            if(self.typeMotor == "default"):
                self.step = 0
                self.state = (self.state + sign)%self.stepCount
                self.active()
            elif(self.typeMotor == "bound"):
                self.step +=sign
                self.state = (self.state + sign)%self.stepCount
                self.active()
        elif(self.typeMotor == "bound" and self.step + sign == self.nbStepsMax +1):
            print("Motor is on maximum")
            self.command = self.nbStepsMax
        elif(self.step + sign == -1):
            if(self.typeMotor == "default"):
                self.step = self.nbStepsMax -1
                self.state = (self.state + sign)%self.stepCount
                self.active()
            elif(self.typeMotor == "bound"):
                print("Step is on minimum")
                self.command = 0
        else:
            self.step += sign
            self.state = (self.state + sign)%self.stepCount
            self.active()
        if(show):
            print(self.step)
    # Serves the motor
    def aserv(self,show = False):
        if(self.typeMotor == "default"):
            self.command = self.command % self.nbStepsMax
            T = self.command - self.step
            if(T>0):
                if(T> self.nbStepsMax //2):
                    self.nextStep("down",show)
                else:
                    self.nextStep("up",show)
            elif(T<0):
                if(T< -self.nbStepsMax//2):
                    self.nextStep("up",show)
                else:
                    self.nextStep("down",show)
            else:
                self.set = True
                return True
        elif(self.typeMotor == "bound"):
            T = self.command - self.step
            if(T>0):
                self.nextStep("up",show)
            elif(T<0):
                self.nextStep("down",show)
            else:
                self.set = True
                return True
        self.set = False
        return False
    # Checks if the servoing is good
    def testAserv(self,command = None):
        if(command != None):
            self.command = command
        a = False
        while(not(a)):
            a = self.aserv()
