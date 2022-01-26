import json
import requests
import os
from dotenv import load_dotenv

url_link = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Southampton/2021-12-08/2022-02-10?unitGroup=metric&elements=datetime%2CdatetimeEpoch%2Cname%2Clatitude%2Clongitude%2Ctempmax%2Ctempmin%2Ctemp%2Cfeelslikemax%2Cfeelslikemin%2Cfeelslike%2Chumidity%2Cprecip%2Cprecipprob%2Cprecipcover%2Cpreciptype%2Csnow%2Csnowdepth%2Cwindgust%2Cwindspeed%2Cwinddir%2Cpressure%2Ccloudcover%2Cvisibility%2Csunrise%2Csunset%2Cmoonphase%2Cstations%2Csource&include=days&key=EAJDPXFMSTWTK5J8K6KG5TUCY&contentType=json"

def pull_daily_data(start_date, end_date, location):
    try:
        load_dotenv()
        key = os.getenv("API_KEY")
    except Exception:
        print("Exception has occured", Exception)

class get_data():
    def __init__(self):
        try:
            load_dotenv()
            key = os.getenv("API_KEY")
        except Exception:
            print("Exception has occured", Exception)

    def daily_data(self, start_date, end_date, location):
        try:
            load_dotenv()
            key = os.getenv("API_KEY")
        except Exception:
            print("Exception has occured", Exception)

    def hourly_data(self, start_date, end_date, location):
        pass



if __name__ == "__main__":
    pass
