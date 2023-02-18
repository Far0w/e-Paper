import pandas as pd
from dateutil import parser

class dataCollector:
    
    def __init__(self, events_spreadsheet_URL:str):
        self.events_spreadsheet_URL = events_spreadsheet_URL
        
    def download_events(self):
        colnames = ['date','event']
        try:
            df = pd.read_csv(self.events_spreadsheet_URL, names=colnames)
            events = [ [parser.parse(df.iloc[i].date), df.iloc[i].event] for i in range(len(df))]
            print("Events download sucessful.")
        except:
            print("Events download failed.")