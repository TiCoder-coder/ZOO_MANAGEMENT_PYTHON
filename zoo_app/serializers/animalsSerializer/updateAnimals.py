from .baseSerializerAnimal import BaseSerializerAnimal

# Tao mot du lieu json khi cap nhap thong tin animal
class AnimalUpdate (BaseSerializerAnimal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False                                              # Cac thuoc tinh la khong bat buoc
        
        # Loai bo field id khi update
        if "id" in self.fields:
            self.fields.pop("id")