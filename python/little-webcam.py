#!/usr/bin/env python

import sys
import socket
import time
import picamera

try:
    with picamera.PiCamera() as camera:
        #camera.resolution = (640, 480)
        camera.resolution = (1024, 768)
        #camera.resolution = (2592, 1944)
        camera.framerate = 24
        camera.brightness = 60
        camera.vflip = True
        camera.hflip = True

        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('wb')
        try:
            camera.start_recording(connection, format='h264')
            camera.wait_recording(30)
            camera.stop_recording()

        except socket.error as e:
            print('Caught exception: {0}'.format(e))

        finally:
            print("Closing sockets.")
            connection.close()
            server_socket.close()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))

print("Bye bye")
