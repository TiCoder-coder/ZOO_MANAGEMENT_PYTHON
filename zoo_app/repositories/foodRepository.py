# ---------------------------------DINH NGHIA CAC HAM DUNG DE TUONG TAC VOI DATABASE --------------------------------------------------------------------------


from pymongo import MongoClient
from decouple import config

# Dinh nghia mot client dung de goi database
client = MongoClient(config("MONGO_URI"))
db = client[config("DB_NAME")]
food_collection = db["foods"]

# Dinh nghia mot class dung de tuong tac truc tiep voi database ---- Tang service se su dung lai
class FoodRepository:
    
    
    # Ham dung de them moi mot thong tin mon an vao database
    @staticmethod
    def insert_one(data):
        return food_collection.insert_one(data)
    
    
    # Lay tat ca cac thong tin food tu database
    @staticmethod
    def find_all():
        return list(food_collection.find())

    # Lay cac thong tin food theo id tu database
    @staticmethod
    def find_by_id(idFood):
        return food_collection.find_one({"idFood": idFood})

    
    # Cap nhap thong tin cua food theo id
    @staticmethod
    def update_by_id(idFood, update_data):
        return food_collection.update_one({"idFood": idFood}, {"$set": update_data})

    # Xoa thong tin cua food theo id
    @staticmethod
    def delete_by_id(idFood):
        return food_collection.delete_one({"idFood": idFood})
    