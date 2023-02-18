#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd
from dateutil import parser
from data_collection import dataCollector
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
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    display = Display(epd)
    
    display.clear()

    title_font = ImageFont.truetype(os.path.join(fontdir, 'NiceChalk.ttf'), 40)
    text_font = ImageFont.truetype(os.path.join(fontdir, 'Font0.ttc'), 18)


    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    Limage = Image.new('1', (display.height, display.width), 255)  # 255: clear frame
    draw = ImageDraw.Draw(Limage)
    draw.text((2, 5), 'Title test', font = title_font, fill = 0)
    draw.text((2, 50), 'Ecran 7.5 pouces', font = text_font, fill = 0)
    draw.text((2, 80), 'Test 2', font = text_font, fill = 0)
    #draw.line((10, 90, 60, 140), fill = 0)
    #draw.line((60, 90, 10, 140), fill = 0)
    #draw.rectangle((10, 90, 60, 140), outline = 0)
    #draw.line((95, 90, 95, 140), fill = 0)
    #draw.line((70, 115, 120, 115), fill = 0)
    #draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
    draw.rectangle((10, 150, 60, 200), fill = 0)
    draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
    display.display(Limage)
    time.sleep(2)

    #logging.info("3.read bmp file")
    #Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
    #epd.display(epd.getbuffer(Himage))
    #time.sleep(2)

    #logging.info("4.read bmp file on window")
    #Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    #bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    #Himage2.paste(bmp, (50,10))
    #epd.display(epd.getbuffer(Himage2))
    #time.sleep(2)
    display.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
