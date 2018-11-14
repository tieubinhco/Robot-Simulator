'''
TODO:
    - allow multiwheel/non-static config
    - Implement first order motor equations for PWM voltage+battery -> torque output
    - Torque/voltage proportional battery decay
'''
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
        torqueL = (-Tstall/maxRPM * rpmL + Tstall) * speedL * battery
        torqueR = (-Tstall/maxRPM * rpmR + Tstall) * speedR * battery

        #Compute tangential force vectors, net force by subtracting inline friction forces
        forceL = torqueL/wheelRadius - uk * mass * 9.81
        forceR = torqueR/wheelRadius - uk * mass * 9.81

        #Integrate net acceleration for tangential velocities 
        veloL += forceL/mass * deltaT
        veloR += forceR/mass * deltaT

        #forward force is the average of the two motor forces
        f_fwd = (forceL + forceR)/2
        #torque is created by the differential between the forces multiplied by radius 
        torque = (forceR - forceL) * width

        #integrate angular acceleration, calculated from Torque over MOI for velocity
        omega += (torque/MOI) * deltaT
        accel= f_fwd/mass
        #integrate acceleration for velocity
        velo += accel * deltaT
        #integrade angular velocity for theta
        theta += (omega + prevOmega)/2 * deltaT
        #integrate velocity for position, break up into vertical and horizontal comp
        x += ((velocity+prevVeloL)/2 * deltaT) * math.cos(theta)
        y += ((velocity+prevVeloR)/2 * deltaT) * math.sin(theta)

        #rate limiters
        prevOmega = omega
        prevVelo = velo
        #janky RPM calculation, this is probably wrong
        rpmL = veloL/wheelRadius * (60/(2*math.pi))
        rpmR = veloR/wheelRadius * (60/(2*math.pi))
        
    def getPos():
        return [self.x, self.y, self.head]
       

s = Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0)
s.update(0.1, 1.00, 1.0, 1.0)
print(s.getPos())
