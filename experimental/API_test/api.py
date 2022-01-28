import os
from dotenv import load_dotenv
import pandas as pd
import datetime

def main(start_date = 0, end_date = 0):
    try:
        load_dotenv()
        key = os.getenv("API_KEY")
    except Exception:
        print("Exception has occured", Exception)

    if end_date == 0 and start_date == 0:
        start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Southampton/" + start_date + "/" + end_date +"?unitGroup=metric&elements=datetime%2CdatetimeEpoch%2Cname%2Caddress%2Clatitude%2Clongitude%2Ctempmax%2Ctempmin%2Ctemp%2Cfeelslikemax%2Cfeelslikemin%2Cfeelslike%2Chumidity%2Cprecip%2Cprecipprob%2Cprecipcover%2Cpreciptype%2Csnow%2Csnowdepth%2Cwindgust%2Cwindspeed%2Cwinddir%2Cpressure%2Ccloudcover%2Csunrise%2Csunset%2Cmoonphase&include=days&key=" + key + "&maxStations=1&contentType=json"
    res = pd.read_json(url)

    data = []
    for i in range(len(res['days'])):
        data.append(res['days'][i])

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d", errors='coerce')
    print(df)
    return df

if __name__ == "__main__":
    main()
