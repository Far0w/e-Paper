#From https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
import requests, json


class WeatherAPI():
    def __init__(self):
        self.api_key = "264308798c3239b2dc857702b9155206" # to hide after
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.city_name = "Copenhagen"

        self.complete_url = self.base_url + "appid=" + self.api_key + "&q=" + self.city_name
        
    def request_data(self):
        response = requests.get(self.complete_url)

        self.x = response.json()

        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found
        if self.x["cod"] != "404":
            print(self.x)
            # store the value of "main"
            # key in variable y
            self.y = self.x["main"]

            # store the value corresponding
            # to the "temp" key of y
            self.current_temperature = self.y["temp"]

            # store the value corresponding
            # to the "pressure" key of y
            self.current_pressure = self.y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            self.current_humidity = self.y["humidity"]

            # store the value of "weather"
            # key in variable z
            self.z = self.x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            self.weather_description = self.z[0]["description"]

            # print following values
            print(" Temperature (in kelvin unit) = " +
                            str(self.current_temperature) +
                "\n atmospheric pressure (in hPa unit) = " +
                            str(self.current_pressure) +
                "\n humidity (in percentage) = " +
                            str(self.current_humidity) +
                "\n description = " +
                            str(self.weather_description))

        else:
            print(" City Not Found ")
