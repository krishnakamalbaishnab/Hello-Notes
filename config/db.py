from pymongo import MongoClient
from config.settings import settings

class Database:
    client: MongoClient = None
    
    def connect_to_database(self):
        if not self.client:
            self.client = MongoClient(settings.MONGO_URI)
        
    def close_database_connection(self):
        if self.client:
            self.client.close()
            self.client = None
            
    def get_database(self):
        if not self.client:
            self.connect_to_database()
        return self.client[settings.DATABASE_NAME]

db = Database()
