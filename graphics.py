import pygame
class Graphics: #graph trail, hold trail buffer array
    def __init__(self, robots):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        
        self.sprite = pygame.Surface((50, 100))
        self.sprite.fill((255,0,0))
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (100, 100)

        #self.sprite, self.rect = self.rot_center(self.sprite, self.rect, 30)
        self.angle = 0
        #self.angle+=0.01
        
    def translateCoord(self, x, y):
        return
    
    def rot_center(self, image, rect, angle): #Taken from pygame library
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
    
    def updateGraphics(self):
        pygame.event.get()
        self.screen.fill((0,0,0))  

        self.sprite2, self.rect2 = self.rot_center(self.sprite, self.rect, self.angle)
        self.angle+= 1
        self.screen.blit(self.sprite2, self.rect2)
        pygame.display.flip()
        return
