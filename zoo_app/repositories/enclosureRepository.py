# ---------------------------------DINH NGHIA CAC HAM DUNG DE TUONG TAC VOI DATABASE --------------------------------------------------------------------------


from pymongo import MongoClient
from decouple import config


# Dinh nghia mot client dung de goi database
client = MongoClient(config("MONGO_URI"))
db = client[config("DB_NAME")]
enclosure_collection = db["enclosures"]


# Dinh nghia mot class dung de tuong tac truc tiep voi database ---- Tang service se su dung lai
class EnclosureRepository:
    
    
    # Ham dung de them mot enclosure moi vao database
    @staticmethod
    def insert_one(data):
        return enclosure_collection.insert_one(data)
    
    # Ham dung de xuat thong tin tat ca cac enclosure trong zoo
    @staticmethod
    def find_all():
        return list(enclosure_collection.find())


    # Ham dung de xuat thong tin cua mot enclosure nao do theo id
    @staticmethod
    def find_by_id(idEnclosure):
        try:
            return enclosure_collection.find_one({"_id": ObjectId(idEnclosure)})
        except Exception:
            return enclosure_collection.find_one({"idEnclosure": idEnclosure})

    
    # Cap nhap enclosure theo id
    @staticmethod
    def update_by_id(idEnclosure, update_data):
        return enclosure_collection.update_one({"idEnclosure": idEnclosure}, {"$set": update_data})

    # Delete mot enclosure theo id
    @staticmethod
    def delete_by_id(idEnclosure):
        return enclosure_collection.delete_one({"idEnclosure": idEnclosure})
