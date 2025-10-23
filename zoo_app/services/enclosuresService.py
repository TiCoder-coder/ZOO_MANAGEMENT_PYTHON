from datetime import datetime, timezone
from rest_framework.exceptions import ValidationError
from zoo_app.repositories.enclosureRepository import EnclosureRepository
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

class EnclosureService:


    # CREATE ENCLOSURE  -------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_enclosure(user, validated_data):
        require_manager(user)                                                                # PHAN QUYEN: CHI CO MANAGER MOI DUOC SU DUNG
        try:
            
            # Tu dong tao createAt, updateAt
            validated_data["createAt"] = datetime.now(timezone.utc)
            validated_data["updateAt"] = datetime.now(timezone.utc)
            
            # Thong qua rang repository de insert du lieu vao database
            result = EnclosureRepository.insert_one(validated_data)
            
            # Tra ve id vua insert
            return str(result.inserted_id)
        except Exception as e:
            raise ValidationError(f"Error creating enclosure: {str(e)}")
        
        
    # REVIEW ALL ENCLOSURE  ---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_enclosure(user):
        require_staff_or_manager(user)                                                       # PHAN QUYEN: STAFF HAY MANAGER DEU SU DUNG DUOC
        try:
            
            # Goi ham de lay tat ca cac thong tin
            enclosures = EnclosureRepository.find_all()
            
            # Chuyen sang str va in ra
            return convert_objectid(enclosures)
        except Exception as e:
            raise ValidationError(f"Error reviewing enclosures: {str(e)}")

    # REVIEW ENCLOSURE BY ID -------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_enclosure_by_id(user, idEnclosure):
        require_staff_or_manager(user)                                                       # PHAN QUYEN: STAFF HAY MANAGER DEU SU DUNG DUOC
        try:
            
            # Kiem tra id co ton tai khong
            enclosure = EnclosureRepository.find_by_id(idEnclosure)
            if not enclosure:
                raise ValidationError(f"No enclosure found with id: {idEnclosure}")
            
            # Chuyen doi ra str va return
            return convert_objectid(enclosure)
        except Exception as e:
            raise ValidationError(f"Error reviewing enclosure by id: {str(e)}")

    

    # UPDATE ENCLOSURE -------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def update_enclosure(user, idEnclosure, validated_data):
        require_manager(user)                                                                 # PHAN QUYEN: CHI CO MANAGER MOI DUOC SU DUNG
        try:
            
            # Kiem tra enclosure co ton tai hay khong
            existing = EnclosureRepository.find_by_id(idEnclosure)
            if not existing:
                raise ValidationError(f"No enclosure found with id: {idEnclosure}")

            # Giu nguyen cac attribute cu neu khong co thong tin moi
            for k, v in existing.items():
                if k not in validated_data:
                    validated_data[k] = v

            # Cap nhap lai ngay update
            validated_data["updateAt"] = datetime.now(timezone.utc)
            
            # Update
            result = EnclosureRepository.update_by_id(idEnclosure, validated_data)
            
            # Kiem tra thong tin da duoc update hay chua
            if result.matched_count == 0:
                raise ValidationError(f"No enclosure found with id: {idEnclosure}")
            return {"Updated": True}
        except Exception as e:
            raise ValidationError(f"Error updating enclosure: {str(e)}")

    # DELETE ENCLOSURE -------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete_enclosure(user, idEnclosure):
        require_manager(user)                                                                 # PHAN QUYEN: CHI CO MANAGER MOI DUOC SU DUNG
        try:
            # Goi ham xoa thong tin
            result = EnclosureRepository.delete_by_id(idEnclosure)
            
            # Neu khong co du lieu nao khop thi in ra loi
            if result.deleted_count == 0:
                raise ValidationError(f"No enclosure found with id: {idEnclosure}")
            return {"Deleted": True}
        except Exception as e:
            raise ValidationError(f"Error deleting enclosure: {str(e)}")
