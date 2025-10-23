from .baseSerializerManagers import BaseSerializerManager


# Tao du lieu json khi tao mot manager
class ManagerCreate(BaseSerializerManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dinh nghia cac thuoc tinh bat buoc khi khoi tao
        required_fields = ["name", "userName", "password", "email", "role"]
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
