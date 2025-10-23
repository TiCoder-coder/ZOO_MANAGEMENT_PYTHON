from datetime import datetime, timezone
from rest_framework.exceptions import ValidationError, NotFound
from zoo_app.repositories.foodRepository import FoodRepository
from bson import ObjectId
from zoo_app.middleware.auth import require_manager, require_staff_or_manager

# Dinh nghia mot ham dung de convert cac object -> str
def convert_objectid(obj):
    # Neu la list: duyet qua cac phan tu torng list va chuyen doi object -> str
    if isinstance(obj, list):
        return [convert_objectid(o) for o in obj]
    
    # Neu la dict: duyet qua cac phan tu va xu li cho tung key, value
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                new_obj[k] = str(v)
            else:
                new_obj[k] = convert_objectid(v)
        return new_obj
    return obj


# --------------------------------------------- CLASS KHONG TRUC TIEP TUONG TAC VOI DATABASE MA SE THONG QUA REPOSITORY DE TUONG TAC ----------------------------------------------------------------------- 
# ------------------------------------------------------------------VA PHAN QUYEN SU DUNG CHO STAFF HAY MANAGER VA ADMIN------------------------------------------------------------------------------------    

class FoodService:
    
    
    # CREATE FOOD ------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def create_food(user, validated_data):
        require_manager(user)
        try:
            
            # Tu dong tao createAt, updateAt
            validated_data["createAt"] = datetime.now(timezone.utc)
            validated_data["updateAt"] = datetime.now(timezone.utc)
            FoodRepository.insert_one(validated_data)
            return validated_data["idFood"]
        except Exception as e:
            raise ValidationError(f"Error creating food: {str(e)}")
        
    
    # REVIEW ALL FOOD ---------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def review_all_foods(user):
        require_staff_or_manager(user)
        try:
            
            # Goi ham de lay tat ca cac thong tin va return ra
            return FoodRepository.find_all()
        except Exception as e:
            raise ValidationError(f"Error reviewing foods: {str(e)}")


    # REVIEW FOOD BY ID ------------------------------------------------------------------------------------------------------------------------
    
    def review_food_by_id(user, idFood):
        require_staff_or_manager(user)
        try:
            food = FoodRepository.find_by_id(idFood)
            if not food:
                raise ValidationError(f"No food found with id: {idFood}")
            return convert_objectid(food)
        except Exception as e:
            raise ValidationError(f"Error reviewing food by id: {str(e)}")

    

    # UPDATE FOOD ------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def update_food(user, idFood, data):
        require_manager(user)
        food = FoodRepository.find_by_id(idFood)
        if not food:
            raise NotFound(detail=f"Không tìm thấy món ăn với idFood '{idFood}'.")

        FoodRepository.update_by_id(idFood, data)
        updated = FoodRepository.find_by_id(data.get('idFood', idFood))
        return updated


    # DELETE ANIMAL ------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def delete_food(user, idFood):
        require_manager(user)
        try:
            result = FoodRepository.delete_by_id(idFood)
            if result.deleted_count == 0:
                raise ValidationError(f"No food found with id: {idFood}")
            return {"Deleted": True}
        except Exception as e:
            raise ValidationError(f"Error deleting food: {str(e)}")
