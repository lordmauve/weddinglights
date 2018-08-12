#!/usr/bin/env python

import struct
from SocketServer import ThreadingTCPServer, StreamRequestHandler
from threading import Thread

import unicornhat as unicorn


width = height = 8

def init():
    global width, height
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
    width, height=unicorn.get_shape()

MSG_HEADER = struct.Struct('>BBH')


class Handler(StreamRequestHandler):
    def handle(self):
        sock = self.request
        f = sock.makefile('rb')

        while True:
            hdr = f.read(MSG_HEADER.size)
            if not hdr:
                break
            channel, command, length = MSG_HEADER.unpack(hdr)
            data = f.read(length)
            if command == 0:
                for off in range(0, len(data), 3):
                    y, x = divmod(off // 3, 64)	
                    if y > height or x > width:
                        continue
                    color = tuple(ord(c) for c in data[off:off + 3])
                    unicorn.set_pixel(y, 8 - x, color)
                unicorn.show()
            elif command == 2:
                print("Unsupported command %d" % command)


init()
s = ThreadingTCPServer(('0.0.0.0', 7891), Handler)
s.daemon_threads = True
s.serve_forever()
