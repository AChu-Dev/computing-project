import json
import requests
import os
from dotenv import load_dotenv

def main():
    try:
        load_dotenv()
        key = os.getenv("API_KEY")
    except Exception:
        print("Exception has occured", Exception)
    
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Southampton/last15days?include=fcst%2Cobs%2Chistfcst%2Cstats%2Chours&key=" + key + "&options=preview&contentType=json"
    res = requests.get(url).text
    print(res)

    res_json = json.loads(res)
    print(res_json)


if __name__ == "__main__":
    main()
