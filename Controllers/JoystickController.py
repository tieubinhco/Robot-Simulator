import pygame

class JoystickController:
    def __init__(self):
        self.left = 0
        self.right = 0
        return

    def update(self):
        self.left = 0
        self.right = 0
        events = pygame.event.get()
        keys=pygame.key.get_pressed()


        if keys[pygame.K_LEFT]:
            self.left += -1.0
            self.right += 1.0
        if keys[pygame.K_RIGHT]:
            self.left += 1.0
            self.right += -1.0
        if keys[pygame.K_UP]:
            self.left += 1.0
            self.right += 1.0
        if keys[pygame.K_DOWN]:
            self.left += -1.0
            self.right += -1.0

        b = max(self.left, self.right)
        if b > 1.0:
            self.left *= 1.0/b
            self.right *= 1.0/b


        return [self.left, self.right]