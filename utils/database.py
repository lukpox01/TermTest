from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv('URI')
        self.client = None
        self.mydb = None
        self.users = None
        self.connect()
        self.create_database()

    def connect(self):
        self.client = MongoClient(self.uri)

    def create_database(self):
        self.mydb = self.client["TermTest"]
        self.users = self.mydb["users"]

    def add_user(self, name, password, email, version=0.0):
        dic = {"name": name, "password": password, "email": email, "version": version}
        self.users.insert_one(dic)

    def find_user(self, name, password):
        query1 = {"$or": [{"$and": [{"name": name}, {"password": password}]},
                          {"$and": [{"email": name}, {"password": password}]}]}
        result = self.users.find_one(query1)

        return result

    def is_empty(self):
        result = self.users.find_one()
        if result is None:
            return True
        return False

    def name_exists(self, name):
        result = self.users.find({},{"name": 1})
        for name_ in result:
            if name == name_:
                return True
        return False

    def delete_user(self, name, password):
        query1 = {"$or": [{"$and": [{"name": name}, {"password": password}]},
                          {"$and": [{"email": name}, {"password": password}]}]}
        self.users.delete_one(query1)


