'''
TODO:
    - allow multiwheel/non-static config
    - Implement first order motor equations for PWM voltage+battery -> torque output
    - Torque/voltage proportional battery decay
'''

import math 
class Robot:
    def __init__(self, x, y, head, battery, uk, width, mass, wheelRadius, motorStallTorque, motorMaxRPM, motorGearing, maxV, maxA, maxJ):
        #Instantaeous Robot Properties 
        self.x = x
        self.y = y
        self.head = head
    
        self.veloL = 0
        self.veloR = 0

        self.rpmL = 0
        self.rpmR = 0
    
        self.accel = 0
        self.velo = 0
        self.battery = battery
        
        #Static Robot Characteristics 
        self.uk = uk
        self.width = width
        self.mass = mass
        self.wheelRadius = wheelRadius
        self.Tstall = motorStallTorque
        self.maxRPM = motorMaxRPM
        self.motorGearing = motorGearing
        self.maxV = maxV
        self.maxA = maxA
        self.maxJ = maxJ
        self.MOI = mass * (width ** 2)
        
        #rate limiters
        self.prevVelo = 0
        self.prevOmega = 0
        
        
    def update(self, deltaT, battery, speedL, speedR):
        #Calculate instant motor output torque based on the RPM/Torque curve and applied power
        torqueL = (-self.Tstall/self.maxRPM * abs(self.rpmL) + self.Tstall) * abs(speedL) * battery
        torqueR = (-self.Tstall/self.maxRPM * abs(self.rpmR) + self.Tstall) * abs(speedR) * battery

        #Preserve signs
        lSign = 1
        rSign = 1
        if(speedL != 0):
            lSign = (abs(speedL)/speedL)
        if(speedR != 0):
            rSign = (abs(speedR)/speedR)

        #Compute tangential force vectors, net force by subtracting inline friction forces, max friction
        forceFrictionL = self.uk * self.mass * 9.81
        forceFrictionR = self.uk * self.mass * 9.81

        if(torqueL > 0): #check if velo is zero crossing,
            forceFrictionL = min(forceFrictionL, torqueL/self.wheelRadius)
        if(torqueR > 0):
            forceFrictionR = min(forceFrictionL, torqueR/self.wheelRadius)

        forceL = (torqueL/self.wheelRadius - self.uk * self.mass * 9.81)* lSign #maintain signs
        forceR = (torqueR/self.wheelRadius - self.uk * self.mass * 9.81)* rSign #problem, in static case, robot goes backward

        #Integrate net acceleration for tangential velocities 
        self.veloL += forceL/self.mass * deltaT
        self.veloR += forceR/self.mass * deltaT

        #forward force is the average of the two motor forces
        f_fwd = (forceL + forceR)/2
        #torque is created by the differential between the forces multiplied by radius 
        torque = (forceR - forceL) * self.width/2

        #integrate angular acceleration, calculated from Torque over MOI for velocity
        omega = self.prevOmega+(torque/self.MOI) * deltaT
        accel = f_fwd/self.mass
        #integrate acceleration for velocity
        velo = self.prevVelo + accel * deltaT
        #integrade angular velocity for theta
        self.head += (omega + self.prevOmega)/2 * deltaT
        #integrate velocity for position, break up into vertical and horizontal comp
        self.x += ((velo+self.prevVelo)/2 * deltaT) * math.cos(self.head)
        self.y += ((velo+self.prevVelo)/2 * deltaT) * math.sin(self.head)

        #rate limiters
        self.prevOmega = omega
        self.prevVelo = velo
        #janky RPM calculation, this is probably wrong
        self.rpmL = self.veloL/self.wheelRadius * (60/(2*math.pi))
        self.rpmR = self.veloR/self.wheelRadius * (60/(2*math.pi))
        print(str(torqueL) + " " + str(torqueR))

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
