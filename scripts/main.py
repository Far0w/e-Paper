#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd
from dateutil import parser
from data_collection import dataCollector
from display import Display, Canva, Text, Rectangle
import logging
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import traceback
import time

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

data_collector = dataCollector('https://docs.google.com/spreadsheets/d/e/2PACX-1vRJtzo9q4NS01XynS0s6ic1da7o8sENcO_QCBlt9UbrKw24ltaRj0cdAKcRCSoG3j4-QdSvMJnxBb_i/pub?output=csv')
calendar_events = data_collector.download_events()

months = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

def canva(epd):
    title_font = ImageFont.truetype(os.path.join(fontdir, 'NiceChalk.ttf'), 50)
    text_font = ImageFont.truetype(os.path.join(fontdir, 'Font0.ttc'), 18)
    canva1 = Canva(epd.width,epd.height)

    canva1.add_object(Rectangle(0,0,479,72))
    canva1.add_object(Text(title_font, 36, 5, 'SAMEDI 18 FEVRIER', 0, "center"))
    for i_event in range(len(calendar_events)):
        date_str = str(calendar_events[i_event][0].day) + " " + months[calendar_events[i_event][0].month-1] + " | " + str(calendar_events[i_event][0].hour) + ":" + str(calendar_events[i_event][0].minute)
        canva1.add_object(Text(text_font, 36, 30+18*i_event, date_str + event[1], 0, "center"))

    canva1.draw_objects()
    return canva1
    
try:
    epd = epd7in5_V2.EPD()
    display = Display(epd, picdir, libdir, fontdir)
    
    display.clear()

    #display.canva1()
    display.draw_canva(canva(epd))
    time.sleep(2)
        

    display.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
