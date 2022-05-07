import json
import matplotlib.pyplot as plt

def render_historic():
	formatted = []
	with open("static/historical_weather-2021.json", 'r') as f:
		data = json.load(f)
		output = []
		month_count = 1
		for month in data:
			dates = month["date"]
			month["snow"] = []
			average = {"temp": 0, "prec": 0, "snow": 0}
			for day in range(len(dates)):
				temp = month["temp"][day]
				prec = month["prec"][day]
				snow = 0
				if temp[0] <= 0:
					snow = prec
					month["prec"][day] = 0
				month["snow"].append(snow)
				average["temp"] += ((temp[0] + temp[1]) / 2)
				average["prec"] += month["prec"][day]
				average["snow"] += month["snow"][day]
			average["temp"] /= len(dates)
			average["prec"] /= len(dates)
			average["snow"] /= len(dates)
			output.append({"month": round(month_count,2), "temp": round(average["temp"],2), "prec": round(average["prec"],2), "snow": round(average["snow"], 2)})
			month_count += 1
		formatted = output
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	temp = [date["temp"] for date in formatted]
	prec = [date["prec"] for date in formatted]
	snow = [date["snow"] for date in formatted]
	figure = plt.gcf()
	figure.set_size_inches(7, 5)
	plt.plot(months, temp, label = "Temperature (°C)", linewidth=2)
	plt.plot(months, prec, label = "Precipitation (mm)", linewidth=3)
	plt.plot(months, snow, label = "Snowfall (mm)", linewidth=4)
	plt.title("Average historic weather (2021)")
	plt.legend()
	plt.savefig("static/historic_weather_2021.png", bbox_inches='tight')
