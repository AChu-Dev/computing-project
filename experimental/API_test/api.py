import requests
import time

class api:
	url = "https://api.weatherunlocked.com/api/resortforecast/54883444?app_id=a3fd6c9a&app_key=027a1023047a432b9ed2e4a7db484a07"
	last_request = 0
	request_interval = 87
	cached = None

	def __init__(self) -> None:
		pass

	def get_weather(self):
		try:
			if self.updatable():
				response = requests.get(self.url, headers={"Accept": "application/json"})
				if response:
					self.cached = response.json()["forecast"]
					self.last_request = time.time()
		except:
			self.cached = None
		return self.cached

	def updatable(self):
		return (self.last_request < (time.time() - self.request_interval) or self.cached == None)