import logging

class Display:
    
    def __init__(self, epd):
        self.epd = epd
        self.height = epd.height
        self.width  = epd.width
    
    def display(self, img):
        self.epd.display(self.epd.getbuffer(img))
    
    def clear(self):
        logging.info("Clear...")
        self.epd.init()
        self.epd.Clear()
        
    def sleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()
        
       