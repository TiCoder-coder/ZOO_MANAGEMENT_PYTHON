# ---------------------------------DINH NGHIA CAC HAM DUNG DE TUONG TAC VOI DATABASE --------------------------------------------------------------------------


from pymongo import MongoClient
from decouple import config
from bson import ObjectId

# Dinh nghia mot client dung de goi database
client = MongoClient(config("MONGO_URI"))
db = client[config("DB_NAME")]
manager_collection = db["managers"]

# Dinh nghia mot class dung de tuong tac truc tiep voi database ---- Tang service se su dung lai
class ManagerRepository:

    # Ham dung de them moi mot manager vao database
    @staticmethod
    def insert_one(data):
        return manager_collection.insert_one(data)
    
    # Ham dung de lay thong tin tat ca cac manager
    @staticmethod
    def find_all():
        return list(manager_collection.find())

    # Ham dung de tim thong tin cua manager theo id
    @staticmethod
    def find_by_id(idManager):
        return manager_collection.find_one({"_id": ObjectId(idManager)})

    # Ham dung de tim manager theo uesrName va id
    @staticmethod
    def find_by_username_or_email(identifier):
        return manager_collection.find_one({"$or": [{"userName": identifier}, {"email": identifier}]})

    # Ham dung de tim kiem thong tin theo uerNAme
    @staticmethod
    def find_by_username(userName):
        return manager_collection.find_one({"userName": userName})

    # Ham dung de cap nhap thong tin manager theo id
    @staticmethod
    def update_by_id(idManager, update_data):
        return manager_collection.update_one({"_id": ObjectId(idManager)}, {"$set": update_data})

    # Ham dung de delete mot manager theo id
    @staticmethod
    def delete_by_id(idManager):
        return manager_collection.delete_one({"_id": ObjectId(idManager)})
