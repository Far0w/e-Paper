#From https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
import requests, json
import datetime


class WeatherAPI():
    def __init__(self, API_key):
        self.api_key = API_key # to hide after
        self.base_url_current = "http://api.openweathermap.org/data/2.5/weather?"
        self.base_url_forecast = "http://api.openweathermap.org/data/2.5/forecast?"
        #http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
        self.city_name = "Copenhagen"
        self.complete_url_current_weather  = self.base_url_current  + "appid=" + self.api_key + "&q=" + self.city_name + "&units=metric"
        self.complete_url_next_day_weather = self.base_url_forecast + "appid=" + self.api_key + "&q=" + self.city_name + "&units=metric&cnt=16" # Ask for 16 next 3h forecast
        self.current_temperature = "NA"
        self.current_pressure = "NA"
        self.current_humidity = "NA"
        self.current_weather_desc = "NA"
        self.current_weather_icon = None
        self.tomorrow_min_temperature = "NA"
        self.tomorrow_max_temperature = "NA"
        self.tomorrow_weather_desc = "NA"
        self.tomorrow_weather_icon = None
        #self.returned_json = None
        
    def update_data(self):
        # --- Current weather data
        response_current_weather = requests.get(self.complete_url_current_weather)

        self.x = response_current_weather.json()

        if self.x["cod"] != "404":
            #print(self.x)
            self.y = self.x["main"]
            self.current_temperature = "{:.1f}".format(self.y["temp"])
            self.current_pressure = self.y["pressure"]
            self.current_humidity = self.y["humidity"]
            self.z = self.x["weather"]
            self.current_weather_desc = self.z[0]["description"]
            self.current_weather_icon = self.z[0]["icon"][:-1]

        else:
            print("No weather data found.")
            
        # --- Forecast weather data
            
        response_forecast_weather = requests.get(self.complete_url_next_day_weather)

        self.x = None
        self.x = response_forecast_weather.json()

        self.tomorrow_day_of_month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")
        self.tomorrow_weathers = []
        self.tomorrow_weathers_icons = []
        self.tomorrow_temperatures = []
            
        if self.x["cod"] != "404":
            print(self.x)
            for i in range(len(self.x['list'])): # Checking each data and finding data for tommorow
                if (self.x['list'][i]['dt_txt'][8:10] == self.tomorrow_day_of_month):
                    self.tomorrow_temperatures.append(self.x['list'][i]['main']['temp'])
                    self.tomorrow_weathers.append(self.x['list'][i]['weather'][0]['description'])
                    self.tomorrow_weathers_icons.append(self.x['list'][i]['weather'][0]['icon'])
            
            self.tomorrow_min_temperature = str( round( float( min( self.tomorrow_temperatures ) ) ) )
            self.tomorrow_max_temperature = str( round( float( max( self.tomorrow_temperatures ) ) ) )
            self.tomorrow_weather_desc = self.most_frequent(self.tomorrow_weathers)
            self.tomorrow_weather_icon = self.most_frequent(self.tomorrow_weathers_icons)

        else:
            print("No weather data found.")
            
    @staticmethod        
    def most_frequent(List):
        return max(set(List), key = List.count)
