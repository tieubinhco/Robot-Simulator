import time

class SpeedProfiler: #trapezoidal motion profile
    def __init__(self, maxVelo, maxAccel, distance):
        self.maxVelo = maxVelo
        self.maxAccel = maxAccel
        self.timeToAccel = maxVelo/maxAccel * 2
        self.timeForPath = distance/maxVelo + self.timeToAccel/2
        self.maxVeloTime = self.timeForPath - self.timeToAccel
        self.accelPercent = (self.timeToAccel/2)/self.timeForPath
        self.deccelPercent = self.timeForPath - self.accelPercent

    def update(self, percent):
        velocity = 0

        #trapezoid by parts
        if(percent <= self.accelPercent):
            velocity = self.maxVelo + self.maxAccel * (percent - self.accelPercent)
        elif(percent >= self.deccelPercent):
            velocity = self.maxVelo - self.maxAccel * (percent - self.deccelPercent)
        else:
            velocity = self.maxVelo

        return velocity