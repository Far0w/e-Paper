import logging
from PIL import Image,ImageDraw,ImageFont
import os
import time

# Display is a technical object to update the display, make it slept, clear it

class Display:
    
    def __init__(self, epd, picdir, libdir, fontdir):
        self.epd = epd
        self.picdir = picdir
        self.libdir = libdir
        self.fontdir = fontdir
        self.height = epd.height
        self.width  = epd.width
        self.frames = []
        
        self.title_font = ImageFont.truetype(os.path.join(self.fontdir, 'NiceChalk.ttf'), 50)
        self.text_font = ImageFont.truetype(os.path.join(self.fontdir, 'Font0.ttc'), 18)
    
    def test(self):

        
        logging.info("2.Drawing on the Vertical image...")
        self.Limage = Image.new('1', (self.height, self.width), 255)  # 255: clear frame
        draw = ImageDraw.Draw(self.Limage)
        draw.text((2, 5), 'Title test', font = self.title_font, fill = 0)
        draw.text((2, 50), 'Ecran 7.5 pouces', font = self.text_font, fill = 0)
        draw.text((2, 80), 'Test 2', font = self.text_font, fill = 0)
        #draw.line((10, 90, 60, 140), fill = 0)
        #draw.line((60, 90, 10, 140), fill = 0)
        #draw.rectangle((10, 90, 60, 140), outline = 0)
        #draw.line((95, 90, 95, 140), fill = 0)
        #draw.line((70, 115, 120, 115), fill = 0)
        #draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        draw.rectangle((10, 150, 60, 200), fill = 0)
        draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        #self._update_display(self.Limage)
        time.sleep(2)
        
    def canva1(self):
        #self.canva.draw_rect()
        canva1 = Canva(self.width,self.height)
        
        canva1.add_object(Rectangle(0,0,479,72))
        canva1.add_object(Text(self.title_font, 36, 5, 'SAMEDI 18 FEVRIER', 0, "center"))
        
        canva1.draw_objects()
        self.draw_canva(canva1)
        time.sleep(2)
    
    def draw_canva(self, canva):
        self.epd.display(self.epd.getbuffer(canva.image))
    
    def clear(self):
        logging.info("Clear...")
        self.epd.init()
        self.epd.Clear()
        
    def sleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()
    
    
class Canva: # Object to draw on that will return an image to display
    def __init__(self, display_width = 100, display_height = 100, vertical_mode=True):
        if vertical_mode:
            self.height = display_height
            self.width  = display_width
        else:
            self.height = display_width
            self.width  = display_height
        self.vertical_mode = vertical_mode
        self.image = Image.new('1', (self.height, self.width), 255)  # image file where all object are drawn on 
        self.objects = []
        #self.fontdir = fontdir
        #self.title_font = ImageFont.truetype(os.path.join(self.fontdir, 'NiceChalk.ttf'), 40)
        
    def add_object(self, obj):
        self.objects.append(obj)
        
    def draw_objects(self):
        self.image = Image.new('1', (self.height, self.width), 255) # clearing canva
        self.draw = ImageDraw.Draw(self.image)
        for obj in self.objects:
            if isinstance(obj, Rectangle):
                logging.info("Drawing a rectangle...")
                if self.vertical_mode:
                    self.draw.rectangle((obj.X, obj.Y, obj.X+obj.width, obj.Y+obj.height), fill = obj.fill_color, outline = obj.outline_color, width = obj.linewidth)
                else:
                    self.draw.rectangle((obj.X, obj.Y, obj.X+obj.width, obj.Y+obj.height), fill = obj.fill_color, outline = obj.outline_color, width = obj.linewidth)
            elif isinstance(obj, Text):
                logging.info("Drawing a text...")
                self.draw.text((obj.X, obj.Y), obj.text, font = obj.font, fill = obj.fill_color, align = obj.align)
            elif isinstance(obj, Line):
                logging.info("Drawing a line...")
                self.draw.line(obj.xy, fill = obj.fill_color, width = obj.width)
            elif isinstance(obj, Image):
                logging.info("Drawing a image...")
                self.image.paste(obj.image, (obj.X,obj.Y))
                
        logging.info("Drawing ended.")

        
class Rectangle:
    def __init__(self, X = 0, Y = 0, width = 10, height = 10, fill_color = 255, outline_color = 0, linewidth = 2):
        self.width = width
        self.height = height
        self.X = X
        self.Y = Y
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.linewidth = linewidth
        
class Line:
    def __init__(self, xy = [], fill_color = 0, width = 2):
        self.xy = xy
        self.fill_color = fill_color
        self.width = width
        
class Text:
    def __init__(self, font, X = 0, Y = 0, text = "", fill_color = 0, align= "left"):
        self.X = X
        self.Y = Y
        self.font = font
        self.text = text
        self.fill_color = fill_color
        self.align = align
        
class Image:
    def __init__(self, bmp, X = 0, Y = 0):
        self.image = bmp
        self.X = X
        self.Y = Y

#ImageDraw.text(xy, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None, features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class Module: # Module inside canva
    
    def __init__(self, width = 10, height = 10, posX = 0, posY = 0):
        self.height = height
        self.width  = width
        self.posX = posX
        self.posY = posY
        
       
    
    
    
    
    
    
    
    #logging.info("3.read bmp file")
    #Himage = Image.open(os.path.join(self.picdir, '7in5_V2.bmp'))
    #epd.display(epd.getbuffer(Himage))
    #time.sleep(2)

    #logging.info("4.read bmp file on window")
    #Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    #bmp = Image.open(os.path.join(self.picdir, '100x100.bmp'))
    #Himage2.paste(bmp, (50,10))
    #epd.display(epd.getbuffer(Himage2))
    #time.sleep(2)
        
       