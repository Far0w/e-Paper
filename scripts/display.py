import logging
from PIL import Image,ImageDraw,ImageFont
import os

class Display:
    
    def __init__(self, epd, picdir, libdir, fontdir):
        self.epd = epd
        self.picdir = picdir
        self.libdir = libdir
        self.fontdir = fontdir
        self.height = epd.height
        self.width  = epd.width
        self.frames = []
        self.canva = Image.new('1', (self.height, self.width), 255)  # image file where all object are drawn on 
        
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
        self.update_display(Limage)
        time.sleep(2)
    
    def update_display(self, img):
        self.epd.display(self.epd.getbuffer(img))
    
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
    
class Frame:
    
    def __init__(self, width = 10, height = 10, posX = 0, posY = 0):
        self.height = height
        self.width  = width
        self.posX = posX
        self.posY = posY
        
       