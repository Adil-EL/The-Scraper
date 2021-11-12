from pymongo import MongoClient

URI = "mongodb+srv://AdilLaptops:AdilLaptops@laptops.m72a4.mongodb.net"
client =MongoClient(URI)

db = client.laptops


def Add_laptops(laptops):
    
    return db.laptops.insert_many(laptops)