'''
TODO:
    - allow multiwheel/non-static config
    - Implement first order motor equations for PWM voltage+battery -> torque output
    - Torque/voltage proportional battery decay
'''
#https://www.chiefdelphi.com/t/paper-practical-guide-to-state-space-control/166417

import math 
class IdealRobot:
    def __init__(self, x, y, head):
        #Instantaeous Robot Properties 
        self.x = x
        self.y = y
        self.head = head
        
    def update(self, deltaT, veloL, veloR):

        self.head += (omega + self.prevOmega)/2 * deltaT
        #integrate velocity for position, break up into vertical and horizontal comp
        self.x += ((velo+self.prevVelo)/2 * deltaT) * math.cos(self.head)
        self.y += ((velo+self.prevVelo)/2 * deltaT) * math.sin(self.head)

    def getTelemetry(self):
        return 
        #return [self.]
    def getPos(self):
        return [self.x, self.y, self.head]

#s = Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0)
#for i in range(0, 250):
#    s.update(0.01, 1.0, 1.0, 1.0)
#print(s.getPos())
