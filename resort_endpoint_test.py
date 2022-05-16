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
    assertEqual(response_post, 403)
print('------------------------------------------------------')

print('LIST TEST - RESORT')
response_get = requests.get("http://127.0.0.1:8000/rest_api/resort/")
print(response_get.status_code)
print(response_get.json())
assertEqual(response_get, 200)
print('------------------------------------------------------')

print('UPDATE TEST - RESORT')
response_update = requests.put("http://127.0.0.1:8000/rest_api/resort/1/", data = datav2)
print(response_update.status_code)
assertEqual(response_update, 403)
print('------------------------------------------------------')

print('DELETE TEST - RESORT')
response_delete = requests.delete("http://127.0.0.1:8000/rest_api/resort/2/", data={})
print(response_delete.status_code)
assertEqual(response_delete, 403)
print('------------------------------------------------------')

