from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('.ini')

URI = config['DB']['URI']
client =MongoClient(URI)


db = client.laptops


def insert_laptops(laptops):
    
    return db.laptops.insert_many(laptops)