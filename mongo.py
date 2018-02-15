import pymongo
import math
import urllib2

connection = pymongo.MongoClient("149.89.150.100")
db = connection.test
collection = db.restaurants

def boro(name):
    cursor = collection.find({ "borough" : name, "borough." + name + ".name" : {"$ne" : ""} } )
    for i in cursor:
        print i["name"]
        #print i["borough"]

def zipcode(code):
    cursor = collection.find({ "address.zipcode" : code })
    for i in cursor:
        print i["name"]
        #print i["address"]["zipcode"]

def zipgrade(code, grade):
    cursor = collection.find({ "address.zipcode" : code, "grades.grade" : grade })
    for i in cursor:
        print i["name"]
        #print i["grades"][0]["grade"]

def zipbelowscore(code, score):
    cursor = collection.find({ "address.zipcode" : code, "grades.score" : {"$lt" : score} })
    for i in cursor:
        print i["name"]
        #print i["grades"][0]["score"]
        
def closest(dict):
    latitude = dict['lat']
    longitude = dict['long']
    cursor = collection.find()
    winner = 999999999999999999999999999999999999999999999999
    for i in cursor:
        try:
            dist = distance(latitude, longitude, i["address"]["coord"][1], i["address"]["coord"][0])
            #print dist
            if dist < winner:
                winner = dist
                ans = i["name"]
                #print ans
        except:
            pass
    print "closest: " + ans

#in case web crawling/urllib2 not working
def closest_latlong(latitude, longitude):
    cursor = collection.find()
    winner = 999999999999999999999999999999999999999999999999
    for i in cursor:
        try:
            dist = distance(latitude, longitude, i["address"]["coord"][1], i["address"]["coord"][0])
            #print dist
            if dist < winner:
                winner = dist
                ans = i["name"]
                #print ans
        except:
            pass
    print "closest: " + ans

    
def distance(sx,sy,ex,ey): #gives the distance between two points using the haversine formula
    lateral_distance = sx-ex
    longitudal_distance = sy-ey
    a = math.sin(math.radians(lateral_distance/2))**2 + math.cos(math.radians(sx)) * math.cos(math.radians(ex)) * math.sin(math.radians(longitudal_distance/2))**2
    c = 2 * math.atan2((a**0.5 ),(1-a**0.5))
    d = 3959 * c
    return d

def getCoords(address):  #returns the map of the latitude/longitude of the user inputted address so far
    address = address.replace(' ',"+")  #replaces spaces in user inputted address value with +'s in order to comply with gmap's API
    url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyD7g6o2aIIo3ZlXtYbc4LjhcUaRizS1DKU" % address  #geocodes the address
    response = urllib2.urlopen(url)
    info = response.read() #these past few lines basically assign a json formatted file from google api to info
    info = info.replace('true','True') #puts booleans in proper format
    exec "info =" + info #executes a string that sets variable "info" equal to the python formatted stuff
    try:
        lat = info["results"][0]['geometry']['location']['lat']  #gets latitude
    except IndexError:
        print 'Location: index.html'
        print #blank print
    lng = info["results"][0]['geometry']['location']['lng']  #gets longitude
    return {'long': lng, 'lat': lat}
                                                                                    

        
#boro("Manhattan")
#zipcode("10282")
#zipgrade("10282", "A")
#zipbelowscore("10282", 2)

#see http://homer.stuy.edu/~henry.zheng/proj/
closest(getCoords("stuyvesant high school"))
#closest_latlong(40.718041, -74.013881)
