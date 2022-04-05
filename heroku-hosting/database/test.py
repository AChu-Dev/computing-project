import db
from db import *

db = 'snow'
con,curs = newcon(db)

tablecreate(curs,con)

user_name = 'test'
first_name = 'testy'
last_name = 'testerton'
email = 'test@test.test'
permission = 1
num_fav_resorts = 0

insertUser(user_name,first_name,last_name,email,permission,num_fav_resorts,curs)


name = 'testres'
address = 'test street'
longitude = 1
latitude = 1

insertResort(name,address,longitude,latitude,curs)

resort_id = 1
date = '01/03/2020'
min_temp = 10
max_temp = 20
feels_like = 15
precipitation_probability = 5
visibility = 4
wind_direction = 'N' 
wind_speed = 100 
snow_depth = 100
mountain_segment = 2


insertWeather(date,min_temp,max_temp,feels_like,precipitation_probability,visibility,wind_direction,wind_speed,snow_depth,mountain_segment,resort_id,curs)

print(getWeather('testres',curs))

updateWeather('snow_depth','10','resort_id','1',curs)

print(getWeather('testres',curs))
