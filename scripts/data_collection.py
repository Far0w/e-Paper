import pandas as pd
from dateutil import parser

class GSheetDataCollector:
    
    def __init__(self, events_spreadsheet_URL:str):
        self.events_spreadsheet_URL = events_spreadsheet_URL
        
    def download_events(self):
        colnames = ['date','event']
        events = ["No data found."]
        try:
            df = pd.read_csv(self.events_spreadsheet_URL, names=colnames)
            events = [ [parser.parse(df.iloc[i].date), df.iloc[i].event] for i in range(len(df))]
            print("Events download sucessful. {} events downloaded.".format(len(events)))
        except:
            print("Events download failed. 0 event downloaded.")
        return events
    
    
class NotionDataCollector:
    
    def __init__(self):
        pass
