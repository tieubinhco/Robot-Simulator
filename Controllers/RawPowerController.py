

class RawPowerController:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        return

    def setSpeed(self, left, right):
        self.left = left
        self.right = right

    def update(self):
        return [self.left, self.right]