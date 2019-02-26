import pygame

class JoystickController:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        return

    def setSpeed(self, left, right):
        self.left = left
        self.right = right

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = -1.0
                    self.right = -1.0
                if event.key == pygame.K_RIGHT:
                    self.left = 1.0
                    self.right = 1.0
        return [self.left, self.right]