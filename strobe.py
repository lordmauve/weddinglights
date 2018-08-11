from lights import Grid, WHITE, BLACK


g = Grid(interp=False)


for i in g.fps(10):
    g.fill(WHITE if i % 2 else BLACK)
