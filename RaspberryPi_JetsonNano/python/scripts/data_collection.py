import pandas as pd
from dateutil import parser

class dataCollector:
    
    def __init__(self, eventsSpreadsheetURL:str):
        self.events_spreadsheet_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRJtzo9q4NS01XynS0s6ic1da7o8sENcO_QCBlt9UbrKw24ltaRj0cdAKcRCSoG3j4-QdSvMJnxBb_i/pub?output=csv'
        
    def download_events(self):
        colnames = ['date','event']
        try:
            df = pd.read_csv(self.events_spreadsheet_URL, names=colnames)
            events = [ [parser.parse(df.iloc[i].date), df.iloc[i].event] for i in range(len(df))]
            print("Events download sucessful.")
        except:
            print("Events download failed.")