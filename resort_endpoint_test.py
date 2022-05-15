import requests

datav2 = {'name': ['Three Valleys'], 'address': ['France'], 'longitude': ['-50.32'], 'latitude': ['32.2'], 'description': ['This is a nice palce'], "image": [""]}
response = requests.post("http://127.0.0.1:8000/rest_api/resort/", data = datav2)
print(response)
print(response.json())

response_get = requests.get("http://127.0.0.1:8000/rest_api/resort/")
print(response_get)
print(response_get.json())

response_delete = requests.delete("http://127.0.0.1:8000/rest_api/resorts/4/", data={})
print(response_delete)
