import sqlite3
import pandas as pd


def newcon(db):
    try:
        con = sqlite3.connect('{}.db'.format(db))
        print('{}.db'.format(db))
        curs = con.cursor()        
        return con,curs
    except:
        print('database not found')

def tablecreate(curs,con):
    resorts_table= """CREATE TABLE IF NOT EXISTS Resorts (
                      resort_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name VARCHAR(255) NOT NULL,
                      address VARCHAR(255) UNIQUE NOT NULL,
                      longitude REAL NOT NULL,
                      latitude REAL NOT NULL
                      ); """

    weather_table="""CREATE TABLE IF NOT EXISTS Weather(
                     resort_id INTEGER NOT NULL,
                     date datetime,
                     min_temp REAL,
                     max_temp REAL,
                     feels_like REAL,
                     precipitation_probability REAL,
                     visibility REAL,
                     wind_direction VARCHAR(255),
                     wind_speed REAL,
                     snow_depth REAL,
                     mountain_segment INTEGER,
                     FOREIGN KEY (resort_id)
                        REFERENCES Resorts (resort_id)
                     );"""
    
    user_table = """CREATE TABLE IF NOT EXISTS Users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name VARCHAR(255) NOT NULL UNIQUE,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255),
                    email VARCHAR(255) NOT NULL UNIQUE,
                    permission INTEGER NOT NULL,
                    num_fav_resorts INTEGER NOT NULL
                    );"""

    favourites_table = """CREATE TABLE IF NOT EXISTS Favourites(
                          user_id INTEGER NOT NULL,
                          resort_id INTEGER NOT NULL,
                          FOREIGN KEY (user_id)
                            REFERENCES Users (user_id)
                          );"""

    try:
        curs.execute(resorts_table)
        con.commit()
        print('region table found/successfully generated')
    except:
        print('region table missing/failed to generate')
    try:
        curs.execute(weather_table)
        con.commit()
        print('weather table found/successfully generated')
    except:
        print('weather table missing/failed to generate')
    try:
        curs.execute(user_table)
        con.commit()
        print('user table found/successfully generated')
    except:
        print('user table missing/failed to generate')
    try:
        curs.execute(favourites_table)
        con.commit()
        print('favourites table found/successfully generated')
    except:
        print('favourites table missing/failed to generate')
 


#--------------------------------------------------------------------------
# GENERIC QUERY FUNCTIONS, UNSAFE AND UNTESTED
#--------------------------------------------------------------------------

#def genericSelect(curs, params, table, mods):
#     select = """SELECT {}
#                 FROM {}
#                 {}
#                 ;
#                 """.format(params,table,mods)
#    curs.execute(select)
#    result = curs.fetchall()
#
#    result = pd.DataFrame(result)
#    return result

#def genericRemove(curs,params,table,vals):
#    delete = """DELETE FROM {} WHERE {} = {};""".format(table,params,vals)
#    curs.execute(delete)

#def genericInsert(curs,params,table,vals):
#    insert = """INSERT INTO {}({}) VALUES({});""".format(table,params,vals)
#    curs.execute(insert)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
def getResorts(resort,curs):
    if type(resort) == int:
        query = """SELECT *
                   FROM Resorts
                   WHERE resort_id = {};""".format(resort)
    else:
        if type(resort) == str:
            if resort == '*':
                query = """SELECT * FROM Resorts;"""
            else:
                query = """SELECT * 
                           FROM Resorts
                           WHERE name = '{}';""".format(resort)
    curs.execute(query)
    result = curs.fetchall()
    result = pd.DataFrame(result, columns = ['resort_id','name','address','longitude','latitude'])
    return result

def getWeather(resort,curs):
    if type(resort) == int:
        query = """SELECT Weather.resort_id,
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
                           Resorts.name
                   FROM Weather
                    INNER JOIN Resorts on Resorts.resort_id = Weather.resort_id
                   WHERE resort_id = {};""".format(resort)
    else:
        if type(resort) == str:
            if resort == '*':
                query = """SELECT Weather.resort_id,
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
                           Resorts.name
                           FROM Weather
                           INNER JOIN Resorts on Resorts.resort_id = Weather.resort_id;"""
            else:
                query = """SELECT Weather.resort_id,
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
                                  Resorts.name
                           FROM Weather

                            INNER JOIN Resorts on Resorts.resort_id = Weather.resort_id

                           WHERE Resorts.name = '{}'
                           ORDER BY date;""".format(resort)

    curs.execute(query)
    result = curs.fetchall()
    result = pd.DataFrame(result, columns = 
       ['resort_id',
        'date',
        'min_temp',
        'max_temp',
        'feels_like',
        'precipitation_probability',
        'visibility',
        'wind_direction',
        'wind_speed',
        'snow_depth',
        'mountain_segment',
        'name'])
    return result

