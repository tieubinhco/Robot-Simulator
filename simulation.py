'''
    TODO:
    -Locks/thread synchronization
    -More realistic robot model
    -Make a Path/Traj class and use in Pure Persuit
'''


import threading
import robot
import idealrobot
import time
import graphics
import plot
import Controllers.RawPowerController
import Controllers.JoystickController
import numpy as np
import Controllers.PurePersuitController
import sys
from PyQt5.QtWidgets import QApplication

# start world thread, control thread, and graphics thread


class Simulation:
    # give world,control,and graphics frequencies in hertz, give simulation rate multiple
    # allow max on world frequency to use CPU inhibited speed
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
        self.plot = threading.Thread(target=self.plotThread)
        self.world.start()
        self.graphics.start()
        self.control.start()
        self.plot.start()

        self.window = None

    def worldThread(self):
        self.start = time.time()
        cnt = 0
        while(1):
            t = time.time()
            for i in range(len(self.robots)):
                self.robots[i].update(
                    (t - self.prevT)*self.simRate, 1.0, self.speeds[i][0], self.speeds[i][1])
            time.sleep(float(self.worldFreq)/float(self.simRate))
            #print(str(cnt) + " | " + str((time.time()-self.start)*self.simRate) + " | " + str(self.robots[0].getPos()[1]))
            cnt += 1
            self.prevT = t

    def controlThread(self):
        while(1):
            for i in range(len(self.robots)):
                command = self.controllers[i].update(self.robots[i].getPos())
                self.speeds[i] = command

            time.sleep(self.controlFreq/self.simRate)

    def graphicsThread(self):
        self.window = graphics.Graphics(
            (1000, 1000), (10, 10), self.robots, self.controllers)
        while(1):
            self.window.updateGraphics()
            time.sleep(self.graphicsFreq/self.simRate)
        return

    def plotThread(self):
        # print("1")
        plot1 = plot.Plot("x v y", "x", "y", np.empty(0), np.empty(0))
        while(1):
            #plot1.addData(time.time(), self.robots[0].getPos()[0])
            plot1.addData(self.robots[0].getPos()[0],
                          self.robots[0].getPos()[1])
            plot1.plot()
            time.sleep(0.01)


# DO stuff thats sketch
# battery1 = battery.Battery(1.0, 's') paramterize robot with a battery
'''
robot1 = robot.Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0)
robot2 = idealrobot.IdealRobot(0, 0, 0, 0.2286)
robot3 = idealrobot.IdealRobot(-0.5, 0, 0, 0.2286)

controller1 = Controllers.RawPowerController.RawPowerController(0.0, 0.0)
controller2 = Controllers.JoystickController.JoystickController()
s = Simulation(100, 40, 30, 1.0, [robot2, robot3], [controller2, controller2])
time.sleep(1)
s.window.trails[0].color = (255, 0, 0)
'''
if __name__=="__main__":
    #robot1 = robot.Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0)
    # app=QApplication(sys.argv)
    robot1 = idealrobot.IdealRobot(0, 0, 0, 0.2286)
    purePersuit = Controllers.PurePersuitController.PurePersuitController(
        0.75, robot1.width)
    purePersuit.addPoint(0, 0)
    purePersuit.addPoint(3, 4)


    #purePersuit.addPoint(0, 20)
    print(str(purePersuit.getLookAheadPoint(
        Controllers.PurePersuitController.Point(0, 2))))
    s = Simulation(100, 40, 30, 1.0, [robot1], [purePersuit])
    time.sleep(1)

    # sys.exit(app.exec_())
    # s.window.addDebugger(purePersuit.visualDebug)
