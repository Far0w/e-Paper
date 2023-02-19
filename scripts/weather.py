#From https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
import requests, json


class WeatherAPI():
    def __init__(self, API_key):
        self.api_key = API_key # to hide after
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.city_name = "Copenhagen"
        self.complete_url = self.base_url + "appid=" + self.api_key + "&q=" + self.city_name
        self.current_temperature = "NA"
        self.current_pressure = "NA"
        self.current_humidity = "NA"
        self.current_weather_desc = "NA"
        
    def update_data(self):
        response = requests.get(self.complete_url)

        self.x = response.json()

        if self.x["cod"] != "404":
            print(self.x)

            
            self.y = self.x["main"]
            self.current_temperature = "{:.1f}".format(self.y["temp"]-273.15)
            self.current_pressure = self.y["pressure"]
            self.current_humidity = self.y["humidity"]
            self.z = self.x["weather"]
            self.current_weather_desc = self.z[0]["description"]

            #print(" Temperature : {} \n atmospheric pressure (in hPa unit) = {} \n humidity (in percentage) = {} \n description = {}".format(str(self.current_temperature),str(self.current_pressure),str(self.current_humidity),str(self.weather_description)))

        else:
            print("No weather data found.")
