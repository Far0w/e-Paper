#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd
from dateutil import parser
from data_collection import dataCollector
from display import Display
import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

data_collector = dataCollector('https://docs.google.com/spreadsheets/d/e/2PACX-1vRJtzo9q4NS01XynS0s6ic1da7o8sENcO_QCBlt9UbrKw24ltaRj0cdAKcRCSoG3j4-QdSvMJnxBb_i/pub?output=csv')
calendar_events = data_collector.download_events()


try:
    epd = epd7in5_V2.EPD()
    display = Display(epd, picdir, libdir, fontdir)
    
    display.clear()

    display.test()

    display.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
