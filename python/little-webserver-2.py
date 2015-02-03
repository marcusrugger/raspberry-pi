#!/usr/bin/env python3

# This code is written by Stephen C Phillips.
# It is in the public domain, so you can do what you like with it
# but a link to http://scphillips.com would be nice.
 
import socket
import re
import sys
 
# Standard socket stuff:
host = '192.168.254.14'  # do we need socket.gethostname() ?
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)  # don't queue up any requests
 
# Loop forever, listening for requests:
try:
    while True:
        csock, caddr = sock.accept()
        print("Connection from: " + repr(caddr))
        req = csock.recv(1024)  # get the request, 1kB max
        print(req)
#         response = """\
# HTTP/1.0 200 OK
# Content-Type: text/html
 
# <html>
# <head>
# <title>Success</title>
# </head>
# <body>
# Boo!
# </body>
# </html>"""
#         print(response)
        print("Call send.")
        csock.send("Hello world.")
        print("Close socket")
        csock.close()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))


sock.close()