def getUser(user,curs):
    if type(user) == int:
        query = """SELECT *
                   FROM Users
                   WHERE user_id = {};""".format(user)
    else:
        if type(user) == str:
            if user == '*':
                query = """SELECT * FROM Users;"""
            else:
                query = """SELECT *
                           FROM Users
                           WHERE user_name = '{}';""".format(user)

    curs.execute(query)
    result = curs.fetchall()
    result = pd.DataFrame(result,columns = 
            ['user_id',
            'user_name',
            'first_name',
            'last_name',
            'email',
            'permission',
            'num_fav_resorts'])
    return result

def getUserFavourites(user,curs):
    if type(user) == int:
        query = """SELECT
                   Resorts.name,
                   Users.user_name,
                   Users.user_id
                   FROM Favourites
                      INNER JOIN Resorts on Resorts.resort_id = Favourites.resort_id
                      INNER JOIN Users on Users.user_id = Favourites.user_id

                   WHERE user_id = {};""".format(user)
    if type(user) == str:
        if user == '*':
            query = """SELECT
                       Resorts.name,
                       Users.user_name,
                       Users.user_id
                       FROM Favourites
                        INNER JOIN Resorts on Resorts.resort_id = Favourites.resort_id
                        INNER JOIN Users on Users.user_id = Favourites.user_id;"""
        else:
            query = """SELECT
                       Resorts.name,
                       Users.user_name,
                       Users.user_id
                       FROM Favourites
                        INNER JOIN Resorts on Resorts.resort_id = Favourites.resort_id
                        INNER JOIN Users on Users.user_id = Favourites.user_id
                       WHERE Users.user_name = '{}';""".format(user)

    curs.execute(query)
    result = curs.fetchall()
    result = pd.DataFrame(result, columns = ['resort_name','user_name','user_id'])
    return result

def insertUser(user_name,first_name,last_name,email,permission,num_fav_resorts,curs):
    query = """INSERT INTO Users(user_name,first_name,last_name,email,permission,num_fav_resorts) VALUES('{}','{}','{}','{}',{},{});""".format(
            user_name,
            first_name,
            last_name,
            email,
            permission,
            num_fav_resorts)
    curs.execute(query)

def insertResort(name,address,longitude,latitude,curs):
    query = """INSERT INTO Resorts(name,address,longitude,latitude) VALUES('{}','{}',{},{});""".format(
            name,
            address,
            longitude,
            latitude)
    curs.execute(query)

def insertWeather(date,min_temp,max_temp,feels_like,precipitation_probability,visibility,wind_direction,wind_speed,snow_depth,mountain_segment,resort_id,curs):
    query = """INSERT INTO Weather(resort_id,date,min_temp,max_temp,feels_like,precipitation_probability,visibility,wind_direction,wind_speed,snow_depth,mountain_segment) VALUES({},'{}',{},{},{},{},{},'{}',{},{},{});""".format(resort_id,date,
            min_temp,
            max_temp,
            feels_like,
            precipitation_probability,
            visibility,
            wind_direction,
            wind_speed,
            snow_depth,
            mountain_segment)
    curs.execute(query)
def updateWeather(setparam,setval,whereparam,whereval,curs):
    if setparam or setval or whereparam or whereval != '' or NULL or '*':

        query = """UPDATE Weather
                   SET {} = {}
                   WHERE {} = {};""".format(setparam,setval,whereparam,whereval)
        print(query)
        curs.execute(query)
    else:
        print("can only edit one entry per query OR your values are empty")

def insertFavourite(user_id,resort_id,curs):
    query = """INSERT INTO Favourites(user_id,resort_id) VALUES({},{});""".format(user_id,resort_id)
    curs.execute(query)


def removeResort(resort_id,curs):
    if resort_id != '*':    
        query = """DELETE FROM Resorts WHERE resort_id = {};""".format(resort_id)
        query2 = """DELETE FROM Weather WHERE resort_id = {};""".format(resort_id)
        query3 = """DELETE FROM Favourites WHERE resort_id = {};""".format(resort_id)
        curs.execute(query)
        curs.execute(query2)
        curs.execute(query3)
    else:
        print('stop trying to delete everything, please')

def removeUser(user_id,curs):
    if user_id != '*':         
        query = """DELETE FROM Users WHERE user_id = {};""".format(user_id)
        query2 = """DELETE FROM Favourites WHERE user_id = {};""".format(user_id)
        curs.execute(query)
        curs.execute(query2)
    else:
        print('stop trying to delete everything, please')
def removeWeather(param,val,curs):
    if param or val != '*':
        query = """DELETE FROM Weather WHERE {} = {};""".format(param,val)
        curs.execute(query)
    else:
        print('stop trying to delete everything, please')


def removeFavourite(user_id,resort_id,curs):
    if user_id or resort_id != '*':
        query = """DELETE FROM Favourites WHERE user_id = {} AND resort_id = {};""".format(user_id,resort_id)
        curs.execute(query)
    else:
        print('stop trying to delete everything, please')

