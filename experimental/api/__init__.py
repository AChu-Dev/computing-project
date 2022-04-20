import requests
import time
import datetime
from database.db import *

class api:
	url = "https://api.weatherunlocked.com/api/resortforecast/54883444?app_id=a3fd6c9a&app_key=027a1023047a432b9ed2e4a7db484a07&hourly_interval=6"
	last_request = 0
	request_interval = 87
	cached = None
	con = None
	curs = None

	def __init__(self):
		db = 'snow'
		self.con, self.curs = newcon(db)
		if self.has_database_connection():
			if not(tablecreate(self.curs, self.con)):
				closecon()
				self.con = None
				self.curs = None
		pass

	def has_database_connection(self):
		return (self.con != None and self.curs != None)

	def get_weather(self):
		try:
			if self.weather_cache_updatable():
				response = requests.get(self.url, headers={"Accept": "application/json"})
				if response:
					response = response.json()
					for forecast in response["forecast"]:
						for segment in ["base", "mid", "upper"]:
							insertWeather(datetime.datetime.combine(datetime.datetime.strptime(forecast["date"], "%d/%m/%Y"), datetime.datetime.strptime(forecast["time"], "%H:%M").time()), forecast[segment]["temp_min_c"], forecast[segment]["temp_max_c"], forecast[segment]["feelslike_c"], forecast["precip_in"], forecast["vis_mi"], forecast[segment]["winddir_compass"], forecast[segment]["windspd_mph"], forecast[segment]["freshsnow_in"], segment, response["id"], self.curs)
					self.cached = response.json()["forecast"]
					self.last_request = time.time()
		except:
			self.cached = None
		return self.cached
	
	def get_resort(self, resort):
		return getResorts(resort, self.curs)

	def get_user(self, user):
		return getUsers(user, self.curs)

	def get_user_favourites(self, user):
		return getUserFavourites(user, self.curs)

	def weather_cache_updatable(self):
		return (self.last_request < (time.time() - self.request_interval) or self.cached == None)