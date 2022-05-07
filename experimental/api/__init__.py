import requests
import time
from database.db import *

class api:
	urls = [
		{
			"resort": [
				333031,
				"Saint Martin De Belleville"
			],
			"url": "https://api.weatherunlocked.com/api/resortforecast/333031?app_id=a3fd6c9a&app_key=027a1023047a432b9ed2e4a7db484a07&hourly_interval=6"
		},
		{
			"resort": [
				333005,
				"Courchevel"
			],
			"url": "https://api.weatherunlocked.com/api/resortforecast/333005?app_id=4c84c18d&app_key=5f4b7efa21bbda9d00d158c7c11ac815&hourly_interval=6"
		},
		{
			"resort": [
				333014,
				"Meribel"
			],
			"url": "https://api.weatherunlocked.com/api/resortforecast/333014?app_id=62707ed6&app_key=10981bcbfd38f7a0b53bb253990c0cbf&hourly_interval=6"
		},
	]
	ids = {"333031": 0, "333005": 1, "333014": 2}
	last_request = [0, 0, 0]
	request_interval = 87
	cached = [None, None, None]
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

	def get_weather(self, id):
		try:
			id = str(id)
			if not id in self.ids.keys():
				raise None
			if self.weather_cache_updatable(self.ids[id]):
				response = requests.get(self.urls[self.ids[id]]["url"], headers={"Accept": "application/json"})
				if response:
					response = response.json()
					self.cached[self.ids[id]] = response["forecast"]
					self.last_request[self.ids[id]] = time.time()
		except:
			self.cached[self.ids[id]] = None
		return self.cached[self.ids[id]]
	
	def get_resort(self, resort):
		return getResorts(resort, self.curs)

	def get_user(self, user):
		return getUsers(user, self.curs)

	def get_user_favourites(self, user):
		return getUserFavourites(user, self.curs)

	def weather_cache_updatable(self, id):
		return (self.last_request[id] < (time.time() - self.request_interval) or self.cached[id] == None)
