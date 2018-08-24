import math


class Block:
    def __init__(self, grid, x, y, w, h):
        self.grid = grid
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def keys(self):
        for j in range(max(self.y, 0), min(self.y + self.h, self.grid.H)):
            for i in range(max(self.x, 0), min(self.x + self.w, self.grid.W)):
                yield i, j

    def items(self):
        for k in self.keys():
            yield k, self.grid[k]

    def set(self, color):
        for pos in self.keys():
            self.grid[pos] = color


class Spotlight(Block):
    intensity = 1

    def set(self, color):
        hw = self.w * 0.5
        hh = self.h * 0.5
        cx = self.x + hw - 0.5
        cy = self.y + hh - 0.5
        for (x, y), prev in super().items():
            dx = (x - cx) / hw
            dy = (y - cy) / hh

            dist = math.sqrt(dx * dx + dy * dy) / self.intensity
            frac = max(0, 1.0 - dist * dist * dist)

            self.grid[x, y] = tuple(min(255, p + c * frac) for p, c in zip(prev, color))
