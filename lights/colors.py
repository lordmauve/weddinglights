
RED = 255, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLACK = 0, 0, 0
YELLOW = 255, 255, 0
PURPLE = 200, 0, 200
BLUE = 0, 0, 255
CYAN = 0, 255, 255


def hsv(hue):
    hue %= 360
    h, i = divmod(hue, 60)
    p = 0
    q = 255 * (60 - i) // 60
    t = 255 * i // 60
    if h % 2 == 0:
        vs = [255, t, p]
    else:
        vs = [q, 255, p]
    for _ in range(int(h // 2)):
        vs.insert(0, vs.pop())
    return vs


def color_map():
    """Load a mapping of names to colors."""
    import pkgutil
    import io
    import csv
    mapping = {}
    color_data = pkgutil.get_data(__name__, 'data/colors.csv')
    f = io.StringIO(color_data.decode('utf8'))
    r = csv.reader(f)
    for row in r:
        name = row[0]
        val = tuple(int(c) for c in row[-3:])
        mapping[name] = val
    return mapping
