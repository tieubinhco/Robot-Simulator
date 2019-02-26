import pygame

class Trail:
    def __init__(self, thickness=1, size=400, color=(0,255,255)):
        self.trail = []
        self.enabled = True
        self.size = size
        self.color = color
        self.thickness = thickness

    def drawTrail(self, screen):
        if (self.enabled):
            for p in range(min(len(self.trail), self.size)):
                pygame.draw.circle(screen, self.color, self.trail[len(self.trail) - p - 1], self.thickness, 0)