import requests

signup0 = {"username":["Joe"], "email":["Joe@Appleton.co.uk"], "password1": ["JoeAppleton"]}
response0 = requests.post("http://127.0.0.1:8000/rest_api/duser/create/", data = signup0)
print(response0)
print(response0.json)


signin0 = {"username": ["Joe"], "password":["JoeAppleton"]}
#response1 = requests.post("http://127.0.0.1:8000/rest_api/signin/", data = signin0)
#print(response1)
#print(response1.json)

signout = {}
#response2 = requests.post("http://127.0.0.1:8000/rest_api/signout/", data = signout)
#print(response2)
#print(response2.json)
