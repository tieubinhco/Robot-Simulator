'''
    TODO:
    -Allow multi-robot support
    -Allow better simulation
'''


import threading
import robot
import idealrobot
import time
import graphics

#start world thread, control thread, and graphics thread 
class Simulation:
    #give world,control,and graphics frequencies in hertz, give simulation rate multiple
    #allow max on world frequency to use CPU inhibited speed
    def __init__(self, worldFreq, controlFreq, graphicsFreq, simRate, robots, controllers):
        self.worldFreq = worldFreq
        if(self.worldFreq != 'max'):
            self.worldFreq = (1.0/worldFreq)
        else:
            self.worldFreq = 0.0
        self.controlFreq = 1.0/controlFreq
        self.graphicsFreq = 1.0/graphicsFreq
        self.simRate = simRate

        self.deltaT = 0
        self.prevT = time.time()
        self.robots = robots
        self.controllers = controllers

        self.speeds = []
        for i in robots:
            self.speeds.append((0, 0))
        
        self.world = threading.Thread(target=self.worldThread)
        self.graphics = threading.Thread(target=self.graphicsThread)
        self.control = threading.Thread(target=self.controlThread)
        self.world.start()
        self.graphics.start()
        self.control.start()

    def worldThread(self):
        self.start = time.time()
        cnt = 12 
        while(1):
            t = time.time()
            for i in range(len(self.robots)):
                self.robots[i].update((t - self.prevT)*self.simRate, 1.0, self.speeds[i][0], self.speeds[i][1])
            time.sleep(float(self.worldFreq)/float(self.simRate))
            print(str(cnt) + " | " + str((time.time()-self.start)*self.simRate) + " | " + str(self.robots[0].getPos()[2]))
            cnt+=1
            self.prevT = t
    def controlThread(self):
        while(1):
            self.speeds[0] = (0.5, 0.9)
            self.speeds[1] = (0.5, 0.9)
            time.sleep(self.controlFreq/self.simRate)
    def graphicsThread(self):
        window = graphics.Graphics((400,400), (2,2), self.robots)
        while(1):
            #print("hi")
            window.updateGraphics()
            time.sleep(self.graphicsFreq/self.simRate)
        return

# battery1 = battery.Battery(1.0, 's') paramterize robot with a battery
robot1 = robot.Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0)
robot2 = idealrobot.IdealRobot(0, 0, 0, 0.2286)
#controller1 = pid.PID()
s = Simulation(100, 40, 30, 1.0, [robot1, robot2], [])
