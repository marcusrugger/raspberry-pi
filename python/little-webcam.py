#!/usr/bin/env python

import sys
import socket
import time
import picamera

def start_recording(camera, server_socket, connection):
    print("Start recording.")
    try:
        camera.start_recording(connection, format='h264')
        while True : camera.wait_recording(30)

    except socket.error as e:
        print('start_recording: Caught exception: {0}'.format(e))
        print('start_recording: Stop recording.')
        camera.stop_recording()

    finally:
        print("start_recording: finally")
        #print("Closing sockets.")
        #connection.close()
        #server_socket.close()


def wait_for_connection(camera):
    print("Configure socket.")
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    print("Wait for connection.")
    connection = server_socket.accept()[0].makefile('wb')

    start_recording(camera, server_socket, connection)



while True:
    try:
        print("Instantiate camera.")
        with picamera.PiCamera() as camera:
            print("Configure camera.")
            camera.resolution = (640, 480)
            #camera.resolution = (800, 600)
            #camera.resolution = (1024, 768)
            #camera.resolution = (2592, 1944)
            camera.framerate = 24
            camera.brightness = 60
            camera.vflip = True
            camera.hflip = True

            wait_for_connection(camera)

    except socket.error as e:
        print('Caught exception: {0}'.format(e))

    print('Sleep for two minutes.')
    time.sleep(120)

print("Bye bye")

