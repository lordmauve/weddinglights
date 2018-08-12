from lights.colors import BLACK
import struct
from socketserver import ThreadingTCPServer, StreamRequestHandler
from threading import Thread


pixels = [BLACK] * 8 * 64

TITLE = "Wedding lights simulator"
WIDTH = 15 * 50 + 20
HEIGHT = 20 * 8 + 20


MSG_HEADER = struct.Struct('>BBH')


class Handler(StreamRequestHandler):
    def handle(self):
        global pixels
        sock = self.request
        f = sock.makefile('rb')

        while True:
            hdr = f.read(MSG_HEADER.size)
            if not hdr:
                break
            channel, command, length = MSG_HEADER.unpack(hdr)
            data = f.read(length)
            if command == 0:
                newpixels = []
                for off in range(0, len(data), 3):
                    newpixels.append(tuple(data[off:off + 3]))
                pixels = newpixels
            elif command == 2:
                print("Unsupported command %d" % command)

def serve():
    s = ThreadingTCPServer(('0.0.0.0', 7890), Handler)
    s.daemon_threads = True
    s.serve_forever()


Thread(target=serve, daemon=True).start()


def draw():
    screen.clear()
    for i, p in enumerate(pixels):
        y, x = divmod(i, 64)
        if x >= 50:
            continue
        r, g, b = p
        intensity = max(p)

        cx = x * 15 + 20
        cy = y * 20 + 20
        screen.draw.filled_circle(
            pos=(cx, cy),
            radius=4,
            color=p
        )
        l = 10 * (intensity / 255) ** 2
        screen.draw.line(
            start=(cx - l, cy - l),
            end=(cx + l, cy + l),
            color=p
        )
        screen.draw.line(
            start=(cx - l, cy + l),
            end=(cx + l, cy - l),
            color=p
        )



def update():
    pass

