from .baseSerializerAnimal import BaseSerializerAnimal


# Tao du lieu json khi tao mot animal
class AnimalCreate (BaseSerializerAnimal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dinh nghia cac thuoc tinh bat buoc khi khoi tao
        field_required = ["id", "name", "age", "species", "gender", "weight", "healthStatus", "enclosureId"]
        for field_name, field in self.fields.items():
            if field in self.fields:
                field.required = True