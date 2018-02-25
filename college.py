'''
Reddit
Subreddit: Applying To College
Descrpition from site:
    "/r/ApplyingToCollege is the premier forum for college 
     admissions questions, advice, and discussions, from 
     college essays and scholarships to SAT/ACT test prep, 
     career guidance, and more."

Dataset Link: https://www.reddit.com/r/ApplyingToCollege.json

Import mechanism:
    From the url above, we use the requests module to decode 
    the json file from the website and read the data into our python script. 
    1) Import json and requests
    2) Store json link in a variable
    3) Read the url using requests.get()
    4) Decode webpage to json file using json()
'''

import pymongo, json, requests


link = 'https://www.reddit.com/r/ApplyingToCollege.json'
r = requests.get(link, headers = {'User-agent': 'fourthTermJuniors'})
data = r.json()
posts = data["data"]["children"]

connection = pymongo.MongoClient("149.89.150.100")
db = connection.fourthTermJuniors
collection = db.a2c


def addToCollection(collection):
    for each in posts:
        #print collection.update({ "data.title" : each["data"]["title"] }, each, upsert=True)
        collection.update({ "data.title" : each["data"]["title"] }, each, upsert=True)

        
def suggested_sort(suggested):
    print "==========printing posts with suggested_sort = " + suggested + "...=========="
    cursor = collection.find({ "data.suggested_sort" : suggested })
    for i in cursor:
        print "\t" + i["data"]["title"]
        
def upvotes(number):
    print "==========printing posts with upvotes > " + str(number) + "...=========="
    cursor = collection.find({ "data.ups" : {"$gt" : number} })
    for i in cursor:
        print "\t" + str(i["data"]["ups"]) + ": " + i["data"]["title"]

def score(number):
    print "==========printing posts with score > " + str(number) + "...=========="
    cursor = collection.find({ "data.score" : {"$gt" : number} })
    for i in cursor:
        print "\t" + str(i["data"]["score"]) + ": " + i["data"]["title"]
        
def stickied():
    print "==========printing stickied posts...=========="
    cursor = collection.find({ "data.stickied" : True })
    for i in cursor:
        print "\t" + i["data"]["title"]

def nonstickied():
    print "==========printing nonstickied posts...=========="
    cursor = collection.find({ "data.stickied" : False })
    for i in cursor:
        print "\t" + i["data"]["title"]


addToCollection(collection)

suggested_sort("confidence")
upvotes(15)
upvotes(300)
score(15)
score(300)
stickied()
nonstickied()
