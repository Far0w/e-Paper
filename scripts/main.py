#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd
from dateutil import parser
from data_collection import GSheetDataCollector, NotionDataCollector
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

GSheet_data_collector = GSheetDataCollector(credentials.calendar_spreadsheet_link)
Notion_data_collector = NotionDataCollector(credentials.notion_API_key, credentials.notion_todolist_database_id)
weatherAPI = WeatherAPI(credentials.weather_API_key)

def signal_handler(signal, frame): # To cut the infinite loop
    global interrupted
    interrupted = True

def display_calendar_event(canva):
    X = 15
    Y = 530
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
    canva.add_object(Text(text_font, X+320, Y, "Tomorrow:", 0, "center"))
    canva.add_object(Line([X+300,Y+10,X+300,Y+90]))

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
    
def display_todolist(canva):
    X = 20
    Y = 360
    width = 460
    height = 150
    canva.add_object(Rectangle(X = X, Y = Y, width = width, height = height, fill_color = 225, outline_color = 255, linewidth = 2))
    canva.add_object(Line([(X,Y), (X, Y+height)]))
    todo_icon = Image.open(os.path.join(picdir, 'to_do_icon.bmp'))
    canva.add_object(Picture(todo_icon, X+5,Y+5))
    
    #Downloading tasks on todo list
    tasks = Notion_data_collector.download_todo_list()
    logging.info("Task downloaded: {}.".format(tasks))
    
    for i in range(len(tasks)):
        canva.add_object(Text(text_font, X + 20, Y + (i+1)*20, tasks[i], 0, "left"))
        

def display_quotes(canva, author = "Marcus Aurelius"):
    X = 10
    Y = 220
    width = 460
    height = 75
    Y_size = 100
    padding = 10
    quote_limit = 150
    quote_font = text_font
    quote = QuoteAPI.random_search(author)
    logging.info("New quote: {} | size: {}.".format(quote, len(quote)))
    nb_iter = 1
    max_iter = 25
    
    # Getting a quote
    while len(quote) > quote_limit and nb_iter < max_iter: # To get only "small" quotes ( limited by length size < quote_limit)
        quote = QuoteAPI.random_search(author)
        logging.info("New quote: {} | size: {}.".format(quote, len(quote)))
        nb_iter += 1
        if nb_iter - 1 == max_iter:
            logging.info("Did not found any quote smaller than {} characters. Increase quote_limit.".format(quote_limit))
            quote = "No quote for today!"
            
    # Reformating the quote to fit the module width (not height)
    # Ajouter une condition pour que nb_iter*text_height < height et c'est bon
    selected_quote = quote.replace("\n", " ")
    text_width, text_height = canva.draw.textsize(selected_quote, quote_font)
    width_available = width - 2*padding
    nb_iter = text_width//width_available + 1
    if text_width%width_available != 0 and text_width%width_available !=text_width:
        nb_iter += 1
    quote_words_list = selected_quote.split(" ")
    quote_words_list.reverse()
    formated_quote = ""
    for _ in range(nb_iter):
        line = ""
        line_width, line_height = canva.draw.textsize(line, quote_font)
        while line_width < width_available:
            if len(quote_words_list) > 0:
                line_width, line_height = canva.draw.textsize(line + quote_words_list[-1] + " ", quote_font)
            if (len(quote_words_list) > 0 and line_width >= width_available):
                line += "\n"
            elif len(quote_words_list) > 0:
                line += quote_words_list.pop() + " " # Delete last word from the quote list, add the word to the line, add a space
            else:
                break
        formated_quote += line
    formated_quote += "\n\n{}.".format(author)
    logging.info("Formated quote:\n{}".format(formated_quote))   
    
    # Adding quote + frame
    text_width, text_height = canva.draw.textsize(formated_quote, quote_font)
    X_adjustment = (width_available-text_width)//2
    #canva.add_object(Rectangle(X = X, Y = Y, width = width, height = height, fill_color = 225, outline_color = 0, linewidth = 2))
    canva.add_object(Rectangle(X = X, Y = Y, width = width, height = Y_size, fill_color = 0, outline_color = 0, linewidth = 2))
    canva.add_object(Text(quote_font, X + padding, Y + (Y_size - text_height)/2, formated_quote, 0, "left"))
        

def canva(epd):
    canva_obj = Canva(epd.width,epd.height)
    
    display_weather_data(canva_obj)
    display_title_date(canva_obj)
    
    display_quotes(canva_obj)
    canva_obj.add_object(Line([(50,340), (480-50, 340)], 0, 4))
    display_todolist(canva_obj) 
    display_calendar_event(canva_obj)   
    display_footer(canva_obj)
    
    canva_obj.draw_objects()
    return canva_obj


signal.signal(signal.SIGINT, signal_handler)

interrupted = False

try:
    calendar_events = GSheet_data_collector.download_events()
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
