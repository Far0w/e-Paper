#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd
from dateutil import parser
from data_collection import dataCollector
from weather import WeatherAPI
from display import Display, Canva, Text, Rectangle, Line, Picture
import logging
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as date
import traceback
import time
import signal
import credentials
from quote import cli as QuoteAPI

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')

if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

title_font = ImageFont.truetype(os.path.join(fontdir, 'BebasKai.ttf'), 50)
text_font = ImageFont.truetype(os.path.join(fontdir, 'KeepCalm.ttf'), 16)

months = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"] # For calendar display

refresh_time = 10 # time in minutes to refresh the screen

data_collector = dataCollector(credentials.calendar_spreadsheet_link)
weatherAPI = WeatherAPI(credentials.weather_API_key)

def signal_handler(signal, frame): # To cut the infinite loop
    global interrupted
    interrupted = True

def display_calendar_event(canva):
    X = 15
    Y = 500
    text_spacing = 20
    week_spacing = 8
    weeks_number = 0 #To store how many weeks are there
    lastWeek = calendar_events[0][0].isocalendar().week
    for i_event in range(len(calendar_events)):
        date_str = str(calendar_events[i_event][0].day) + " " + months[calendar_events[i_event][0].month-1] + " - " + str(calendar_events[i_event][0].hour) + ":" + ("0" + str(calendar_events[i_event][0].minute))[-2:]
        if calendar_events[i_event][0].isocalendar().week != lastWeek:
            lastWeek = calendar_events[i_event][0].isocalendar().week
            canva.add_object(Line([X, Y+text_spacing*i_event+weeks_number*week_spacing, X+100, int(Y+text_spacing*i_event+weeks_number*week_spacing)]))
            weeks_number += 1
        canva.add_object(Text(text_font, X, Y+text_spacing*i_event+weeks_number*week_spacing, date_str + " | "+ calendar_events[i_event][1], 0))
        
def display_weather_data(canva):
    X = -20
    Y = 100
    bmp = Image.open(os.path.join(picdir, weatherAPI.icon + '.bmp'))
    canva.add_object(Picture(bmp, X,Y-50))
    
    canva.add_object(Text(title_font, X+180, Y, "{}°C".format(weatherAPI.current_temperature), 0, "center"))
    canva.add_object(Text(text_font, X+180, Y+60, "{}hPa".format(weatherAPI.current_pressure), 0, "center"))
    canva.add_object(Text(text_font, X+180, Y+80, "{}%".format(weatherAPI.current_humidity), 0, "center"))
    canva.add_object(Line([X+280,Y+10,X+280,Y+90]))

def display_title_date(canva):
    X_size = 480
    Y_size = 72
    canva.add_object(Rectangle(0,0,X_size-1,Y_size-1))
    todayDate = date.today().strftime("%A %d %B")
    text_width, text_height = canva.draw.textsize(todayDate, title_font)
    canva.add_object(Text(title_font, X_size//2 - (text_width / 2), Y_size//2 - (text_height / 2)-5, todayDate, 0, "left"))
    
    
def display_footer(canva):
    canva.add_object(Rectangle(0,765,479,35,0))
    canva.add_object(Text(text_font, 10, 780, "Last update: {}/{} | {}.".format(date.today().strftime("%d"), date.today().strftime("%m"), date.today().strftime("%R")), 255, "center"))

def display_quotes(canva, author = "Nietzsche"):
    X = 10
    Y = 300
    padding = 10
    quote_limit = 250
    quote = QuoteAPI.random_search(author)
    logging.info("New quote: {} | size: {}.".format(quote, len(quote)))
    nb_iter = 1
    max_iter = 25
    while len(quote) > quote_limit and nb_iter < max_iter: # To get only "small" quotes ( limited by length size < quote_limit)
        quote = QuoteAPI.random_search(author)
        logging.info("New quote: {} | size: {}.".format(quote, len(quote)))
        nb_iter += 1
        if nb_iter - 1 == max_iter:
            logging.info("Did not found any quote smaller than {} characters.".format(quote_limit))
    canva.add_object(Rectangle(X = X, Y = Y, width = 460, height = 75, fill_color = 225, outline_color = 0, linewidth = 2))
    canva.add_object(Text(text_font, X + padding, Y + padding, quote, 0, "left"))
        

def canva(epd):
    canva_obj = Canva(epd.width,epd.height)
    
    display_weather_data(canva_obj)   
    display_calendar_event(canva_obj)   
    display_title_date(canva_obj)
    display_footer(canva_obj)
    display_quotes(canva_obj)
    
    canva_obj.draw_objects()
    return canva_obj


signal.signal(signal.SIGINT, signal_handler)

interrupted = False

try:
    calendar_events = data_collector.download_events()
    weatherAPI.update_data()

    epd = epd7in5_V2.EPD()
    display = Display(epd, picdir, libdir, fontdir)

    display.clear()

    display.draw_canva(canva(epd))

    display.sleep()


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
