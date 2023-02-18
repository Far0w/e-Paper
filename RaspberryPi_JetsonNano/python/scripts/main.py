#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    title_font = ImageFont.truetype(os.path.join(fontdir, 'NiceChalk.ttf'), 40)
    text_font = ImageFont.truetype(os.path.join(fontdir, 'Font0.ttc'), 18)


    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    draw.text((2, 20), 'Title test', font = title_font, fill = 0)
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
    epd.display(epd.getbuffer(Limage))
    time.sleep(20)

    logging.info("3.read bmp file")
    Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("4.read bmp file on window")
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    Himage2.paste(bmp, (50,10))
    epd.display(epd.getbuffer(Himage2))
    time.sleep(2)

    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
