import pymongo
from pymongo import MongoClient

import configparser

config = configparser.ConfigParser()
config.read('.ini')

URI = config['DB']['URI']
client =MongoClient(URI)


db = client.laptops


def insert_laptops(laptops):
    print("the number of crawled items : ",len(laptops))
    
    try:
        insert_many_result = db.tests.insert_many(laptops,ordered=False)
        nr_inserts = len(insert_many_result.inserted_ids)
        print("the number of inserted when ok :",nr_inserts)
    except pymongo.errors.BulkWriteError as bwe:
        nr_inserts = bwe.details["nInserted"]
        print("the number of inserted when not OK:",nr_inserts)

def insert_laptops_2(laptops):
    print("the number of crawled items : ",len(laptops))
    for laptop in laptops:
        
        if laptop["price"]:
            try:
                insert_one_result = db.tests.insert_many(laptop)
            except:
                print ("... laptop not inserted")
