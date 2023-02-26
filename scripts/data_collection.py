import pandas as pd
from dateutil import parser
import requests, json

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
    
    def __init__(self, token, database_id):
        self.token = token
        self.database_id = database_id
    
    def download_todo_list(self):
        self.read_URL = "https://api.notion.com/v1/databases/{}/query".format(self.database_id)
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Notion-Version": "2022-06-28" # to be updated according to https://developers.notion.com/reference/retrieve-a-database
        }
        
        self.res = requests.request("POST", self.read_URL, headers=self.headers)
        
        if self.res.status_code == 200:
            print("Notion data sucessfully acquired.")
        else:
            print("Notion data not acquired. ERROR :{}".format(self.res.status_code))
        
        self.todolist_items = [self.res.json()["results"][i]["properties"]["Name"]["title"][0]["text"]["content"] for i in range(len(self.res.json()["results"]))]
        #print(self.json_res)
        
        return self.todolist_items
        #print(self.res.json()['title'])
        #print(pd.read_json(self.res.json()))