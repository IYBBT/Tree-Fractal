
import pygame as pygame
import math as math
import random as random

scale = 6

class Line:
    def __init__(self, depth=0, length=300, angle=math.pi/2):
        self.length = length
        self.angle = angle
        self.depth = depth
    
    def draw(self, window, startPos):
        global scale
        endPos = (startPos[0] - math.cos(self.angle) * self.length, 
                  startPos[1] - math.sin(self.angle) * self.length)
        
        color = (200, 100, 0) if self.depth > 0 else (0, 200, 0)
        pygame.draw.line(window, color, startPos, endPos)
        pygame.display.flip()
        
        if self.depth > 0:
            dl = (math.pi / scale)
            left = Line(self.depth-1, self.length * 0.75, self.angle - dl)
            left.draw(window, endPos)

            dr = (math.pi / scale)
            right = Line(self.depth-1, self.length * 0.75, self.angle + dr)
            right.draw(window, endPos)


if __name__ == '__main__':
    pygame.init()
    
    window = pygame.display.set_mode((2000, 1200))
    window.fill((20, 20, 20))
    
    root = Line(10)
    root.draw(window, (1000, 1200))
    print(scale)
    
    while True:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
