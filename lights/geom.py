import math


class Block:
    def __init__(self, grid, x, y, w, h):
        self.grid = grid
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def keys(self):
        for j in range(self.y, self.y + self.h):
            for i in range(self.x, self.x + self.w):
                yield i, j

    def set(self, color):
        for pos in self.keys():
            self.grid[pos] = color


class Spotlight(Block):
    def set(self, color):
        cx = self.x + 0.5 * self.w
        cy = self.y + 0.5 * self.h
        for x, y in super().keys():
            dx = (x - cx) / (self.w / 2)
            dy = (y - cy) / (self.h / 2)

            dist = math.sqrt(dx * dx + dy * dy)
            frac = max(0, 1.0 - dist * dist * dist)
            self.grid[x, y] = tuple(c * frac for c in color)
