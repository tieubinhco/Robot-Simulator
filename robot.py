#TODO: allow multiwheel, wheel spacing, OR non-static wheels, also allow better motor PWM voltage+battery -> torque output calcm 

class Robot:
    def __init__(self, x, y, head, battery, uk, us, spdpwr_coef, length, width, mass, wheelRadius, motorStallTorque, motorMaxRPM, motorGearing, maxV, maxA, maxJ, kR):
        #Instantaeous Robot Properties 
        self.x = x
        self.y = y
        self.veloL = 0
        self.accelL = 0
        self.veloR = 0
        self.accelR = 0
        self.head = head
        self.battery = battery
        
        #Static Robot Characteristics 
        self.uk = uk
        self.us = us
        self.spdpwr_coef = spdpwr_coef #translate an applied motor power to speed
        self.length = length
        self.width = width
        self.mass = mass
        self.wheelRadius = wheelRadius
        self.motorStallTorque = motorStallTorque
        self.motorMaxRPM = motorMaxRPM
        self.motorGearing = motorGearing
        self.maxV = maxV
        self.maxA = maxA
        self.maxJ = maxJ
        self.kR = kR #coeficient of randomness in applied speed/velo and friction
        
        #rate limiters
        self.prevVeloL = 0
        self.prevVeloR = 0
        self.prevAccelL = 0
        self.prevAccelR = 0
        
        
    def update(deltaT, battery, speedL, speedR):
         #update head based on new speeds and deltaT
         #update velo and accel based on new speeds, make sure they stay within powered rate limits, otherwise limit and increase randomness to stimulate jolt, if downward change not within powered rate change, switch to decay rates by inertia
         #update x and y based on new heading and velo and deltaT
         #multiply in battery percentage to dampen spdpwr_coef
         head = 
         y += velo
    
       
        

    #what the fuk is the relationship between the velo of two wheels, deltaT and the turn rate [see discord]





#http://forum.arduino.cc/index.php?topic=289568.0

