from datetime import datetime, timezone
from rest_framework.exceptions import ValidationError, NotFound
from zoo_app.repositories.feedRecordRepository import FeedRecordRepository
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

class FeedRecordService:


    # CREATE FEEDRECORD ---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_feedRecord(user, validated_data):
        require_manager(user)                                                               # PHAN QUYEN: CHI MANAGER MOI SU DUNG DUOC
        try:
            
            # Tu dong tao createAt, updateAt, feedAt
            validated_data["feedAt"] = datetime.now(timezone.utc)
            validated_data["createAt"] = datetime.now(timezone.utc)
            validated_data["updateAt"] = datetime.now(timezone.utc)

            # Them feedRecord vao database
            FeedRecordRepository.insert_one(validated_data)
            return validated_data["idFeedRecord"]
        except Exception as e:
            raise ValidationError(f"Error creating feedRecord: {str(e)}")


    # REVIEW ALL FEEDRECORD ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_feedRecord(user):
        require_staff_or_manager(user)                                                      # PHAN QUYEN: STAFF HAY MANAGER DEU SU DUNG DUOC
        try:
            
            # Goi ham de lay tat ca cac thong tin
            records = FeedRecordRepository.find_all()
            
            # Chuyen doi cac thong tin sang str va return
            return convert_objectid(records)
        except Exception as e:
            raise ValidationError(f"Error reviewing feedRecords: {str(e)}")


    # REVIEW FEEDRECORD BY ID -------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_feedRecord_by_id(user, idFeedRecord):
        require_staff_or_manager(user)                                                      # PHAN QUYEN: STAFF HAY MANAGER DEU SU DUNG DUOC
        try:
            
            # Kiem tra feedRecord co ton tai khong
            record = FeedRecordRepository.find_by_id(idFeedRecord)
            if not record:
                raise ValidationError(f"No feedRecord found with id: {idFeedRecord}")
            
            # Chuyen doi thong tin sang str -> return 
            return convert_objectid(record)
        except Exception as e:
            raise ValidationError(f"Error reviewing feedRecord by id: {str(e)}")


    # UPDATE FEEDRECORD ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def update_feedRecord(user, idFeedRecord, validated_data):
        
        require_manager(user)                                                               # PHAN QUYEN: CHI MANAGER MOI SU DUNG DUOC
        
        # Kiem tra feedRecord co ton tai khong
        feedRecord = FeedRecordRepository.find_by_id(idFeedRecord)
        if not feedRecord:
            raise NotFound(detail=f"Không tìm thấy món ăn với idFeedRecord '{idFeedRecord}'.")

        # Goi ham cap nhap theo id
        FeedRecordRepository.update_by_id(idFeedRecord, validated_data)
        updated = FeedRecordRepository.find_by_id(validated_data.get('idFeedRecord', idFeedRecord))
        return updated


    # DELETE FEEDRECORD -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete_feedRecord(user, idFeedRecord):
        require_manager(user)                                                               # PHAN QUYEN: CHI MANAGER MOI SU DUNG DUOC
        try:
            
            # Delete thong tin feedRecord
            result = FeedRecordRepository.delete_by_id(idFeedRecord)
            if result.deleted_count == 0:
                raise ValidationError(f"No feedRecord found with id: {idFeedRecord}")
            return {"Deleted": True}
        except Exception as e:
            raise ValidationError(f"Error deleting feedRecord: {str(e)}")
