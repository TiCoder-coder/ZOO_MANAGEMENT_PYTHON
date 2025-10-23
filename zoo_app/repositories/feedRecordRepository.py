# ---------------------------------DINH NGHIA CAC HAM DUNG DE TUONG TAC VOI DATABASE --------------------------------------------------------------------------


from pymongo import MongoClient
from decouple import config

# Dinh nghia mot client dung de goi database
client = MongoClient(config("MONGO_URI"))
db = client[config("DB_NAME")]
feedRecord_collection = db["feed_records"]

# Dinh nghia mot class dung de tuong tac truc tiep voi database ---- Tang service se su dung lai
class FeedRecordRepository:
    
    # Ham dung de tao mot bao cao feedRecord moi vao databse
    @staticmethod
    def insert_one(data):
        return feedRecord_collection.insert_one(data)
    
    
    # Ham dung de xuat thong tin tat ca cac bao cao
    @staticmethod
    def find_all():
        return list(feedRecord_collection.find())

    
    # Ham dung de xuat thong tin cua mot bao cao theo id
    @staticmethod
    def find_by_id(idFeedRecord):
        return feedRecord_collection.find_one({"idFeedRecord": idFeedRecord})  # ✅ sửa id -> idFeedRecord

    
    # Ham dung de cap nhap thong tin cua bao cao theo id
    @staticmethod
    def update_by_id(idFeedRecord, update_data):
        return feedRecord_collection.update_one({"idFeedRecord": idFeedRecord}, {"$set": update_data})

    # Ham dung de xoa mot bao cao theo id
    @staticmethod
    def delete_by_id(idFeedRecord):
        return feedRecord_collection.delete_one({"idFeedRecord": idFeedRecord})
