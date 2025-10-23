from datetime import datetime, timezone
from rest_framework.exceptions import ValidationError
from zoo_app.repositories.animalRepository import AnimalRepository
from zoo_app.middleware.auth import require_manager, require_staff_or_manager

# --------------------------------------------- CLASS KHONG TRUC TIEP TUONG TAC VOI DATABASE MA SE THONG QUA REPOSITORY DE TUONG TAC ----------------------------------------------------------------------- 
# ------------------------------------------------------------------VA PHAN QUYEN SU DUNG CHO STAFF HAY MANAGER VA ADMIN------------------------------------------------------------------------------------    
class AnimalService:
    
    
    # CREATE ANIMAL ------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_animal(user, validated_data):
        require_manager(user)                                                                 # PHAN QUYEN: CHI CO MANAGER MOI DUOC SU DUNG
        try:
            
            # Tu dong tao createAt, updateAt
            validated_data["createdAt"] = datetime.now(timezone.utc)
            validated_data["updatedAt"] = datetime.now(timezone.utc)

            # Thong qua rang repository de insert du lieu vao database
            result = AnimalRepository.insert_one(validated_data)

            # Truy cap lai database xem da insert thanh cong chua
            new_animal = AnimalRepository.find_by_id(validated_data["id"])
            if not new_animal:
                raise ValidationError(f"Inserted but not found with id: {validated_data['id']}")

            # Chuyen doi object -> str de in ra (tranh loi drf khong doc duoc)
            if "_id" in new_animal:
                new_animal["_id"] = str(new_animal["_id"])

            return new_animal

        except Exception as e:
            raise ValidationError(f"Error creating animal: {str(e)}")
        
        
    # REVIEW ALL ANIMAL ---------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_animal(user):
        require_staff_or_manager(user)                                                       # PHAN QUYEN: STAFF HAY MANAGER DEU SU DUNG DUOC
        try:
            # Goi ham de lay tat ca cac thong tin
            animals = AnimalRepository.find_all()
            
            # Chuyen sang json de in ra
            for animal in animals:
                if "_id" in animal:
                    animal["_id"] = str(animal["_id"])
            return animals
        except Exception as e:
            raise ValidationError(f"Error reviewing animals: {str(e)}")


    # REVIEW ANIMAL BY ID ------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_animal_by_id(user, idAnimal):
        require_staff_or_manager(user)                                                      # PHAN QUYEN: STAFF HAY MANAGER DEU SU DUNG DUOC
        
        try:
            animal = AnimalRepository.find_by_id(idAnimal)
            if not animal:
                raise ValidationError(f"No animal found with id: {idAnimal}")
            
            # Kiem tra xem id co ton tai khong --- Neu co --> in ra
            if "_id" in animal:
                animal["_id"] = str(animal["_id"])
            return animal
        
        except Exception as e:
            raise ValidationError(f"Error reviewing animal by id: {str(e)}")

    


    # UPDATE ANIMAL ------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def update_animal(user, idAnimal, validated_data):
        require_manager(user)                                                               # PHAN QUYEN: CHI MANAGER MOI SU DUNG DUOC
        try:
            
            # Kiem tra animal co ton tai khong de update
            existing_animal = AnimalRepository.find_by_id(idAnimal)
            if not existing_animal:
                raise ValidationError(f"No animal found with id: {idAnimal}")

            # Cap nhap lai updateAt
            validated_data["updatedAt"] = datetime.now(timezone.utc)

            # Khong cap nhap id
            if "id" in validated_data:
                validated_data.pop("id")

            
            # Update lai thong tin
            AnimalRepository.update_by_id(idAnimal, validated_data)
            
            # Sau khi update thi kiem tra lai thong tin da duoc update hay chua
            updated_animal = AnimalRepository.find_by_id(idAnimal)
            
            # Neu da duoc update thi chuyen id tu object -> str va return
            if "_id" in updated_animal:
                updated_animal["_id"] = str(updated_animal["_id"])
            return updated_animal

        except Exception as e:
            raise ValidationError(f"Error updating animal: {str(e)}")


    # DELETE ANIMAL ------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete_animal(user, idAnimal):
        require_manager(user)                                                               # PHAN QUYEN: CHI MANAGER MOI SU DUNG DUOC
        
        try:
            
            # Kiem tra animal co ton tai khong de delete
            existing_animal = AnimalRepository.find_by_id(idAnimal)
            
            # Neu khong co thi bao loi
            if not existing_animal:
                raise ValidationError(f"No animal found with id: {idAnimal}")

            # Neu co thi delete
            result = AnimalRepository.delete_by_id(idAnimal)
            if result.deleted_count == 0:
                raise ValidationError(f"Delete failed for id: {idAnimal}")

            # Tra ve da delete thanh cong
            return {"Deleted": True}
        except Exception as e:
            raise ValidationError(f"Error deleting animal: {str(e)}")
