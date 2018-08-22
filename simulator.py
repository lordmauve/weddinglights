import os
from lights.colors import BLACK
import struct
import pygame.image
from pygame import Surface
from socketserver import ThreadingTCPServer, StreamRequestHandler
from threading import Thread


STRIDEX = 15
PIXELSH = 8


if os.environ.get('MODE') == 'hat':
    PIXELSW = 8
    PORT = 7891
    STRIDEY = 15
else:
    PIXELSW = 50
    PORT = 7890
    STRIDEY = 30



pixels = [BLACK] * 8 * 64

TITLE = "Wedding lights simulator"
WIDTH = 15 * (PIXELSW - 1) + 40
HEIGHT = STRIDEY * (PIXELSH - 1) + 40


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
    s = ThreadingTCPServer(('0.0.0.0', PORT), Handler)
    s.daemon_threads = True
    s.serve_forever()


Thread(target=serve, daemon=True).start()

lastpixels = pixels

def draw():
    global lastpixels

    if pixels is lastpixels:
        return

    lastpixels = pixels
    screen.clear()
    for i, p in enumerate(pixels):
        y, x = divmod(i, 64)
        if x >= PIXELSW:
            continue
        y = PIXELSH - y - 1
        r, g, b = p
        intensity = max(p)

        x = PIXELSW - x - 1
        cx = x * STRIDEX + 20
        cy = y * STRIDEY + 20
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


def on_key_down(key):
    if key == keys.F12:
        s = Surface((PIXELSW, PIXELSH), depth=24)
        for i, p in enumerate(pixels):
            y, x = divmod(i, 64)
            if x >= PIXELSW:
                continue
            y = PIXELSH - y - 1
            x = PIXELSW - x - 1
            s.set_at((x, y), p)
        pygame.image.save(s, 'grab.png')




import pygame
pygame.mixer.quit()
