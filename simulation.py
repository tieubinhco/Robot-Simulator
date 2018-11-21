import threading
import robot
import time
#import graphics

#start world thread, control thread, and graphics thread 

class Simulation:
    #give world,control,and graphics frequencies in hertz, give simulation rate multiple
    #allow max on world frequency to use CPU inhibited speed
    def __init__(self, worldFreq, controlFreq, graphicsFreq, simRate, robots):
        self.worldFreq = worldFreq
        if(self.worldFreq != 'max'):
            self.worldFreq = (1.0/worldFreq)
        else:
            self.worldFreq = 0.0
        self.controlFreq = 1.0/controlFreq
        self.graphicsFreq = 1.0/graphicsFreq
        self.simRate = simRate

        self.deltaT = 0
        self.robots = robots
        
        world = threading.Thread(target=self.worldThread, args=())
        graphics = threading.Thread(target=self.worldThread, args=())
        control = threading.Thread(target=self.controlThread, args=())
        world.start()
        graphics.start()
        control.start()

        

        
    def worldThread(self):
        self.start = time.time()
        while(1):
            #print(self.worldFreq)
            self.robots[0].update(self.worldFreq, 1.0, 1.0, 1.0)
            time.sleep(float(self.worldFreq)/float(self.simRate))
            print(str(time.time()-self.start) +" | " +str(self.robots[0].getPos()[0]))
            #print()
    def controlThread(self):
        while(1):
            
            time.sleep(self.controlFreq/self.simRate)
    def graphicsThread(self):
        while(1):
            
            time.sleep(self.graphicsFreq/self.simRate)



s = Simulation(100, 40, 30, 1, [ robot.Robot(0, 0, 0, 1.00, 0.1, 0.2286, 6.8, 0.1016, 1.67, 100, 0.0, 0.0, 0.0, 0.0) ])
