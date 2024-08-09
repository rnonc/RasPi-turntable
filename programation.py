import threading

"""
Prog : program of motors and the camera (set of the instruction orders)
    - ListMotor : list of motors
    - ListStep : list of orders
    - camera : if order for camera is set
"""
class Prog:
    def __init__(self,ListMoteur,ListStep,camera = False):
        self.ListMoteur = ListMoteur
        self.camera = camera
        self.ListStep = ListStep
        self.nbMoteur = len(self.ListMoteur)
    # verifies states
    def checkStep(self):
        cond = True
        for indexMoteur in range(self.nbMoteur):
            cond = cond * ((self.ListMoteur[indexMoteur].nbStepsMax % self.ListStep[indexMoteur]) == 0)
        return cond
    # verifies servoing
    def allAserv(self):
        A = False
        while(not(A)):
            A = True
            for j in range(self.nbMoteur):
                x = threading.Thread(target= self.ListMoteur[j].aserv)
                x.start()
                A *= self.ListMoteur[j].set

    # Resets motors
    def reset(self):
        for j in range(self.nbMoteur):
            self.ListMoteur[j].changeCommand(0)
        self.allAserv()
    # Starts the orders
    def start(self):
        if(not(self.checkStep())):
            print("ListStep n'est pas adapté")
            return
        R = [0 for i in range(self.nbMoteur)]
        index = []
        for i in range(self.nbMoteur):
            a = self.ListMoteur[i].nbStepsMax // self.ListStep[i]
            if(self.ListMoteur[i].typeMotor == "bound"):
                a += 1
            index += [a]
        cond  = True
        for j in range(self.nbMoteur):
            self.ListMoteur[j].active()
        self.reset()
        while(cond):
            print(R)
            
            for j in range(self.nbMoteur):
                self.ListMoteur[j].changeCommand(R[j]* self.ListStep[j])
            
            self.allAserv()
            
            R[0] += 1
            for i in range(1,self.nbMoteur):
                if(R[i-1] == index[i-1]):
                    R[i] += 1
                    R[i-1] = 0
            if(R[-1] == index[-1]):
                cond = False
        self.reset()
        print("End of prog!!")
        
                