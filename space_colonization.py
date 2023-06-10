
import pygame as pygame
import math as math
import random as random
import time
from copy import deepcopy

width, height = 500, 500
maxDist, minDist = 50, 10

class Leaf:
    def __init__(self):
        self.pos = (random.randrange(width), random.randrange(height-100))
        self.reached = False

    def show(self, window):
        pygame.draw.circle(window, (0, 200, 0), (self.pos[0], self.pos[1]), 1)


class Branch:
    def __init__(self, parent, pos, dir):
        self.parent = parent
        self.pos = pos
        self.dir = dir
        self.count = 0
        self.origDir = deepcopy(dir)

    def reset(self):
        self.dir = deepcopy(self.origDir)
        self.count = 0

    def next(self):
        nextPos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        nextBranch = Branch(self, nextPos, deepcopy(self.dir))
        return nextBranch
    
    def show(self, window):
        if self.parent is not None:
            color = (200, 100, 0)
            pygame.draw.line(window, color, self.pos, self.parent.pos)
            

class Tree:
    def __init__(self):
        self.leaves = []
                
        for i in range(500):
            self.leaves.append(Leaf())
            
        root = Branch(None, (width/2, height), (0, -1))
        self.branches = [root]
        
        found = False
        current = root
        while not found:
            for i in range(len(self.leaves)):
                d = math.dist(current.pos, self.leaves[i].pos)
                if (d < maxDist):
                    found = True
            
            if not found:
                branch = current.next()
                current = branch
                self.branches.append(current)
                    
    def grow(self):
        for i in range(len(self.leaves)):
            leaf = self.leaves[i]
            record = 100000
            closestBranch = None
            for j in range(len(self.branches)):
                branch = self.branches[j]
                d = math.dist(leaf.pos, branch.pos)
                if d < minDist:
                    leaf.reached = True
                    closestBranch = None
                    break
                elif d > maxDist:
                    pass
                elif closestBranch is None or d < record:
                    closestBranch = branch
                    record = d
                    
            if closestBranch is not None:
                dir = (leaf.pos[0] - closestBranch.pos[0], leaf.pos[1] - closestBranch.pos[1])
                m = math.sqrt(dir[0]*dir[0] + dir[1]*dir[1]) / 5
                dir = (dir[0] / m, dir[1] / m)
                closestBranch.pos = (closestBranch.pos[0] + dir[0], closestBranch.pos[1] + dir[1])
                closestBranch.count += 1
            
        i = len(self.leaves)    
        while i > 0:
            i -= 1
            if self.leaves[i].reached:
                self.leaves.pop(i)
                i -= 1
                
        i = len(self.branches)
        while i > 0:
            i -= 1
            branch = self.branches[i]
            if branch.count > 0:
                branch.dir = (branch.dir[0] / branch.count, branch.dir[1] / branch.count)
                self.branches.append(branch.next())
            branch.reset()
                    
    def show(self, window):
        for i in range(len(self.leaves)):
            self.leaves[i].show(window)
            
        for i in range(len(self.branches)):
            self.branches[i].show(window)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((width, height))
    window.fill((20, 20, 20))
    
    tree = Tree()
    while True:
        window.fill((20, 20, 20))
        tree.grow()
        tree.show(window)
        pygame.display.update()
        time.sleep(0.04)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
