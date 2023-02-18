import logging
from PIL import Image,ImageDraw,ImageFont
import os
import time

class Display:
    
    def __init__(self, epd, picdir, libdir, fontdir):
        self.epd = epd
        self.picdir = picdir
        self.libdir = libdir
        self.fontdir = fontdir
        self.height = epd.height
        self.width  = epd.width
        self.frames = []
        self.canva = Canva(self.width,self.height)
    
    def test(self):
        self.title_font = ImageFont.truetype(os.path.join(self.fontdir, 'NiceChalk.ttf'), 40)
        self.text_font = ImageFont.truetype(os.path.join(self.fontdir, 'Font0.ttc'), 18)
        
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
        self._update_display(self.Limage)
        time.sleep(2)
        
    def canva1(self):
        self.canva.draw_rect()
        self._update_display(self.canva.image)
    
    def _update_display(self, img):
        canva.update()
        self.epd.display(self.epd.getbuffer(canva.image))
    
    def clear(self):
        logging.info("Clear...")
        self.epd.init()
        self.epd.Clear()
        
    def sleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()
        
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
    
    
class Canva: # Objet
    def __init__(self, display_width = 100, display_height = 100, vertical_mode=True):
        if vertical_mode:
            self.height = display_width
            self.width  = display_height
        else:
            self.height = display_height
            self.width  = display_width
        self.image = Image.new('1', (self.height, self.width), 255)  # image file where all object are drawn on 
        self.modules_list = []
        self.draw = ImageDraw.Draw(self.image)
     
    def add_module(self, module):
        self.modules_list.append(module)
        
    def draw_rect(self):
        self.draw.rectangle((10, 150, 60, 200), fill = 0)
        
    def update(self):
        self.new_image = Image.new('1', (self.height, self.width), 255)
        self.draw = ImageDraw.Draw(self.image)
        for module in self.modules_list:
            pass #Draw module
    
class Module:
    
    def __init__(self, width = 10, height = 10, posX = 0, posY = 0):
        self.height = height
        self.width  = width
        self.posX = posX
        self.posY = posY
        
       