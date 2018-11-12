#1D 1 wheel
while(True):
    Power = 0.7 #user program speed from -1.0 to 1.0
    Battery = 0.98
    T = (-Tstall/RPMmax * rpm + Tstall) * Power * Battery
    F = T/radius - coef_kinetic * mass * 9.81
    accel = F/mass 
    velocity += accel * deltaT

    pos += (velocity+vprev)/2 * deltaT  #end goal in the 1D case

    rpm = velocity/r  #times some conversion factor for radians per sec to rev per minute
    vprev = velocity


	
#1D 2 wheel, to add heading just add approrite sin(heading) cos(heading) for x y 
while(True):
	#per wheel 
    Power = 0.7 #user program speed from -1.0 to 1.0
    Battery = 0.98
    T = (-Tstall/RPMmax * rpm + Tstall) * Power * Battery
    F = T/radius - coef_kinetic * mass * 9.81
	
	F = 2*F #since there are two motors/wheels, both the force from motors AND frictional force double
    
	#total robot accel/velo scalars and position
	accel = F/mass 
    velocity += accel * deltaT
    pos += (velocity+vprev)/2 * deltaT  #end goal in the 1D case
	vprev = velocity
	
	#per motor
    rpm = (velocity/r) * 1/2  #times some conversion factor for radians per sec to rev per minute
    

#2D 2 wheel
Battery = 0.98
PowerL = 0.7 
PowerR = 1.0 
Distance = 0.4#distance between center of robot and wheel side in m
x = 0 
y = 0 
theta = 0
while(True):
	#left wheel
    Tl = (-Tstall/RPMmax * rpmL + Tstall) * PowerL * Battery
    Fl = T/radius - coef_kinetic * mass * 9.81
	#right wheel 
	Tr = (-Tstall/RPMmax * rpmR + Tstall) * PowerR * Battery
    Fr = T/radius - coef_kinetic * mass * 9.81
	
	#forward force as average between two motor forces and torque from the force differential 
	F_fwd = (Fl + Fr)/2 
	T_total = (Fl-Fr) * d 
	MOI = mass * Distance**2 #really crappy MOI calc
	
	#calculate accelerations and velocities
	omega += (T_total/MOI)*deltaT #integrate angular accel for angular velo
	
	accel = F_fwd/mass 
    velocity += accel * deltaT
	
	theta += (omega+omegaPrev)/2 * deltaT
    x += ((velocity+vprev)/2 * deltaT) * cos(theta)
	y += ((velocity+vprev)/2 * deltaT) * sin(theta)
	
	vprev = velocity
	omegaprev = omega
	
	#calculate the actual rpms of the motors 
    rpm = (velocity/r) * 1/2  #times some conversion factor for radians per sec to rev per minute
    