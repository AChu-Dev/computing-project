import db
from db import *

db = 'snow'
con,curs = newcon(db)

tablecreate(curs,con)


user_name = 'test'
first_name = 'test'
last_name = 'test'
email = 'test@test'
permission = 1
num_fav_resorts = 0
insertUser(user_name,first_name,last_name,email,permission,num_fav_resorts,curs)

users = getUser('*',curs)
print(users)
user_id = users['user_id'][0]

print(user_id)

name = 'testres'
address = 'test street'
longitude = 1
latitude = 1


insertResort(name,address,longitude,latitude,curs)

resorts = getResorts('*',curs)
print(resorts)

resort_id = resorts['resort_id'][0]

insertFavourite(user_id,resort_id,curs)

favourites  = getUserFavourites(user_name,curs)

print(favourites)

favourites = getUserFavourites('*',curs)

resort_id = resort_id
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

insertWeather(
        date,
        min_temp,
        max_temp,
        feels_like,
        precipitation_probability,
        visibility,
        wind_direction,
        wind_speed,
        snow_depth,
        mountain_segment,
        resort_id,
        curs)

weather = getWeather('testres',curs)

print(weather)


removeResort('*',curs)

removeResort(resort_id,curs)

print(getResorts('*',curs))

print(getWeather('*',curs))

print(getUserFavourites('*',curs))


insertWeather(
        date,
        min_temp,
        max_temp,
        feels_like,
        precipitation_probability,
        visibility,
        wind_direction,
        wind_speed,
        snow_depth,
        mountain_segment,
        resort_id,
        curs)

print(getWeather('testres',curs))

removeWeather('resort_id',1,curs)

print(getWeather('testres',curs))

#print(getUser('*',curs))
#removeUser(1,curs)



insertResort(name,address,longitude,latitude,curs)
print(getUserFavourites('*',curs))
removeFavourite(1,1,curs)
print(getUserFavourites('*',curs))


