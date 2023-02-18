import logging

class Display:
    
    def __init__(self, epd):
        self.epd = epd
        self.height = epd.height
        self.width  = epd.width
        self.events_spreadsheet_URL = events_spreadsheet_URL
    
    def display(self, img):
        epd.display(epd.getbuffer(img))
    
    def clear(self):
        logging.info("Clear...")
        self.epd.init()
        self.epd.Clear()
        
    def sleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()
        
       