# ---------------------------------DINH NGHIA CAC HAM DUNG DE TUONG TAC VOI DATABASE --------------------------------------------------------------------------

from pymongo import MongoClient
from decouple import config

# Dinh nghia mot client dung de goi database
client = MongoClient(config("MONGO_URI"))
db = client[config("DB_NAME")]
animal_collection = db["animals"]

# Dinh nghia mot class dung de tuong tac truc tiep voi database ---- Tang service se su dung lai
class AnimalRepository:
    
    # Ham dung de them mot animal moi vao database
    @staticmethod
    def insert_one(data):
        return animal_collection.insert_one(data)
    
    
    # Ham dung de lay thong tin tat ca cac animal
    @staticmethod
    def find_all():
        return list(animal_collection.find())


    # Ham dung de lay thong tin 1 animal theo id
    @staticmethod
    def find_by_id(idAnimal):
        return animal_collection.find_one({"id": idAnimal})


    # Ham dung de cap nhap 1 animal theo id
    @staticmethod
    def update_by_id(idAnimal, update_data):
        return animal_collection.update_one({"id": idAnimal}, {"$set": update_data})


    # Ham dung de xoa mot animal theo id
    @staticmethod
    def delete_by_id(idAnimal):
        return animal_collection.delete_one({"id": idAnimal})
    
    