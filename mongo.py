import pymongo

connection = pymongo.MongoClient("149.89.150.100")
db = connection.test
collection = db.restaurants

def boro(name):
    cursor = collection.find({ "borough" : name, "borough." + name + ".name" : {"$ne" : ""} } )
    for i in cursor:
        print i["name"]
        
boro("Manhattan")
