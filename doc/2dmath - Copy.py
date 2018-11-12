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
