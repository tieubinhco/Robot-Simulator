'''
    TODO:
    -paramterize screen background and robot colors, allow image inputs
    - draw robot trail, desired paths, and end points

'''

import pygame
import trail

class Graphics: #graph trail, hold trail buffer array, draw desired paths and end points
    def __init__(self, screenDimensions, worldDimensions, robots):
        #initialize graphics
        pygame.init()
        self.screen = pygame.display.set_mode(screenDimensions)

        #store reference dims
        self.worldDimensions = worldDimensions
        self.screenDimensions = screenDimensions
        self.robots = robots

        #trail data
        self.trails = []

        self.q = 0

        #initalize screen resources 
        self.robotSprites = []
        self.robotHitboxes = []
        c = 0
        for robot in self.robots: 
            self.robotSprites.append(pygame.Surface((self.translateDim(robot.getWidth(),0)[0], self.translateDim(0, robot.getWidth())[1])))
            #self.robotSprites[c].fill((255,0,0))
            #self.robotSprites[c].set_colorkey((0,0,0))
            self.robotHitboxes.append(self.robotSprites[c].get_rect())
            self.robotHitboxes[c].center = self.translateCoord(robot.getPos()[0], robot.getPos()[1])

            sprite = pygame.image.load("arrow.jpg")
            self.robotSprites[c] = pygame.transform.scale(sprite, self.robotHitboxes[c].size)
            self.robotSprites[c].convert()
            self.robotSprites[c].set_colorkey((0, 0, 0))

            self.trails.append(trail.Trail(1*worldDimensions[0]))

            c+=1
        

      
        
    def translateCoord(self, x, y):
        x = x * (self.screenDimensions[0]/self.worldDimensions[0]) + self.screenDimensions[0]/2
        y = -y * (self.screenDimensions[1]/self.worldDimensions[1]) + self.screenDimensions[1]/2
        #print(x)
        return (x, y)
    
    def translateDim(self, x, y):
        x = x * (self.screenDimensions[0]/self.worldDimensions[0])
        y = y * (self.screenDimensions[1]/self.worldDimensions[1])
        return (x, y)

    def rot_center(self, image, rect, angle): #Taken from pygame library
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

    # Draw a robot path for debugging path following
    def drawPath(self, path):
        return

    # Draw robot position history for debugging path following
    def enableTrail(self, robotIndex, trailEnabled, maxPoints):
        return


    def updateGraphics(self):
        pygame.event.get()
        self.screen.fill((0,0,0))  

        for i in range(len(self.robots)):
            sc, rc = self.rot_center(self.robotSprites[i],self.robotHitboxes[i], self.robots[i].getPos()[2] * 180.0/3.141592)
            rc.center = self.translateCoord(self.robots[i].getPos()[0], self.robots[i].getPos()[1])
            self.screen.blit(sc, rc)

            self.trails[i].trail.append(rc.center)
            self.trails[i].drawTrail(self.screen)


        pygame.display.flip()
        return

