#!/usr/bin/python3

import logging

loggingLevel = logging.INFO

#FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
#logging.basicConfig(format=FORMAT)

# create logger with 'spam_application'
logger = logging.getLogger('climate_station')
logger.setLevel(loggingLevel)

# create file handler which logs even debug messages
#fh = logging.FileHandler('webcam.log')
#fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(loggingLevel)

# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('[ %(levelname)5s - %(filename)16s:%(lineno)3s - %(funcName)16s ] %(message)s')
#fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
#logger.addHandler(fh)
logger.addHandler(ch)
