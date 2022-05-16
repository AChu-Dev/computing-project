import requests
import os
import shutil

os.remove('db.sqlite3')
shutil.copy('db_backup/db.sqlite3', './')

def assertEqual(call, code):
    if (call.status_code == code):
        print('TEST SUCCEED')
    else: 
        print('TEST FAILED')


datav2 = {
        'name': ['Three Valleys: Test 1v2'],
        'address': ['France'],
        'longitude': ['-50.32'],
        'latitude': ['32.2'],
        'description': ['This is a nice place'],
        "image": [""]}


print('------------------------------------------------------')
print('CREATE TEST - RESORT')
for x in range(0, 3):
    datav1 = {
            'name': ['Three Valleys: Test {}'.format(x)],
            'address': ['France'],
            'longitude': ['-50.32'],
            'latitude': ['32.2'],
            'description': ['This is a nice palce'],
            "image": [""]}
    print(datav1)
    response_post = requests.post("http://127.0.0.1:8000/rest_api/resort/", data = datav1)
    print(response_post.status_code)
    assertEqual(response_post, 201)
print('------------------------------------------------------')

print('LIST TEST - RESORT')
response_get = requests.get("http://127.0.0.1:8000/rest_api/resort/")
print(response_get.status_code)
print(response_get.json())
assertEqual(response_get, 200)
print('--------------------------------------------------

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
