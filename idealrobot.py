#https://www.chiefdelphi.com/t/paper-practical-guide-to-state-space-control/166417

import math 
class IdealRobot:
    def __init__(self, x, y, head, width):
        #Instantaeous Robot Properties 
        self.x = x
        self.y = y
        self.head = head
        self.width = width
        
    def update(self, deltaT, battery, veloL, veloR): #ignore battery
        omega = (veloR - veloL)/(2 * self.width)
        self.head += (omega * deltaT)
        #integrate velocity for position, break up into vertical and horizontal comp
        self.x += ((veloL + veloR)/2 * deltaT) * math.cos(self.head)
        self.y += ((veloL + veloR)/2 * deltaT) * math.sin(self.head)

    def getTelemetry(self):
        return 
        #return [self.]
    def getPos(self):
        return [self.x, self.y, self.head]

    def getWidth(self):
        return self.width
#s = Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0)
#for i in range(0, 250):
#    s.update(0.01, 1.0, 1.0, 1.0)
#print(s.getPos())
